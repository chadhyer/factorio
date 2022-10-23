from ast import arg
from os import environ, system, makedirs as mkdir
from sys import exit
from time import sleep
from update_settings import\
    update_server_settings,\
    update_map_gen_settings,\
    update_map_settings,\
    generate_rcon_passwd,\
    delete_temp_save,\
    generate_new_save
import logging

SCRIPTOUTPUT = environ.get('SCRIPTOUTPUT')
try:
    mkdir(SCRIPTOUTPUT)
except:
    pass
logging.basicConfig(
    filename=environ.get('LOG_FILE', f'{SCRIPTOUTPUT}/entrypoint.log'),
    level=environ.get('LOG_LEVEL', 'INFO'),
    format='%(asctime)s [%(levelname)s] - %(name)s - %(message)s'
)
logging.info('--- factorio docker-entrypoint.py ---')

# Environment Variables
SAVE_NAME = environ.get('SAVE_NAME', 'world')
PORT = environ.get('PORT', 24197)
RCON_PORT = environ.get('RCON_PORT', 25575)
BIND = environ.get('BIND', None)
LOAD_LATEST_SAVE = environ.get('LOAD_LATEST_SAVE', True)
DEBUG = environ.get('DEBUG', False)

logging.debug(
    f'''Environment Variables
    SAVE_NAME={SAVE_NAME},
    PORT={PORT},
    RCON_PORT={RCON_PORT},
    BIND={BIND},
    LOAD_LATEST_SAVE={LOAD_LATEST_SAVE},
    DEBUG={DEBUG}
    '''
)

# Envirnment Directories
FACTORIO_VOL = "/factorio"
CONFIG = environ.get('CONFIG')
DATA = environ.get('DATA')
MODS = environ.get('MODS')
TEMP = environ.get('TEMP')
SCENARIOS = environ.get('SCENARIOS')
SAVE = environ.get('SAVE')

logging.debug(
    f'''Envirnment Directories
    FACTORIO_VOL={FACTORIO_VOL},
    CONFIG={CONFIG},
    DATA={DATA},
    MODS={MODS},
    TEMP={TEMP},
    SCENARIOS={SCENARIOS},
    SAVE={SAVE}
    '''
)

try:
    mkdir(FACTORIO_VOL)
    logging.info(f'Directory {FACTORIO_VOL} created')
except:
    pass
try:
    mkdir(CONFIG)
    logging.info(f'Directory {CONFIG} created')
except:
    pass
try:
    mkdir(DATA)
    logging.info(f'Directory {DATA} created')
except:
    pass
try:
    mkdir(MODS)
    logging.info(f'Directory {MODS} created')
except:
    pass
try:
    mkdir(TEMP)
    logging.info(f'Directory {TEMP} created')
except:
    pass
try:
    mkdir(SCENARIOS)
    logging.info(f'Directory {SCENARIOS} created')
except:
    pass
try:
    mkdir(SAVE)
    logging.info(f'Directory {SAVE} created')
except:
    pass

# Environment Files
server_settings_file = f'{CONFIG}/server-settings.json'
rcon_passwd_file = f'{CONFIG}/rconpwd'
map_gen_settings_file = f'{CONFIG}/map-gen-settings.json'
map_settings_file = f'{CONFIG}/map-settings.json'
save_path = f'{SAVE}/{SAVE_NAME}.zip'
server_banlist_file = f'{CONFIG}/server-banlist.json'
server_whitelist_file = f'{CONFIG}/server-whitelist.json'
server_adminlist_file = f'{CONFIG}/server-adminlist.json'
server_id_file = f'{CONFIG}/server-id.json'

# Setup Environment Files
update_server_settings()
update_map_gen_settings()
update_map_settings()
delete_temp_save()
generate_new_save()
rcon_passwd = generate_rcon_passwd()


# Determine agruments options and parameters
argument_list = [
    f'--port {PORT}',
    f'--rcon-port {RCON_PORT}',
    f'--rcon-password "{rcon_passwd}"',
    f'--server-settings "{server_settings_file}"',
    f'--server-banlist "{server_banlist_file}"',
    f'--server-whitelist "{server_whitelist_file}"',
    f'--use-server-whitelist',
    f'--server-adminlist "{server_adminlist_file}"',
    f'--server-id {server_id_file}'
]

if BIND:
    argument_list.append(f'--bind "{BIND}"')

if LOAD_LATEST_SAVE == 'true' or LOAD_LATEST_SAVE == 'True':
    argument_list.append(f'--start-server-load-latest')
else:
    argument_list.append(
        f'--start-server "{save_path}"')

arg_str = " ".join(argument_list)

logging.debug(f'argument_list: {argument_list}')
logging.debug(f'arg_str={arg_str}')

# Execute server with argumetns
logging.info('Executing factorio')
if DEBUG:
    system(f'exec /opt/factorio/bin/x64/factorio {arg_str}')
else:
    system(f'exec /opt/factorio/bin/x64/factorio {arg_str} &')
    system(f'tail -f /dev/null')

sleep(30)
logging.info('CONTAINER GOING DOWN!!!')
print('CONTAINER GOING DOWN!!!')
exit(0)