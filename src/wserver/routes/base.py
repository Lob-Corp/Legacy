from flask import Blueprint, make_response

base_bp = Blueprint('base', __name__)


@base_bp.route('/robots.txt')
def robots_txt():
   raise NotImplementedError("Route /robots.txt not implemented yet")
