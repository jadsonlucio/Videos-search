import os
import json
import firebase_admin
from firebase_admin import credentials


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if "DEPLOY" in os.environ.keys():
    DEPLOY = True
else:
    DEPLOY = False
    _credentials = json.load(open(BASE_DIR+"/credentials.json","r"))

DEBUG = not DEPLOY

if DEPLOY:
    pass
else:
    DEPLOY = False
    firebase_credentials = _credentials["firebase"]


CRED = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(CRED, {"databaseURL": 'https://videos-search-bc4f6.firebaseio.com'})

#scrape config 
MAX_SCRAPED_VIDEOS = 2