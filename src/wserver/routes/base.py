from flask import Flask, Blueprint, make_response

base_bp = Blueprint('base', __name__)


@base_bp.route('/robots.txt')
def robots_txt():
    response = make_response("User-Agent: *\nDisallow: /\n")
    response.headers["Content-Type"] = "text/plain"
    return response
