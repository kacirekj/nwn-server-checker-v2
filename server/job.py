import datetime
from __main__ import scheduler, scoped_factory
import service
from datetime import timedelta

import repository
import connector
import util
import constant
from model import ModulePresence, ModuleInfo


@scheduler.task('cron', minute=constant.NWN_CHECKER_URL_INTERVAL_CRON_PER_HOUR)
def update_module_presences():
    module_infos = repository.get_module_infos()
    for module_info in module_infos:

        # Load players online

        try:
            count = connector.get_nwn_server_players_count(module_info.ip, module_info.port)
        except Exception as e:
            print(f"Can't parse response for {module_info}")
            continue

        # Update Module info

        session = scoped_factory()

        module_info.players = count
        module_info.updated = datetime.datetime.utcnow()

        repository.upsert_module_infos([module_info])

        print(f"Updated {module_info.name} players count to {module_info.players}.")

        # Load latest Module presence

        timestamp_min = datetime.datetime.utcnow() - timedelta(seconds=int(constant.NWN_CHECKER_URL_INTERVAL_UPDATE_DB_SECONDS))
        recent_presences = repository.get_module_presences(module_info_id=module_info.id, timestamp_min=timestamp_min)
        if len(recent_presences) > 0:
            recent_presence = recent_presences[0]
        else:
            recent_presence = None

        # Decide if we need to update Module Presence

        is_db_update = False
        if not recent_presence:
            is_db_update = True
            print(f"Presence for {module_info.name} will be updated because there isn't any since {timestamp_min.isoformat()}")
        elif count > recent_presence.players:
            is_db_update = True
            print(f"Presence for {module_info.name} will be updated because current players {count} is greater that previous {recent_presence.players}")
        else:
            print(f"Presence for {module_info.name} will be not updated because current is {count} and before {(datetime.datetime.utcnow() - timestamp_min).total_seconds() / 60} minutes there was {recent_presence.players}")
        if not is_db_update:
            session.commit()
            continue

        # Update module presence

        if recent_presence:
            recent_presence.players = count
            recent_presence.timestamp = datetime.datetime.utcnow()
        else:
            recent_presence = ModulePresence(
                module_info_id=module_info.id,
                timestamp=datetime.datetime.utcnow(),
                players=count
            )

        repository.upsert_properties([recent_presence])

        print(f'Updated presence: {recent_presence}')
        session.commit()

        # Update chart png

        module_presences = repository.get_module_presences(module_info_id=module_info.id)
        chart_bytes = util.plot_chart_to_bytes(module_info, module_presences)

        with open(f'{constant.WEB_ASSET_DIR}/{module_info.name}-chart.png', 'wb') as file:
            file.write(chart_bytes)


@scheduler.task('interval', seconds=10)
def reload_properties():
    service.reload_properties()
