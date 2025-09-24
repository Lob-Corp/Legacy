from flask import Flask, Blueprint, make_response

base_bp = Blueprint('base', __name__)

# Route pour robots.txt
@base_bp.route('/robots.txt')
def robots_txt():
    # Correspond à robots_txt printer_conf
    response = make_response("User-Agent: *\nDisallow: /\n")
    response.headers["Content-Type"] = "text/plain"
    return response
