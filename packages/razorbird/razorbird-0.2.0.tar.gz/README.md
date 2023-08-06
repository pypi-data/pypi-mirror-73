# Razorbird

Razorbird is a WSGI application server for Python.
Well, or just me trying to learn some Rust.

Needless to say, do not use it for anything serious.
Apart from being hampered by my poor Rust skills, it has serious flaws:
* Request is buffered in memory without any restrictions.
* Response is not streamed but concatenated to a byte string.
* Single process/single threaded cause I haven't found out how to make Tokio
  threads work with PyO3.
* The server is always (hardcoded) bound to http://127.0.0.1:8000 .
* Signal handling is an example of horrible duct taping.

Patches welcome!

## Installation

I have been lazy to upload wheels, so you'll need access to a functional Rust
environment with `cargo`, `rustc` etc. Then just install from sdist:
```
$ pip install razorbird
```

## Usage

Don't.

Well, if you'd really like to give it a spin, just run
```
$ razorbird your.module.name
```

``your.module.name`` should contain a WSGI callable named `application`, `app`
or `api`, but that is customizable from the command line.
