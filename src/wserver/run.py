"""Run the Flask application."""

from wserver import create_app
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app()

host = os.environ.get("FLASK_HOST", "127.0.0.1")
port = int(os.environ.get("FLASK_PORT", 5000))


if __name__ == "__main__":
    app.run(host=host, port=port, debug=app.config["DEBUG"])

