# Imports
import json
import logging
from http.client import HTTPException
import os

from flask_apscheduler import APScheduler
from flask import Flask, send_from_directory, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Component imports

import context
import initdb
import util
from constant import STATIC_FILE_SUFFIXES, WEB_DIR, DATA_DIR
from util import CustomJSONEncoder

# Init Flask

os.environ['TZ'] = 'Europe/Prague'
context.app = Flask(__name__, )
context.app.json_encoder = CustomJSONEncoder
# context.app.config['JSON_SORT_KEYS'] = False
# context.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Init SqlAclhemy

context.engine = create_engine(f"sqlite:///{DATA_DIR}/sqlite.db")
context.session_factory = sessionmaker(bind=context.engine)
context.scoped_factory = scoped_session(context.session_factory)

import repository
import rest
import constant
import service

# Init Scheduler

service.reload_properties()
context.scheduler = APScheduler()
context.scheduler.init_app(context.app)
context.scheduler.start()

import job


@context.app.route('/')
def get_index():
    return send_from_directory(WEB_DIR, 'index.html')


@context.app.route('/<path:text>')
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


@context.app.teardown_request
def teardown_request(exception):
    if '/api' not in request.path:
        return
    print('Teardown')
    session = context.scoped_factory()
    if not exception:
        print('Commit')
        session.commit()
    else:
        print('Rollback')
        session.rollback()
    session.close()


@context.app.errorhandler(Exception)
def handle_http_exception(e):
    response = {
        "error": e.name,
        "message": e.description,
        "status_code": e.code
    }
    return json.dumps(response), e.code


application = context.app # gunicorn needs "application" variable


if __name__ == '__main__':
    context.app.run(debug=True, host='0.0.0.0', port=8080, use_reloader=False)
