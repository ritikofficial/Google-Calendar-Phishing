import flask
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

import os
from os.path import join, dirname

from datetime import datetime

#write client secret file
def write_client_secret():
    print('writing client secret file')
    file = open(CLIENT_SECRET_FILE, 'w')
    file.write(os.environ['CLIENT_SECRET'])
    file.close()


write_client_secret() 

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ['FLASK_SECRET_KEY']
db = SQLAlchemy(app)
