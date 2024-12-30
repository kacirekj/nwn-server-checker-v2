import datetime
from __main__ import scheduler, scoped_factory
import importlib
import repository
import connector
import util
import constant
from server.model import ModulePresence


@scheduler.task('interval', seconds=1)
def update_module_presences():
    print("Do job")
    module_infos = repository.get_module_infos()
    for module_info in module_infos:
        try:
            count = connector.get_nwn_server_players_count(module_info.ip, module_info.port)
        except Exception as e:
            print(f"Can't parse response for {module_info}")
            continue
        module_presence = ModulePresence(
            module_info_id=module_info.id,
            timestamp=datetime.datetime.utcnow(),
            players=count
        )
        session = scoped_factory()
        repository.upsert_properties([module_presence])
        session.commit()
        print(module_presence)

        module_presences = repository.get_module_presences(module_info_id=module_info.id)
        chart_bytes = util.plot_chart_to_bytes(module_info, module_presences)

        with open(f'{constant.WEB_ASSET_DIR}/{module_info.name}-chart.png', 'wb') as file:
            file.write(chart_bytes)


@scheduler.task('interval', seconds=10)
def reload_properties():
    properties = repository.get_property()
    constant_module = importlib.import_module('constant')
    for property in properties:
        setattr(constant_module, property.key, property.value)
