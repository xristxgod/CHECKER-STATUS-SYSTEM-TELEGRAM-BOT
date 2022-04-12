from logging import getLogger
from os import environ


logger = getLogger(__name__)

TOKEN = environ.get('TOKEN')
ADMIN_IDS = environ.get('ADMIN_IDS').split(',')
TEST_FILE = environ.get('TEST_FILE')


DOMAINS = {x: y for x, y in environ.items() if x.startswith('domain_')}

if DOMAINS == {}:
    DOMAINS = {
        'domain_bank': '',
        'domain_bsc_api': '',
        'domain_btc_api': '',
        'domain_tron_api': '',
    }
