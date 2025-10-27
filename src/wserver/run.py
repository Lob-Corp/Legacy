"""Run the Flask application."""

from wserver import create_app
from wserver.settings import settings

app = create_app()

if __name__ == "__main__":

    is_ssl_configured = settings.ssl_cert_path and settings.ssl_key_path
    if settings.ssl_enabled and is_ssl_configured:
        app.run(
            host=settings.host,
            port=settings.port,
            debug=settings.debug,
            ssl_context=(
                settings.ssl_cert_path,
                settings.ssl_key_path
            )
        )
    else:
        app.run(
            host=settings.host,
            port=settings.port,
            debug=settings.debug
        )
