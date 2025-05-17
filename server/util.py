import io
import string
from datetime import date, datetime, timedelta
from json import JSONEncoder
import random
from typing import List

import matplotlib
import matplotlib.dates as md
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from matplotlib.transforms import interval_contains

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


def plot_chart_to_bytes(module_info: ModuleInfo, module_presences: List[ModulePresence], since: datetime = None):
    matplotlib.use('Agg')  # Use non-GUI backend

    # Truncate presences by date if needed

    if since is not None:
        module_presences = [presence for presence in module_presences if presence.timestamp >= since]

    # Calculate

    dates = [module_presence.timestamp for module_presence in module_presences]
    players_count = [module_presence.players for module_presence in module_presences]

    # Calculate averages per day

    players_count_date_map = {}

    for p in module_presences:
        date = p.timestamp.date()
        if date not in players_count_date_map:
            players_count_date_map[date] = []
        players_count_date_map[date].append(p.players)

    avg_players_counts = []

    for date, items in players_count_date_map.items():
        avg = sum(items) / len(items)
        for item in items:
            avg_players_counts.append(avg)

    # Add same starting date so charts are comparable

    if since is None:
        dates.insert(0, datetime(2024,12,29,12,12,12,12))
    else:
        dates.insert(0, since.replace(hour=0, minute=0, second=0, microsecond=0))
    players_count.insert(0, 0)
    avg_players_counts.insert(0, 0)



    plt.figure(figsize=(19.2, 10.8*0.75))
    # plt.suptitle(module_info.name, fontsize=36)
    plt.xlabel("Date (UTC)", fontsize=26)
    plt.ylabel("Players (Peak and Average)", fontsize=26)
    plt.xticks(fontsize=24, rotation=45)
    plt.yticks(fontsize=24)
    plt.grid()
    plt.subplots_adjust(bottom=0.25)
    plt.gca().xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
    plt.tight_layout()

    # Set X axis label frequency to each 2nd monday

    if (max(dates) - min(dates)).days < 28 * 3:
        interval = 1
    else:
        interval = 4
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MONDAY, interval=interval, tz="UTC"))

    # Set X axis vertical line frequency to each monday

    all_mondays = pd.date_range(start=min(dates).replace(hour=0, minute=0, second=0, microsecond=0), end=max(dates).replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=7), freq='W-MON', tz="UTC")
    for monday in all_mondays:
        plt.axvline(monday, color='lightgray', linestyle='-', linewidth=0.5)

    # Plot lines

    plt.plot(dates, players_count, label="Ab", linewidth=0.4)
    plt.plot(dates, avg_players_counts, label="CD", linewidth=2.5)

    # Plot single big point with latest playuers count maximum

    plt.scatter([max(dates)], [players_count[len(players_count)-1]], color='blue', s=200, zorder=5, marker='x', linewidths=3)
    # plt.scatter(dates, avg_players_counts, color='orange', s=200, zorder=5, marker='_', linewidths=1)
    plt.scatter([max(dates)], [avg_players_counts[len(avg_players_counts)-1]], color='red', s=200, zorder=5, marker='x', linewidths=3)

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', transparent=True)
    plt.close()
    return img_buf.getvalue()


def generate_random_lowercase_string(length):
    return ''.join(random.choices(string.ascii_uppercase, k=length))


def increment_page_visits_route_if_unique(request, respomse):
    if not request.cookies.get('user_id'):
        response.set_cookie('user_id', 'unique_user_id_123')  # Nastavíme unikátní ID pro uživatele
    return response
