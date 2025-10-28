from flask import Blueprint, send_from_directory, abort
from pathlib import Path

images_bp = Blueprint('images', __name__)


@images_bp.route('/images/<path:filename>')
def images_route(filename):
    """
    Serve image files used by GeneWeb.
    Returns 404 if not found.
    """
    repo_root = Path(__file__).resolve().parents[3]
    repo_root = repo_root / "src" / "wserver" / "static" / "images"
    filename_path = Path(filename)
    if filename_path.is_absolute() or ".." in filename_path.parts:
        abort(400)
    file_path = repo_root / filename
    if file_path.exists() and file_path.is_file():
        resp = send_from_directory(str(repo_root), filename)
        resp.cache_control.max_age = 3600
        return resp
    abort(404)
