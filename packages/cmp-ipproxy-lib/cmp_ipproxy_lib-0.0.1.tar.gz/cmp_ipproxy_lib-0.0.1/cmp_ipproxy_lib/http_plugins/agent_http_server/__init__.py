import inspect
import logging
import traceback

logger = logging.getLogger(__name__)


def install():
    # noinspection PyBroadException
    try:
        from http.server import BaseHTTPRequestHandler

        _handle = BaseHTTPRequestHandler.handle

        def _agent_handle(handler: BaseHTTPRequestHandler):
            clazz = handler.__class__
            if 'werkzeug.serving.WSGIRequestHandler' == ".".join([clazz.__module__, clazz.__name__]):
                wrap_werkzeug_request_handler(handler)
            else:
                wrap_default_request_handler(handler)
            _handle(handler)

        BaseHTTPRequestHandler.handle = _agent_handle

    except Exception:
        logger.warning('failed to install plugin %s', __name__)
        traceback.print_exc()


def wrap_werkzeug_request_handler(handler):
    """
    Wrap run_wsgi of werkzeug.serving.WSGIRequestHandler to add skywalking instrument code.
    """
    _run_wsgi = handler.run_wsgi

    def _wrap_run_wsgi():
        return _run_wsgi()

    handler.run_wsgi = _wrap_run_wsgi


def wrap_default_request_handler(handler):
    http_methods = ('GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH')
    for method in http_methods:
        _wrap_do_method(handler, method)


def _wrap_do_method(handler, method):
    if hasattr(handler, 'do_' + method) and inspect.ismethod(getattr(handler, 'do_' + method)):
        _do_method = getattr(handler, 'do_' + method)

        def _sw_do_method():
            _do_method()

        setattr(handler, 'do_' + method, _sw_do_method)
