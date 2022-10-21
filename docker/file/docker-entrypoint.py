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

# Environment Variables
SAVE_NAME = environ.get('SAVE_FILE', 'world')
PORT = environ.get('PORT', 24197)
RCON_PORT = environ.get('RCON_PORT', 25575)
BIND = environ.get('BIND', None)
LOAD_LATEST_SAVE = environ.get('LOAD_LATEST_SAVE', True)
DEBUG = environ.get('DEBUG', False)

# Envirnment Directories
FACTORIO_VOL = "/factorio"
CONFIG = environ.get('CONFIG')
DATA = environ.get('DATA')
MODS = environ.get('MODS')
TEMP = environ.get('TEMP')
SCENARIOS = environ.get('SCENARIOS')
SCRIPTOUTPUT = environ.get('SCRIPTOUTPUT')
SAVE = environ.get('SAVE')

try:
    mkdir(FACTORIO_VOL)
except:
    pass
try:
    mkdir(CONFIG)
except:
    pass
try:
    mkdir(DATA)
except:
    pass
try:
    mkdir(MODS)
except:
    pass
try:
    mkdir(TEMP)
except:
    pass
try:
    mkdir(SCENARIOS)
except:
    pass
try:
    mkdir(SCRIPTOUTPUT)
except:
    pass
try:
    mkdir(SAVE)
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

if LOAD_LATEST_SAVE:
    argument_list.append(f'--start-server-load-latest')
else:
    argument_list.append(
        f'--start-server "{save_path}"')

arg_str = " ".join(argument_list)

# Execute server with argumetns
if DEBUG:
    system(f'exec /opt/factorio/bin/x64/factorio {arg_str}')
else:
    system(f'exec /opt/factorio/bin/x64/factorio {arg_str} &')
    system(f'tail -f /dev/null')

sleep(30)
print('CONTAINER GOING DOWN!!!')
exit(0)