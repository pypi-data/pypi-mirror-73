import configparser
from aito.common.generic_utils import ROOT_PATH
parser = configparser.ConfigParser()
with (ROOT_PATH / '.circleci' / 'credentials').open() as f:
    config = parser.read_file(f)

print(parser.has_section('ok'))
print(parser.has_section('first profile'))
# print(parser.get('ok', 'second'))
print(parser.get('first profile', 'second'))
