# Imports
import json
import logging
from http.client import HTTPException

from flask_apscheduler import APScheduler
from flask import Flask, send_from_directory, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Component imports

import initdb
import util
from constant import STATIC_FILE_SUFFIXES, WEB_DIR, DATA_DIR
from util import CustomJSONEncoder

# Init Flask

app = Flask(__name__, )
app.json_encoder = CustomJSONEncoder
# app.config['JSON_SORT_KEYS'] = False
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Init SqlAclhemy

engine = create_engine(f"sqlite:///{DATA_DIR}/sqlite.db")
session_factory = sessionmaker(bind=engine)
scoped_factory = scoped_session(session_factory)

import repository
import rest
import constant
import service

# Init Scheduler

service.reload_properties()
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

import job


@app.route('/')
def get_index():
    return send_from_directory(WEB_DIR, 'index.html')


@app.route('/<path:text>')
def get_index_with(text: str):
    if text == '/':
        return send_from_directory(WEB_DIR, 'index.html')
    elif text.startswith('/api'):
        pass
    elif text.endswith(STATIC_FILE_SUFFIXES):
        web_file = text.split('web/')[1]
        return send_from_directory(WEB_DIR, web_file)
    else:
        return send_from_directory(WEB_DIR, 'index.html')  # Should have 404 not found


@app.teardown_request
def teardown_request(exception):
    if '/api' not in request.path:
        return
    print('Teardown')
    session = scoped_factory()
    if not exception:
        print('Commit')
        session.commit()
    else:
        print('Rollback')
        session.rollback()
    session.close()


@app.errorhandler(Exception)
def handle_http_exception(e):
    response = {
        "error": e.name,
        "message": e.description,
        "status_code": e.code
    }
    return json.dumps(response), e.code


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000, use_reloader=False)
