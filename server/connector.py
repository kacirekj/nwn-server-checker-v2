import constant
import requests
import re


def get_nwn_server_players_count(ip, port):
    url = constant.NWN_CHECKER_URL.replace('${IP}', ip).replace('${PORT}', str(port))
    response = requests.get(url)

    try:
        groups = re.findall(constant.NWN_CHECKER_URL_PLAYER_COUNT_REGEX, response.text)
        count = groups[0][constant.NWN_CHECKER_REGEX_PLAYER_COUNT_GROUP]
    except Exception as e:
        groups = re.findall(constant.NWN_CHECKER_URL_SERVER_OFFLINE_REGEX, response.text)
        if len(groups) > 0:
            count = 0
        else:
            raise e

    return int(count)