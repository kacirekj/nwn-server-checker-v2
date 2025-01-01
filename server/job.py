import datetime
import statistics
from datetime import timedelta

import connector
import constant
import context
import repository
import service
import util
from model import ModulePresence


@context.scheduler.task('cron', minute=constant.NWN_CHECKER_URL_INTERVAL_CRON_PER_HOUR)
def update_module_presences():
    module_infos = repository.get_module_infos()
    for module_info in module_infos:

        # Load players online

        try:
            count = connector.get_nwn_server_players_count(module_info.ip, module_info.port)
        except Exception as e:
            print(f"Can't parse response for {module_info}")
            continue

        if module_info.players > 2 and count - module_info.players > 40:
            print(f"There is nonsense presence {count} while previous was {module_info.players} for {module_info.name}.")
            continue

        # Update Module info

        session = context.scoped_factory()

        module_info.players = count
        module_info.updated = datetime.datetime.now(datetime.timezone.utc)

        repository.upsert_module_infos([module_info])
        session.commit()

        print(f"Updated {module_info.name} players count to {module_info.players}.")

        # Load latest Module presence

        timestamp_min = datetime.datetime.now(datetime.timezone.utc) - timedelta(seconds=int(constant.NWN_CHECKER_URL_INTERVAL_UPDATE_DB_SECONDS))
        recent_presences = repository.get_module_presences(module_info_id=module_info.id, timestamp_min=timestamp_min)
        if len(recent_presences) > 0:
            recent_presence = recent_presences[0]
        else:
            recent_presence = None

        # Decide if we need to update Module Presence

        if not recent_presence:
            is_db_update = True
            print(f"Presence for {module_info.name} will be updated because there isn't any since {timestamp_min.isoformat()}")
        elif count > recent_presence.players:
            is_db_update = True
            print(f"Presence for {module_info.name} will be updated because current players {count} is greater that previous {recent_presence.players}")
        else:
            is_db_update = False
            print(f"Presence for {module_info.name} will be not updated because current is {count} and before {(datetime.datetime.now(datetime.timezone.utc) - recent_presence.timestamp.replace(tzinfo=datetime.timezone.utc)).total_seconds() / 60} minutes there was {recent_presence.players}")
        if not is_db_update:
            session.commit()
            continue

        # Update module presence

        if recent_presence:
            recent_presence.players = count
            recent_presence.timestamp = datetime.datetime.now(datetime.timezone.utc)
        else:
            recent_presence = ModulePresence(
                module_info_id=module_info.id,
                timestamp=datetime.datetime.now(datetime.timezone.utc),
                players=count
            )

        repository.upsert_module_presences([recent_presence])

        print(f'Updated presence: {recent_presence}')
        session.commit()

        # Update chart png

        module_presences = repository.get_module_presences(module_info_id=module_info.id)
        chart_bytes = util.plot_chart_to_bytes(module_info, module_presences)

        with open(f'{constant.WEB_ASSET_DIR}/{module_info.name}-chart.png', 'wb') as file:
            file.write(chart_bytes)


@context.scheduler.task('interval', seconds=10)
def reload_properties():
    service.reload_properties()








