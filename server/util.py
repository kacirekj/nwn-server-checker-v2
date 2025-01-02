import io
import string
from datetime import date, datetime
from json import JSONEncoder
import random
from typing import List

import matplotlib
import matplotlib.dates as md
import matplotlib.pyplot as plt

from model import ModulePresence, ModuleInfo


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date) or isinstance(obj, datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def plot_chart_to_bytes(module_info: ModuleInfo, module_presences: List[ModulePresence]):
    matplotlib.use('Agg')  # Use non-GUI backend

    dates = [module_presence.timestamp for module_presence in module_presences]
    players_count = [module_presence.players for module_presence in module_presences]

    # Add same starting date so charts are comparable

    dates.insert(0, datetime(2024,12,29,12,12,12,12))
    players_count.insert(0, 0)

    plt.figure(figsize=(19.2, 10.8*0.75))
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


def generate_random_lowercase_string(length):
    return ''.join(random.choices(string.ascii_uppercase, k=length))


def increment_page_visits_route_if_unique(request, respomse):
    if not request.cookies.get('user_id'):
        response.set_cookie('user_id', 'unique_user_id_123')  # Nastavíme unikátní ID pro uživatele
    return response
