# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import copy
import constants
import ConfigParser

config_parser = ConfigParser.ConfigParser()

__all__ = ('main', )
__author__ = 'Evoca'

CURRENT_PATH = ''
CONFIG_PATH = ''

def parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-cmd', dest='cmd', choices=['set', 'delete', 'update'], help='Your action, required')
    parser.add_argument('-update', dest='update', help='-cmd update -n name -update key:value, keys: {key}'.format(key=constants.CAN_UPDATE_OPTIONS_STR))
    parser.add_argument('-n', '--name', dest='name', help='The name of the section you want to operate on, required')
    parser.add_argument('-host', dest='host', help='username@host[:port], requierd when use \'set\'')
    parser.add_argument('-pwd', dest='password', help='password[option], option when use \'set\'')
    parser.add_argument('-idt', dest='identify', help='identify[option] key file path, option when use \'set\'')
    parser.add_argument('-v', '--version', action='store_const', const=constants.__version__, help='show version')
    parser.add_argument('-u', '--usage', action='store_const', const=constants.SAMPLE_USAGE, help='show sample usage')

    return parser.parse_args()


def show_connect_list():
    returnlist = list()
    all_sections = config_parser.sections()
    exit_symbol = constants.SHOW_CONNECT_LIST_SYMBOL
    space_len = constants.SHOW_CONNECT_LIST_SPACE_LENGTH

    print 'Select a number to connect:'
    for idx, section in enumerate(all_sections):
        items_dict = get_options(section, config_parser)
        print constants.NORMAL_CONNECT_ITEMS_STR.format(
            name=section, len=space_len, index=idx, host=items_dict['host'])
        returnlist.append((section, items_dict))
    print constants.EXIT_CONNECT_SHOW_LIST.format(symbol=exit_symbol, name='exit', len=space_len)
    print ''

    return returnlist

def get_options(section, parser=None):
    if not parser:
        parser = config_parser
        parser.read(CONFIG_PATH)

    items = parser.items(section)
    items_dict = dict((item[0], item[1]) for item in items)

    return items_dict

def connect(host_info):
    wrap_login_info(host_info)
    cmd = dispatch_connect_cmd(host_info['login_type'])
    os.system(cmd.format(**host_info))

def dispatch_connect_cmd(login_type):
    type_to_cmd_dict = {
        constants.LOGIN_WITH_PASSWORD: constants.CONNECT_WITH_PASSWORD,
        constants.LOGIN_WITH_KEY: constants.CONNECT_WIT_KEY,
    }
    return type_to_cmd_dict[int(login_type)]

def wrap_login_info(host_info):
    import datetime

    info_dict = copy.deepcopy(host_info)
    # Don't show these keys @_@
    if info_dict.has_key('name'):
        del info_dict['name']
    if info_dict.has_key('login_type'):
        del info_dict['login_type']

    for key, value in info_dict.iteritems():
        if not value:
            continue
        date_str = datetime.datetime.now().strftime(constants.TIME_STF)[:-3]
        print '[Info]: {date} [{key}]:{value}'.format(date=date_str,key=key, value=value)

def unpack_args(args):

    if not args.host:
        print '\'host\' is required, input -h to see the usage'
        sys.exit(1)
    try:
        if ':' in args.host:
            u_h, port = args.host.split(':')
        else:
            u_h, port = args.host, constants.DEFAULT_PORT
        username, host = u_h.split('@')
    except Exception as e:
        print '\'host\' is invalid. input -h to see the usage'
        sys.exit(1)

    login_type, password, identify = constants.LOGIN_WITH_PASSWORD, args.password, args.identify
    if not any([password, identify]):
        print '\'password\' and \'identify\' can not be all empty. input -h to see the usage'
        sys.exit(1)

    if args.identify:
        login_type = constants.LOGIN_WITH_KEY

    returnitem = copy.deepcopy(constants.SECTION_ITEM_DICT)
    returnitem.update(
        name=args.name,
        user_name=username,
        host=host,
        port=port,
        login_type=login_type,
        password=password,
        key_path=identify)

    return returnitem


def set_section(args):
    config = unpack_args(args)
    section = config['name']
    del config['name']

    if config_parser.has_section(section):
        print 'The configuration for {name} already exists'.format(name=section)
        sys.exit(1)

    config_parser.add_section(section)

    for option, value in config.iteritems():
        config_parser.set(section, option, value)

    with open(CONFIG_PATH, 'wb') as fb:
        config_parser.write(fb)


def delete_section(args):
    section = args.name
    config_parser.remove_section(section)

    with open(CONFIG_PATH, 'wb') as fb:
        config_parser.write(fb)

def update_section(args):
    section = args.name

    if not section:
        print '\'name\' is required. input -h to see the usage'
        sys.exit(1)

    if not config_parser.has_section(section):
        print 'The configuration for {name} does not exist'.format(name=section)
        sys.exit(1)

    option, value = None, None
    if args.update:
        try:
            option, value = args.update.split(':')
        except Exception as e:
            print 'Update parameter error. input -h to see the usage'
            sys.exit(1)

    config_parser.set(section, option, value)

    # Update login type
    item = dict(config_parser.items(section))

    if item['key_path']:
        config_parser.set(section, 'login_type', constants.LOGIN_WITH_KEY)
    else:
        config_parser.set(section, 'login_type', constants.LOGIN_WITH_PASSWORD)


    with open(CONFIG_PATH, 'wb') as fb:
        config_parser.write(fb)

def handle_cmd(args):
    cmd_to_method_dict = {
        constants.CMD_SET: set_section,
        constants.CMD_DEL: delete_section,
        constants.CMD_UPDATE: update_section
    }
    cmd_to_method_dict[args.cmd](args)

def handle_connect():
    all_sections = show_connect_list()
    sections_length = len(all_sections)
    if not all_sections:
        return
    item = None
    while True:
        try:
            _input = raw_input('> ')
            # @_@
            if _input == constants.SHOW_CONNECT_LIST_SYMBOL:
                raise KeyboardInterrupt('')
            select = int(_input)
            item = all_sections[select]
        except KeyboardInterrupt as e:
            print '\nbye!'
            sys.exit(0)
        except Exception as e:
            print 'Input valid number! {start}~{end}'.format(start=0, end=sections_length - 1)
            continue
        else:
            break
    connect(item[1])


def main():
    if sys.argv[1:]:
        args = parse_args()
        for action in [args.version, args.usage]:
            if action:
                print action
                sys.exit(0)
        handle_cmd(args)
    else:
        handle_connect()


if __name__ == '__main__':
    # Set path, config.ini must be at the same level as this script
    CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
    CONFIG_PATH = os.path.join(CURRENT_PATH, constants.CONFIG_FILE)
    config_parser.read(CONFIG_PATH)
    main()

