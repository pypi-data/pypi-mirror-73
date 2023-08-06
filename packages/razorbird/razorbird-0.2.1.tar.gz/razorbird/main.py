import argparse
import importlib

from .wsgi import Server


def import_app(module_name, callables):
    module = importlib.import_module(module_name)
    for name in callables[:-1]:
        app = getattr(module, name, None)
        if app:
            return app

    return getattr(module, callables[-1])


def run():
    parser = argparse.ArgumentParser(
        description='Razorbird prototype WSGI server (Rust Hyper+PyO3)')
    parser.add_argument(
        'module', help='module containing the WSGI app')
    parser.add_argument(
        '--callables', help='WSGI callables to try (default: %(default)s)',
        default='application,app,api')

    args = parser.parse_args()

    wsgi_app = import_app(args.module, args.callables.split(','))
    Server(wsgi_app).run()
