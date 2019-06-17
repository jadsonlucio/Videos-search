from flask import Blueprint
from flask import render_template
from flask import request, jsonify

from videos_search.src import core

bp = Blueprint("routes", __name__, url_prefix = "/v1")

@bp.route("/videos/all/" , methods=["GET"])
def all():
    lista = core.all_videos()
    return jsonify(lista)

@bp.route("videos/search/<text>/")
def search(text):
    lista = core.search_videos(text)
    return jsonify(lista)