STATIC_FILE_SUFFIXES = ('.js', '.html', '.css', '.png', '.svg', '.jpg')
WEB_DIR = '../web'
WEB_ASSET_DIR = WEB_DIR + '/asset'
DATA_DIR = '../data'
NWN_CHECKER_URL = 'https://iscandar.ch/server.php?ip=${IP}&port=${PORT}&template=black&font=classic'
NWN_CHECKER_URL_PLAYER_COUNT_REGEX = r'(.*?)(Players.*?>)(.*?)(\/)(.*?)(<\/)'
NWN_CHECKER_URL_SERVER_OFFLINE_REGEX = r'(.*)(Server.*?is offline)(.*)'
NWN_CHECKER_REGEX_PLAYER_COUNT_GROUP = 2
