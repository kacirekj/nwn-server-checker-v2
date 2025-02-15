import datetime
import json
import os
import signal
from dataclasses import asdict

from flask import request, send_file

import context
import mapper
import repository
import validator
import job


# Captcha


@context.app.get('/api/captcha')
def get_captcha():
    data, md5hash = validator.create_captcha()
    return send_file(
        data,
        download_name=f'{md5hash}.png',
        mimetype='image/png',
    )


# Discussion


@context.app.get('/api/discussion-items')
def get_discussion_items():
    results = repository.get_discussion_items()
    return [asdict(result) for result in results]


@context.app.post('/api/discussion-items')
def create_discussion_item():
    validator.validate_captha(request)
    discussion_item = mapper.to_discussion_item(request.json)
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    discussion_item.ip = request.ip = f'{ip_address}, {user_agent}'
    result = repository.upsert_discussion_items([discussion_item])[0]
    return asdict(result)


@context.app.delete('/api/discussion-items')
def delete_discussion_items():
    validator.validate_password(request)
    ids = request.args.getlist('ids[]')
    repository.delete_discussion_items(ids)
    return ""


# Module infos


@context.app.get('/api/module-infos')
def get_module_infos():
    ids = request.args.getlist('ids[]')
    name = request.args.get('name')
    results = repository.get_module_infos(ids, name)
    return json.dumps([asdict(result) for result in results], default=str)


@context.app.post('/api/module-infos')
def upsert_module_infos():
    validator.validate_password(request)
    module_infos = mapper.to_module_infos(request.json)
    results = repository.upsert_module_infos(module_infos)
    return [asdict(result) for result in results]


@context.app.delete('/api/module-infos')
def delete_module_infos():
    validator.validate_password(request)
    ids = request.args.getlist('ids[]')
    password = request.args.getlist('password')
    repository.delete_module_info(ids)
    return ""


# Module presence


@context.app.get('/api/module-presences')
def get_module_presences():
    ids = request.args.getlist('ids[]')
    module_info_id = request.args.get('module_info_id')
    results = repository.get_module_presences(ids, module_info_id)
    return [asdict(result) for result in results]


# Property


@context.app.get('/api/properties')
def get_properties():
    keys = request.args.getlist('keys[]')
    results = repository.get_properties(keys=keys)
    return [asdict(result) for result in results]


@context.app.post('/api/properties')
def upsert_properties():
    validator.validate_password(request)
    properties = mapper.to_properties(request.json)
    results = repository.upsert_properties(properties)
    context.scoped_factory().commit()
    os.kill(os.getpid(), signal.SIGINT)
    return [asdict(result) for result in results]


# Web Visit


@context.app.post('/api/web-visits')
def increment():
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    ip_browser = f'{ip_address}, {user_agent}'
    is_unique_visit_per_day = ip_browser not in context.ip_browser_web_visitors
    web_visit = repository.get_web_visits([0])[0]
    if is_unique_visit_per_day:
        context.ip_browser_web_visitors.add(ip_browser)
        web_visit.unique24hVisitCount += 1
        web_visit.visitCount += 1
        print(f"Unique web visit from: {ip_browser}")
    else:
        web_visit.visitCount += 1
        print(f"Repeated web visit from: {ip_browser}")
    web_visit.updated = datetime.datetime.now(datetime.timezone.utc).isoformat()
    web_visit = repository.upsert_web_visits([web_visit])[0]
    return asdict(web_visit)


@context.app.get('/api/web-visits')
def get_web_visits():
    web_visit = repository.get_web_visits([0])[0]
    return asdict(web_visit)


@context.app.post('/api/re-render')
def re_render():
    print("Re-render trigered")
    job.update_module_presences()
    return ""

