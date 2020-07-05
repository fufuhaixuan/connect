# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__version__ = '0.0.1'
SAMPLE_USAGE = 'Set a new config: connect -cmd set -n myname -host username@host[:port] -pwd mypassword \n' \
               'Delete a config:  connect -cmd delete -n myname\n' \
               'Update a config:  connect -cmd update -n myname -update password:newpassword'
LOGIN_WITH_PASSWORD = 0
LOGIN_WITH_KEY = 1
DEFAULT_PORT = 22
SHOW_CONNECT_LIST_SPACE_LENGTH = 16
SHOW_CONNECT_LIST_SYMBOL = 'e'
CONFIG_FILE = 'config.ini'
CMD_SET = 'set'
CMD_DEL = 'delete'
CMD_UPDATE = 'update'

CONNECT_WITH_PASSWORD = 'sshpass -p {password} ssh -p {port} {user_name}@{host} -o StrictHostKeyChecking=no'
CONNECT_WIT_KEY = 'ssh -i {key_path} {user_name}@{host}'
NORMAL_CONNECT_ITEMS_STR = '[{index}] {name:<{len}}{host}'
EXIT_CONNECT_SHOW_LIST = '[{symbol}] {name:<{len}}'
TIME_STF =  '%a, %d %b %Y %H:%M:%S +%f'

SECTION_ITEM_OPTIONS = ['user_name', 'host', 'port', 'login_type', 'password', 'key_path']
SECTION_ITEM_DICT = dict((key, None) for key in SECTION_ITEM_OPTIONS)
SECTION_ITEM_OPTIONS_STR = ', '.join(SECTION_ITEM_OPTIONS)
CAN_NOT_UPDATE_OPTIONS = ['login_type']
CAN_UPDATE_OPTIONS = [key for key in SECTION_ITEM_OPTIONS if key not in CAN_NOT_UPDATE_OPTIONS]
CAN_UPDATE_OPTIONS_STR = ', '.join(CAN_UPDATE_OPTIONS)