import datetime
import io
from datetime import date
from typing import List
from zoneinfo import ZoneInfo
import hashlib

import constant
import matplotlib.dates as md
import matplotlib.pyplot as plt
from flask.json import JSONEncoder

from server.model import ModulePresence, ModuleInfo


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def plot_chart_to_bytes(module_info: ModuleInfo, module_presences: List[ModulePresence]):
    dates = [module_presence.timestamp for module_presence in module_presences]
    players_count = [module_presence.players for module_presence in module_presences]

    fig = plt.figure(figsize=(19.2, 10.8*0.75))
    # plt.suptitle(module_info.name, fontsize=36)
    plt.xlabel("Date time (UTC)", fontsize=28)
    plt.ylabel("Players online", fontsize=28)
    plt.xticks(fontsize=24, rotation=45)
    plt.yticks(fontsize=24)
    plt.grid()
    plt.subplots_adjust(bottom=0.25)
    plt.gca().xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d %H:%M'))
    plt.tight_layout()
    plt.plot(dates, players_count, linewidth=0.8)

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', transparent=True)

    return img_buf.getvalue()
