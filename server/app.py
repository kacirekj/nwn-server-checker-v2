import json
import os

from flask import Flask, send_from_directory, request
from flask_apscheduler import APScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import constant
import context
import util

# Init Flask

os.environ['TZ'] = 'Europe/Prague'
context.app = Flask(__name__, )
context.app.json_encoder = util.CustomJSONEncoder

# context.app.config['JSON_SORT_KEYS'] = False
# context.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


# Init Sql Alchemy

context.engine = create_engine(f"sqlite:///{constant.DATA_DIR}/sqlite.db")
context.session_factory = sessionmaker(bind=context.engine)
context.scoped_factory = scoped_session(context.session_factory)

# Init Scheduler

import service

service.reload_properties()
context.scheduler = APScheduler()
context.scheduler.init_app(context.app)
context.scheduler.start()

import job
import rest


@context.app.route('/')
def get_index():
    return send_from_directory(constant.WEB_DIR, 'index.html')


@context.app.route('/<path:text>')
def get_index_with(text: str):
    if text == '/':
        return send_from_directory(constant.WEB_DIR, 'index.html')
    elif text.startswith('/api'):
        pass
    elif text.endswith(constant.STATIC_FILE_SUFFIXES):
        web_file = text.split('web/')[1]
        return send_from_directory(constant.WEB_DIR, web_file)
    else:
        return send_from_directory(constant.WEB_DIR, 'index.html')  # Should have 404 not found


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
    if not hasattr(e, 'code'):
        response = {
            "error": 'Unknown error',
            "message": str(e),
            "status_code": 500
        }
    else:
        response = {
            "error": e.name,
            "message": e.description,
            "status_code": e.code
        }
    return json.dumps(response), response['status_code']


application = context.app  # gunicorn needs "application" variable

if __name__ == '__main__':
    context.app.run(debug=True, host='0.0.0.0', port=8080, use_reloader=False)
    context.app.shut
