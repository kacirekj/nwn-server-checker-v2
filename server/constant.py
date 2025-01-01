STATIC_FILE_SUFFIXES = ('.js', '.html', '.css', '.png', '.svg', '.jpg')
WEB_DIR = '../web'
WEB_ASSET_DIR = WEB_DIR + '/asset'
DATA_DIR = '../data'
NWN_CHECKER_URL = 'https://iscandar.ch/server.php?ip=${IP}&port=${PORT}&template=black&font=classic'
NWN_CHECKER_URL_INTERVAL_CRON_PER_HOUR = "*/1"
NWN_CHECKER_URL_INTERVAL_UPDATE_DB_SECONDS = "900"
NWN_CHECKER_URL_PLAYER_COUNT_REGEX = r'(.*?)(Players.*?>)(.*?)(\/)(.*?)(<\/)'
NWN_CHECKER_URL_SERVER_OFFLINE_REGEX = r'(.*)(Server.*?is offline)(.*)'
NWN_CHECKER_URL_PLAYER_COUNT_REGEX_GROUP_0_X = "2"
PASSWORD_SHA_3_512 = '08e22284e5d774c9579927465c41ae5d4f445aadee7ce15862b09c43cd5551af77e6110913f413ff3c193c3ad80061c5919a3693f5b96f321e1e12929dfdc41b'
ADMIN_PASSWORD = ""
CAPTCHA_SEED = "tajnyseed"

with open(f'{DATA_DIR}/adminpassword.txt', 'r') as file:
    ADMIN_PASSWORD = file.readline()
