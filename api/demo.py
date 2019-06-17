from flask import Flask

from videos_search import settings
from videos_search.routes import bp

from videos_search.settings import DEBUG

STATIC_FOLDER = './videos_search/static'
TEMPLATE_FOLDER = './videos_search/templates/'

api = Flask(__name__, static_folder = STATIC_FOLDER, template_folder = TEMPLATE_FOLDER)
api.register_blueprint(bp)


if __name__ == "__main__":
    api.run(debug = DEBUG)
    