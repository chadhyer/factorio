from os import environ, remove, path, system
import json, secrets, string, glob
import logging


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

    logging.info('updating server settings...')
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
        logging.info('generating rcon server password...')
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

    logging.info('deleting temp saves...')
    temp_save = f'{SAVE}/{SAVE_NAME}{temp_file_pattern}'

    for file in glob.glob(temp_save):
        remove(file)


def generate_new_save(
        SAVE:str=environ.get('SAVE'),
        SAVE_NAME:str=environ.get('SAVE_NAME', 'world'),
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

    logging.debug(f'GENERATE_NEW_SAVE={GENERATE_NEW_SAVE}')
    if GENERATE_NEW_SAVE != False:
        logging.info('generating new save...')
        save_path = f'{SAVE}/{SAVE_NAME}.zip'
        if path.exists(save_path):
            logging.info(
                f'Map {save_path} already exists, skipping map generation')
            print(f'Map {save_path} already exists, skipping map generation')
        else:
            system(f'/opt/factorio/bin/x64/factorio \
--create "{save_path}" \
--map-gen-settings "{map_gen_settings}" \
--map-settings "{map_settings}"')


def update_map_gen_settings(
        template:str=f"{environ.get('DATA')}/map-gen-settings.example.json",
        map_gen_settings_file:str=f"{environ.get('CONFIG')}/map-gen-settings.json"
    ):
    """
    Generate/update map-gen-settings.json file

    Parameters
    ----------
    template (str)
        Default: f"{environ.get('DATA')}/map-gen-settings.example.json"
        Description: Location of template map-gen-settings.example.json file

    map_gen_settings_file (str)
        Default: f"{environ.get('CONFIG')}/map-gen-settings.json"
        Description: Location of map-gen-settings.json file

    Returns
    -------
    None
    """

    logging.info('updating map gen settings...')
    env_map_gen_settings = {
        'terrain_segmentation': environ.get('TERRAIN_SEGMENTATION', 1),
        'water': environ.get('WATER', 1),
        'width': environ.get('WIDTH', 0),
        'height': environ.get('HEIGHT', 0),
        'starting_area': environ.get('STARTING_AREA', 1),
        'peaceful_mode': environ.get('PEAVEFUL_MODE', False),
        'autoplace_controls': {
            'coal': {
                'frequency': environ.get('COAL_FREQUENCY', 1),
                'size': environ.get('COAL_SIZE', 1),
                'richness': environ.get('COAL_RICHNESS', 1)
            },
            'stone': {
                'frequency': environ.get('STONE_FREQUENCY', 1),
                'size': environ.get('STONE_SIZE', 1),
                'richness': environ.get('STONE_RICHNESS', 1)
            },
            'copper-ore': {
                'frequency': environ.get('COPPER_FREQUENCY', 1),
                'size': environ.get('COPPER_SIZE', 1),
                'richness': environ.get('COPPER_RICHNESS', 1)
            },
            'iron-ore': {
                'frequency': environ.get('IRON_FREQUENCY', 1),
                'size': environ.get('IRON_SIZE', 1),
                'richness': environ.get('IRON_RICHNESS', 1)
            },
            'uranium-ore': {
                'frequency': environ.get('URANIUM_FREQUENCY', 1),
                'size': environ.get('URANIUM_SIZE', 1),
                'richness': environ.get('URANIUM_RICHNESS', 1)
            },
            'crude-oil': {
                'frequency': environ.get('CRUDE_FREQUENCY', 1),
                'size': environ.get('CRUDE_SIZE', 1),
                'richness': environ.get('CRUDE_RICHNESS', 1)
            },
            'trees': {
                'frequency': environ.get('TREES_FREQUENCY', 1),
                'size': environ.get('TREES_SIZE', 1),
                'richness': environ.get('TREES_RICHNESS', 1)
            },
            'enemy-base': {
                'frequency': environ.get('ENEMY_FREQUENCY', 1),
                'size': environ.get('ENEMY_SIZE', 1),
                'richness': environ.get('ENEMY_RICHNESS', 1)
            }
        },
        'cliff_settings': {
            'name': 'cliff',
            'cliff_elevation_0': environ.get('CLIFF_ELEVATION_0', 10),
            'cliff_elevation_interval': environ.get('CLIFF_ELEVATION_INTERVAL', 40),
            'richness': environ.get('CLIFF_RICHNESS', 1)
        },
        'property_expression_names': {
            'control-setting:moisture:frequency:multiplier': environ.get('MOISTURE_FREQUENCY', "1"),
            'control-setting:moisture:bias': environ.get('MOISTURE_BIAS', "0"),
            'control-setting:aux:frequency:multiplier': environ.get('AUX_FREQUENCY', "1"),
            'control-setting:aux:bias': environ.get('AUX_BIAS', "0")
        },
        'starting_points': [
            {
                'x': environ.get('STARTING_POINTS_X', 0),
                'y': environ.get('STARTING_POINTS_Y', 0),
            }
        ],
        'seed': environ.get('SEED', None)
    }

    with open(template, 'r') as file:
        template_settings = json.load(file)

    map_gen_settings = template_settings

    for key, value in env_map_gen_settings.items():
        map_gen_settings[key] = value

    with open(map_gen_settings_file, 'w', encoding='utf-8') as file:
        json.dump(map_gen_settings, file, ensure_ascii=False, indent=4)


def update_map_settings(
        template:str=f"{environ.get('DATA')}/map-settings.example.json",
        map_settings_file:str=f"{environ.get('CONFIG')}/map-settings.json"
    ):
    """
    Generate/update map-settings.json

    template (str)
        Default: f"{environ.get('DATA')}/map-settings.example.json"
        Description: Location of template map-settings.example.json file

    map_settings_file (str)
        Default: f"{environ.get('CONFIG')}/map-settings.json"
        Description: Location of map-settings.json file to use while generating
            a new save file

    Returns
    -------
    None
    """

    logging.info('updating map settings...')
    env_map_settings = {
        'difficulty_settings': {
            'recipe_difficulty': environ.get('RECIPE_DIFFICULTY', 0),
            'technology_difficulty': environ.get('TECHNOLOGY_DIFFICULTY', 0),
            'technology_price_multiplier': environ.get(
                'TECHNOLOGY_PRICE_MULTIPLIER', 1),
            'research_queue_setting': environ.get(
                'RESEARCH_QUEUE_SETTING', 'after-victory'),
        },
        'pollution': {
            'enabled': environ.get('POLLUTION_ENABLED', True),
            'diffusion_ratio': environ.get('DIFFUSION_RATIO', 0.02),
            'min_to_diffuse': environ.get('MIN_TO_DIFFUSE', 15),
            'ageing': environ.get('AGEING', 1),
            'expected_max_per_chunk': environ.get(
                'EXPECTED_MAX_PER_CHUNK', 150),
            'min_to_show_per_chunk': environ.get(
                'MIN_TO_SHOW_PER_CHUNK', 50),
            'min_pollution_to_damage_trees': environ.get(
                'MIN_POLLUTION_TO_DAMAGE_TREES', 60),
            'pollution_with_max_forest_damage': environ.get(
                'POLLUTION_WITH_MAX_FOREST_DAMAGE', 150),
            'pollution_per_tree_damage': environ.get(
                'POLLUTION_PER_TREE_DAMAGE', 50),
            'pollution_restored_per_tree_damage': environ.get(
                'POLLUTION_RESTORED_PER_TREE_DAMAGE', 10),
            'max_pollution_to_restore_trees': environ.get(
                'MAX_POLLUTION_TO_RESTORE_TREES', 20),
            'enemy_attack_pollution_consumption_modifier': environ.get(
                'ENEMY_ATTACK_POLLUTION_CONSUMPTION_MODIFIER', 1)
        },
        'enemy_evolution': {
            'enabled': environ.get('ENEMY_EVOLUTION_ENABLED', True),
            'time_factor': environ.get(
                'TIME_FACTOR', 0.000004),
            'destroy_factor': environ.get(
                'DESTROY_FACTOR', 0.002),
            'pollution_factor': environ.get(
                'POLLUTION_FACTOR', 0.0000009)
        },
        'enemy_expansion': {
            'enabled': environ.get('ENEMY_EXPANSION_ENABLED', True),
            'min_base_spacing': environ.get(
                'MIN_BASE_SPACING', 3),
            'max_expansion_distance': environ.get(
                'MAX_EXPANSION_DISTANCE', 7),
            'friendly_base_influence_radius': environ.get(
                'FRIENDLY_BASE_INFLUENCE_RADIUS', 2),
            'enemy_building_influence_radius': environ.get(
                'ENEMY_BUILDING_INFLUENCE_RADIUS', 2),
            'building_coefficient': environ.get(
                'BUILDING_COEFFICIENT', 0.1),
            'other_base_coefficient': environ.get(
                'OTHER_BASE_COEFFICIENT', 2.0),
            'neighbouring_chunk_coefficient': environ.get(
                'NEIGHBOURING_CHUNK_COEFFICIENT', 0.5),
            'neighbouring_base_chunk_coefficient': environ.get(
                'NEIGHBOURING_BASE_CHUNK_COEFFICIENT', 0.4),
            'max_colliding_tiles_coefficient': environ.get(
                'MAX_COLLIDING_TILES_COEFFICIENT', 0.9),
            'settler_group_min_size': environ.get(
                'SETTLER_GROUP_MIN_SIZE', 5),
            'settler_group_max_size': environ.get(
                'SETTLER_GROUP_MAX_SIZE', 20),
            'min_expansion_cooldown': environ.get(
                'MIN_EXPANSION_COOLDOWN', 14400),
            'max_expansion_cooldown': environ.get(
                'MAX_EXPANSION_COOLDOWN', 216000)
        },
        'unit_group': {
            'min_group_gathering_time': environ.get(
                'MIN_GROUP_GATHERING_TIME', 3600),
            'max_group_gathering_time': environ.get(
                'MAX_GROUP_GATHERING_TIME', 36000),
            'max_wait_time_for_late_members': environ.get(
                'MAX_WAIT_TIME_FOR_LATE_MEMBERS', 7200),
            'max_group_radius': environ.get('MAX_GROUP_RADIUS', 30.0),
            'min_group_radius': environ.get('MIN_GROUP_RADIUS', 5.0),
            'max_member_speedup_when_behind': environ.get(
                'MAX_MEMBER_SPEEDUP_WHEN_BEHIND', 1.4),
            'max_member_slowdown_when_ahead': environ.get(
                'MAX_MEMBER_SLOWDOWN_WHEN_AHEAD', 0.6),
            'max_group_slowdown_factor': environ.get(
                'MAX_GROUP_SLOWDOWN_FACTOR', 0.3),
            'max_group_member_fallback_factor': environ.get(
                'MAX_GROUP_MEMBER_FALLBACK_FACTOR', 3),
            'member_disown_distance': environ.get(
                'MEMBER_DISOWN_DISTANCE', 10),
            'tick_tolerance_when_member_arrives': environ.get(
                'TICK_TOLERANCE_WHEN_MEMBER_ARRIVES', 60),
            'max_gathering_unit_groups': environ.get(
                'MAX_GATHERING_UNIT_GROUPS', 30),
            'max_unit_group_size': environ.get('MAX_UNIT_GROUP_SIZE', 200)
        },
        'steering': {
            'default': {
                'radius': environ.get('STEERING_RADIUS', 1.2),
                'separation_force': environ.get(
                    'STEERING_SEPARATION_FORCE', 0.005),
                'separation_factor': environ.get(
                    'STEERING_SEPARATION_FACTOR', 1.2),
                'force_unit_fuzzy_goto_behavior': environ.get(
                    'STEERING_UNIT_FUZZY_GOTO_BEHAVIOR', False)
            },
            'moving': {
                'radius': environ.get('MOVING_RADIUS', 3),
                'separation_force': environ.get(
                    'MOVING_SEPARATION_FORCE', 0.01),
                'separation_factor': environ.get(
                    'MOVING_SEPARATION_FACTOR', 3),
                'force_unit_fuzzy_goto_behavior': environ.get(
                    'MOVING_FORCE_UNIT_FUZZY_GOTO_BEHAVIOR', False)
            }
        },
        'path_finder': {
            'fwd2bwd_ratio': environ.get('FWD2BWD_RATIO', 5),
            'goal_pressure_ratio': environ.get('GOAL_PRESSURE_RATIO', 2),
            'max_steps_worked_per_tick': environ.get(
                'MAX_STEPS_WORKED_PER_TICK', 100),
            'max_work_done_per_tick': environ.get(
                'MAX_WORK_DONE_PER_TICK', 8000),
            'use_path_cache': environ.get('USE_PATH_CACHE', True),
            'short_cache_size': environ.get('SHORT_CACHE_SIZE', 5),
            'long_cache_size': environ.get('LONG_CACHE_SIZE', 25),
            'short_cache_min_cacheable_distance': environ.get(
                'SHORT_CACHE_MIN_CACHEABLE_DISTANCE', 10),
            'short_cache_min_algo_steps_to_cache': environ.get(
                'SHORT_CACHE_MIN_ALGO_STEPS_TO_CACHE', 50),
            'long_cache_min_cacheable_distance': environ.get(
                'LONG_CACHE_MIN_CACHEABLE_DISTANCE', 30),
            'cache_max_connect_to_cache_steps_multiplier': environ.get(
                'CACHE_MAX_CONNECT_TO_CACHE_STEPS_MULTIPLIER', 100),
            'cache_accept_path_start_distance_ratio': environ.get(
                'CACHE_ACCEPT_PATH_START_DISTANCE_RATIO', 0.2),
            'cache_accept_path_end_distance_ratio': environ.get(
                'CACHE_ACCEPT_PATH_END_DISTANCE_RATIO', 0.15),
            'negative_cache_accept_path_start_distance_ratio': environ.get(
                'NEGATIVE_CACHE_ACCEPT_PATH_START_DISTANCE_RATIO', 0.3),
            'negative_cache_accept_path_end_distance_ratio': environ.get(
                'NEGATIVE_CACHE_ACCEPT_PATH_END_DISTANCE_RATIO', 0.3),
            'cache_path_start_distance_rating_multiplier': environ.get(
                'CACHE_PATH_START_DISTANCE_RATING_MULTIPLIER', 10),
            'cache_path_end_distance_rating_multiplier': environ.get(
                'CACHE_PATH_END_DISTANCE_RATING_MULTIPLIER', 20),
            'stale_enemy_with_same_destination_collision_penalty': environ.get(
                'STALE_ENEMY_WITH_SAME_DESTINATION_COLLISION_PENALTY', 30),
            'ignore_moving_enemy_collision_distance': environ.get(
                'IGNORE_MOVING_ENEMY_COLLISION_DISTANCE', 5),
            'enemy_with_different_destination_collision_penalty': environ.get(
                'ENEMY_WITH_DIFFERENT_DESTINATION_COLLISION_PENALTY', 30),
            'general_entity_collision_penalty': environ.get(
                'GENERAL_ENTITY_COLLISION_PENALTY', 10),
            'general_entity_subsequent_collision_penalty': environ.get(
                'GENERAL_ENTITY_SUBSEQUENT_COLLISION_PENALTY', 3),
            'extended_collision_penalty': environ.get(
                'EXTENDED_COLLISION_PENALTY', 3),
            'max_clients_to_accept_any_new_request': environ.get(
                'MAX_CLIENTS_TO_ACCEPT_ANY_NEW_REQUEST', 10),
            'max_clients_to_accept_short_new_request': environ.get(
                'MAX_CLIENTS_TO_ACCEPT_SHORT_NEW_REQUEST', 100),
            'direct_distance_to_consider_short_request': environ.get(
                'DIRECT_DISTANCE_TO_CONSIDER_SHORT_REQUEST', 100),
            'short_request_max_steps': environ.get(
                'SHORT_REQUEST_MAX_STEPS', 1000),
            'short_request_ratio': environ.get('SHORT_REQUEST_RATIO', 0.5),
            'min_steps_to_check_path_find_termination': environ.get(
                'MIN_STEPS_TO_CHECK_PATH_FIND_TERMINATION', 2000),
            'start_to_goal_cost_multiplier_to_terminate_path_find': environ.get(
                'START_TO_GOAL_COST_MULTIPLIER_TO_TERMINATE_PATH_FIND', 500.0),
            'overload_levels': [0, 100, 500],
            'overload_multipliers': [2, 3, 4],
            'negative_path_cache_delay_interval': environ.get(
                'NEGATIVE_PATH_CACHE_DELAY_INTERVAL', 20)
        },
        'max_failed_behavior_count': 3
    }

    with open(template, 'r') as file:
        template_settings = json.load(file)

    map_settings = template_settings

    for key, value in env_map_settings.items():
        map_settings[key] = value

    with open(map_settings_file, 'w', encoding='utf-8') as file:
        json.dump(map_settings, file, ensure_ascii=False, indent=4)
