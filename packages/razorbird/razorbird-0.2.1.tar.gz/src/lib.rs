use std::collections::HashMap;
use std::convert::Infallible;
use std::process;

use hyper::http::Version;
use hyper::header::{HeaderName, HeaderValue,CONTENT_LENGTH,CONTENT_TYPE};
use hyper::http::status::StatusCode;
use hyper::service::{make_service_fn, service_fn};
use hyper::{Body, Request, Response, Server};
use tokio::runtime;

use pyo3::prelude::*;
use pyo3::ffi::PyErr_CheckSignals;
use pyo3::types::{IntoPyDict,PyList,PyTuple};
use pyo3::wrap_pyfunction;


fn internal_server_error() -> Response<Body> {
    Response::builder()
        .status(StatusCode::INTERNAL_SERVER_ERROR)
        .body(Body::from("Internal Server Error"))
        .expect("this ought to work")
}

fn from_wsgi_response(py: Python, wsgi_resp: PyObject) -> PyResult<Response<Body>> {
    let result = wsgi_resp.cast_as::<PyList>(py)?;
    if result.len() != 3 {
        Ok (internal_server_error() )
    } else {
        let status: String = result.get_item(0).extract()?;
        let (status_code, _) = status.split_at(3);
        let mut builder = Response::builder()
            // TODO: this unwrap_or_default() is sloppy
            .status(status_code.parse::<StatusCode>().unwrap_or_default());

        let headers = builder.headers_mut().expect("what can possibly go wrong?");
        let header_list = result.get_item(1).cast_as::<PyList>()?;
        for pair in header_list.iter() {
            let tuple = pair.cast_as::<PyTuple>()?;
            let key: String = tuple.get_item(0).extract()?;
            let value: String = tuple.get_item(1).extract()?;
            headers.insert(
                HeaderName::from_bytes(key.as_bytes()).expect("what can possibly go wrong?"),
                HeaderValue::from_bytes(value.as_bytes()).expect("what can possibly go wrong?"),
            );
        }

        let data: Vec<u8> = result.get_item(2).extract()?;
        let resp = builder
            .header("server", "razorbird/0.2.0")
            .body(Body::from(data))
            .expect("this ought to work");

        Ok(resp)
    }

}

#[derive(Clone)]
struct AppServer {
    app: PyObject,
}

impl AppServer {
    pub async fn handle(&self, req: Request<Body>) -> Result<Response<Body>, hyper::Error> {
        let (parts, body) = req.into_parts();
        let bytes = hyper::body::to_bytes(body).await?;

        let gil = Python::acquire_gil();
        let py = gil.python();
        let received_signal: bool;
        unsafe {
            received_signal = PyErr_CheckSignals() != 0;
        }
        if received_signal {
            // TODO: this is horrible and obviously needs improvement.
            process::exit(1);
        }

        let protocol = match parts.version {
            Version::HTTP_09 => "HTTP/0.9",
            Version::HTTP_10 => "HTTP/1.0",
            Version::HTTP_11 => "HTTP/1.1",
            Version::HTTP_2 => "HTTP/2.1",
            Version::HTTP_3 => "HTTP/3.1",
            _ => "HTTP/1.0",
        };

        // WSGI environ
        let environ = [
            ("PATH_INFO", parts.uri.path()),
            ("QUERY_STRING", parts.uri.query().unwrap_or("")),
            ("SERVER_PROTOCOL", protocol),
            ("REQUEST_METHOD", parts.method.as_str()),
        ].into_py_dict(py);

        let mut headers: HashMap<String, String> = HashMap::new();
        for (header_name, header_value) in parts.headers.iter() {
            let name = header_name.as_str()
                .to_string()
                .replace("-", "_")
                .to_uppercase();
            let special_case = header_name == CONTENT_LENGTH || header_name == CONTENT_TYPE;
            let cgi_name = if special_case {name} else {format!("HTTP_{}", name)};
            let value = header_value.to_str().unwrap().to_string();
            headers.insert(cgi_name, value);
        }
        let headers_dict = headers.into_py_dict(py);

        let result = self.app.call1(py, (environ, headers_dict, bytes.as_ref()));
        match result {
            Err(_) => Ok( internal_server_error() ),
            Ok(wsgi_resp) => match from_wsgi_response(py, wsgi_resp) {
                Err(_) => Ok( internal_server_error() ),
                Ok(resp) => Ok(resp),
            },
        }
    }
}

async fn serve(app: PyObject) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let app_server = AppServer {app: app};
    let make_svc = make_service_fn(move |_conn| {
        let app_server = app_server.clone();
        async move {
            Ok::<_, Infallible>(
                service_fn(move |req| {
                    let app_server = app_server.clone();
                    async move {
                        app_server.handle(req).await
                    }
                }))
        }
    });

    let addr = ([127, 0, 0, 1], 8000).into();
    let server = Server::bind(&addr).serve(make_svc);

    println!("Listening on http://{}", addr);

    server.await?;

    Ok(())
}

#[pyfunction]
fn run_tokio(app: PyObject) -> usize {
    let mut basic_rt = runtime::Builder::new()
        .basic_scheduler()
        .enable_all()
        .build()
        .expect("this should work");

    basic_rt
        .block_on(async {
            serve(app).await
        })
        .expect("this should work");

    0
}

#[pymodule]
fn razorbird(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(run_tokio))?;

    Ok(())
}
