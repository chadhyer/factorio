from os import environ, remove, path, system
import json, secrets, string, glob, shutil


def update_server_settings(
        template:str=f"{environ.get('DATA')}/server-settings.example.json",
        settings_file:str=f"{environ.get('CONFIG')}/server-settings.json"
    ) -> None:
    """
    Save factorio server-settings.json to file

    Parameters
    ----------
    template (str)
        Default: f"{environ.get('DATA')}/server-settings.example.json"
        Description: String path to the server-settings.example.json file

    config_dir (str)
        Default: f"{environ.get('CONFIG')}/server-settings.json"
        Description: String path to the server-settings.json file

    Returns
    -------
    None
    """

    env_server_settings = {
        'name': environ.get('NAME', 'MyFactorioServer'),
        'description': environ.get('DESCRIPTION', 'A factorio server!'),
        'max_players': environ.get('MAX_PLAYERS', 0),
        'visibility': {
            'public': environ.get('PUBLIC', True),
            'lan': environ.get('LAN', True),
        },
        'username': environ.get('USERNAME', ''),
        'password': environ.get('PASSWORD', ''),
        'token': environ.get('TOKEN', ''),
        'game_password': environ.get('GAME_PASSWORD', ''),
        'require_user_verification': environ.get('REQUIRE_USER_VERIFICATION', True),
        'max_upload_in_kilobytes_per_second': environ.get('MAX_UPLOAD_IN_KILOBYTES_PER_SECOND', 0),
        'max_upload_slots': environ.get('MAX_UPLOAD_SLOTS', 5),
        'minimum_latency_in_ticks': environ.get('MINIMUM_LATENCY_IN_TICKS', 0),
        'max_heartbeats_per_second': environ.get('MAX_HEARTBEATS_PER_SECOND', 60),
        'ignore_player_limit_for_returning_players': environ.get('IGNORE_PLAYER_LIMIT_FOR_RETURNING_PLAYERS', False),
        'allow_commands': environ.get('ALLOW_COMMANDS', 'admins-only'),
        'autosave_interval': environ.get('AUTOSAVE_INTERVAL', 10),
        'autosave_slots': environ.get('AUTOSAVE_SLOTS', 5),
        'afk_autokick_interval': environ.get('AFK_AUTOKICK_INTERVAL', 0),
        'auto_pause': environ.get('AUTO_PAUSE', True),
        'only_admins_can_pause_the_game': environ.get('ONLY_ADMINS_CAN_PAUSE_THE_GAME', True),
        'autosave_only_on_server': environ.get('AUTOSAVE_ONLY_ON_SERVER', True),
        'non_blocking_saving': environ.get('NON_BLOCKING_SAVING', False),
        'minimum_segment_size': environ.get('MINIMUM_SEGMENT_SIZE', 25),
        'minimum_segment_size_peer_count': environ.get('MINIMUM_SEGMENT_SIZE_PEER_COUNT', 20),
        'maximum_segment_size': environ.get('MAXIMUM_SEGMENT_SIZE', 100),
        'maximum_segment_size_peer_count': environ.get('MAXIMUM_SEGMENT_SIZE_PEER_COUNT', 10),
    }

    with open(template, 'r') as file:
        template_settings = json.load(file)

    server_settings = template_settings

    for key, value in env_server_settings.items():
        server_settings[key] = value

    with open(settings_file, 'w', encoding='utf-8') as file:
        json.dump(server_settings, file, ensure_ascii=False, indent=4)


def generate_rcon_passwd(
        rcon_passwd_file:str=f"{environ.get('CONFIG')}/rconpwd"
    ) -> str:
    """
    Return and save factorio rcon passwd to file

    Parameters
    ----------
    rcon_passwd_file (str)
        Default: f"{environ.get('CONFIG')}/rconpwd"
        Description: String path to rcon passwd file

    Returns
    -------
    Returns rcon_passwd (str)
    """

    if not path.exists(rcon_passwd_file):
        alphabet = string.ascii_letters + string.digits
        rcon_passwd = ''.join(secrets.choice(alphabet) for i in range(20))

        with open(rcon_passwd_file, 'a') as file:
            file.write(rcon_passwd + '\n')

    with open(rcon_passwd_file, 'r') as file:
        rcon_passwd = file.read().rstrip()

    return rcon_passwd


def delete_temp_save(
        SAVE:str=environ.get('SAVE'),
        SAVE_NAME:str=environ.get('SAVE_FILE', 'world'),
        temp_file_pattern:str='*.tmp.zip'
    ) -> None:
    """
    Delete incomplete saves (such as after a forced exit)

    Parameters
    ----------
    SAVE (str)
        Default: environ.get('SAVE')
        Description: Directory where saves are stored

    SAVE_NAME (str)
        Default: environ.get('SAVE_NAME', 'world')
        Description: Name of the save file

    temp_file_pattern (str)
        Default: '*.tmp.zip'
        Description: REGEX pattern to find tmp save files
    """

    temp_save = f'{SAVE}/{SAVE_NAME}{temp_file_pattern}'

    for file in glob.glob(temp_save):
        remove(file)


def generate_new_save(
        SAVE:str=environ.get('SAVE'),
        SAVE_NAME:str=environ.get('SAVE_FILE', 'world'),
        GENERATE_NEW_SAVE:bool=environ.get('GENERATE_NEW_SAVE', False),
        map_gen_settings:str=f"{environ.get('CONFIG')}/map-gen-settings.json",
        map_settings:str=f"{environ.get('CONFIG')}/map-settings.json"
    ) -> None:
    """
    Generate new save file if GENERATE_NEW_SAVE bool is True and file doesn't

    Parameters
    ----------
    SAVE (str)
        Default: environ.get('SAVE')
        Description: Directory where saves are stored

    SAVE_NAME (str)
        Default: environ.get('SAVE_NAME', 'world')
        Description: Name of the save file

    GENERATE_NEW_SAVE (bool)
        Default: environ.get('GENERATE_NEW_SAVE', False)
        Description: Boolean to determine if save should be generated

    map_gen_settings (str)
        Default: f"{environ.get('CONFIG')}/map-gen-settings.json"
        Description: Location of map-gen-settings.json file to use while 
            generating a new save file

    map_settings (str)
        Default: f"{environ.get('CONFIG')}/map-settings.json"
        Description: Location of map-settings.json file to use while generating
            a new save file

    Returns
    -------
    None
    """

    if GENERATE_NEW_SAVE:
        save_path = f'{SAVE}/{SAVE_NAME}.zip'
        if path.exists(save_path):
            print(f'Map {save_path} already exists, skipping map generation')
        else:
            system(f'/opt/factorio/bin/x64/factorio \
--create "{save_path}" \
--map-gen-settings "{map_gen_settings}" \
--map-settings "{map_settings}"')


def update_map_gen_settings(
        template:str=f"{environ.get('DATA')}/map-gen-settings.example.json",
        map_gen_settings:str=f"{environ.get('CONFIG')}/map-gen-settings.json"
    ):
    """
    Generate/update map-gen-settings.json file

    Parameters
    ----------
    template (str)
        Default: f"{environ.get('DATA')}/map-gen-settings.example.json"
        Description: Location of template map-gen-settings.example.json file

    map_gen_settings (str)
        Default: f"{environ.get('CONFIG')}/map-gen-settings.json"
        Description: Location of map-gen-settings.json file

    Returns
    -------
    None
    """

    # Future update will add ENV VAR support to update map-gen-settings
    if not path.exists(map_gen_settings):
        shutil.copyfile(template, map_gen_settings)


def update_map_settings(
        template:str=f"{environ.get('DATA')}/map-settings.example.json",
        map_settings:str=f"{environ.get('CONFIG')}/map-settings.json"
    ):
    """
    Generate/update map-settings.json

    template (str)
        Default: f"{environ.get('DATA')}/map-settings.example.json"
        Description: Location of template map-settings.example.json file

    map_settings (str)
        Default: f"{environ.get('CONFIG')}/map-settings.json"
        Description: Location of map-settings.json file to use while generating
            a new save file

    Returns
    -------
    None
    """

    # Future update will add ENV VAR support to update map-settings.json
    if not path.exists(map_settings):
        shutil.copyfile(template, map_settings)

