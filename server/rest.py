import dataclasses
from __main__ import app
from dataclasses import asdict

import repository
import util
from flask import request
import mapper


# Module infos


@app.get('/api/module-infos')
def get_module_infos():
    ids = request.args.getlist('ids[]')
    name = request.args.get('name')
    results = repository.get_module_infos(ids, name)
    return [asdict(result) for result in results]


@app.post('/api/module-infos')
def upsert_module_infos():
    module_infos = mapper.to_module_infos(request.json)
    results = repository.upsert_module_infos(module_infos)
    return [asdict(result) for result in results]


# Module presence


@app.get('/api/module-presences')
def get_module_presences():
    ids = request.args.getlist('ids[]')
    module_info_id = request.args.get('module_info_id')
    results = repository.get_module_presences(ids, module_info_id)
    return [asdict(result) for result in results]


@app.post('/api/module-presences')
def upsert_module_presences():
    ids = request.args.getlist('ids[]')
    module_info_id = request.args.get('module_info_id')
    results = repository.get_module_presences(ids, module_info_id)
    return [asdict(result) for result in results]
