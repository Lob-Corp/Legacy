import pytest
from unittest.mock import Mock
import io
import wserver


# -------------------
# Tests pour f (serveur principal)
# -------------------

def test_run_server_accepts_arguments():
    logger = lambda lvl, msg: None
    handler = lambda conn, path, query: None
    assert wserver.run_server(logger, None, 8080, 30, None, handler) is None


def test_run_server_invalid_port():
    logger = lambda lvl, msg: None
    handler = lambda conn, path, query: None
    with pytest.raises(ValueError):
        wserver.run_server(logger, None, -1, 30, None, handler)


# -------------------
# Tests pour close_connection
# -------------------
def test_close_connection_runs_without_error():
    wserver.close_connection()


# -------------------
# Tests pour print_string / header
# -------------------
# def test_print_string_outputs(monkeypatch):
#     buffer = io.StringIO()
#     monkeypatch.setattr("sys.stdout", buffer)
#     wserver.print_string("Bonjour")
#     assert "Bonjour" in buffer.getvalue()


# def test_header_prints_correct_format(monkeypatch):
#     buffer = io.StringIO()
#     monkeypatch.setattr("sys.stdout", buffer)
#     wserver.header("Content-Type: text/html")
#     assert "Content-Type" in buffer.getvalue()


# -------------------
# Tests pour wflush
# -------------------
# def test_wflush_flushes(monkeypatch):
#     buffer = io.StringIO()
#     monkeypatch.setattr("sys.stdout", buffer)
#     wserver.print_string("Test")
#     wserver.wflush()
#     assert buffer.getvalue() == "Test"


# -------------------
# Tests pour http & redirect
# -------------------
# def test_http_writes_status(monkeypatch):
#     buffer = io.StringIO()
#     monkeypatch.setattr("sys.stdout", buffer)
#     wserver.http(200)
#     assert "200" in buffer.getvalue()


# def test_http_redirect_temporarily(monkeypatch):
#     buffer = io.StringIO()
#     monkeypatch.setattr("sys.stdout", buffer)
#     wserver.http_redirect_temporarily("/new")
#     assert "/new" in buffer.getvalue()


# -------------------
# Tests pour get_request_and_content
# -------------------
# def test_get_request_and_content_parses():
#     stream = iter("GET /index.html?x=1\r\n\r\nbody")
#     req, content = wserver.get_request_and_content(stream)
#     assert isinstance(req, list)
#     assert "GET" in req[0]
#     assert isinstance(content, str)

