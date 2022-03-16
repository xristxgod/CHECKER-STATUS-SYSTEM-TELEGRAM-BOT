from logging import getLogger
from os import environ


logger = getLogger(__name__)

TOKEN = environ.get('TOKEN', '1971498893:AAFEYk6hTFUHNC5FDI7uqZEaF4-g-JORR2U')
ADMIN_IDS = environ.get('ADMIN_IDS', '853037018,702296838').split(',')
TEST_FILE = environ.get('TEST_FILE', 'stage_endpoints.json')


DOMAINS = {x: y for x, y in environ.items() if x.startswith('domain_')}
