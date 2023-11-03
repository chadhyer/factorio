# Example deployments
```
docker run --name factorio \
    -v factorio-save:/factorio/saves \
    -p 24197:24197/udp \
    -p 25575:25575/tcp
    --env-file ./some.env
```

# Environment Variables
## Main Build Variables
### Build Args
`VERSION`
    Default: `1.1.94`
    Description: Determine which version of factorio to build the server for
`RETRIES`
    Default: `5`
    Description: How many times the build process will attempt to download the factorio server files
`USER`
    Default: `factorio`
    Description: The user that will be executing the factorio server
`GROUP`
    Default: `factorio`
    Description: The primary group of the user that will be executing the factorio server
### Container Variables
`SHA256`
    Default: `NULL`
    Description: Was used in previous branch and may be used in a future branch to ensure integrity of factorio server files
`PORT`
    Default: `24197`
    Description: The UDP port the factorio server will run on
`RCON_PORT`
    Default: `25575`
    Description: The TCP port the rcon server will run on
`RCON_PASSWORD`
    Default: ``
    Description: Determine the rcon password. If not defined then existing file will not be updated.
`BIN`
    Default: `/factorio/bin`
    Description: Currently unused and should be pointed at /opt/factorio/bin anyways...
`CONFIG`
    Default: `/factorio/config`
    Description: The location where all server config files should be saved. Note that /factorio should be a bound to a named volume using the compose file. Note you can edit/backup/restore files in named volumes by editing /var/lib/docker/volumes/docker_<volume_name>.
`DATA`
    Default: `/opt/factorio/data`
    Description: The location where default config files are copied from.
`MODS`
    Default: /factorio/mods
    Description: The location where all server mod files should be saved. Note that /factorio should be a bound to a named volume using the compose file. Note you can edit/backup/restore files in named volumes by editing /var/lib/docker/volumes/docker_<volume_name>.
`TEMP`
    Default: `/factorio/temp`
    Description: This really isn`t used, but is created in the named volume.
`SCENARIOS`
    Default: `/factorio/scenarios`
    Description: I believe this is where scenarios are saved?
`SAVE`
    Default: `/factorio/saves`
    Description: The location where all server save files should be stored. Note that /factorio should be a bound to a named volume using the compose file. Note you can edit/backup/restore files in named volumes by editing /var/lib/docker/volumes/docker_<volume_name>.

## Server settings
`NAME`                                      Default: `MyFactorioServer`
`DESCRIPTION`                               Default: `A factorio server!`
`MAX_PLAYERS`                               Default: `0`
`PUBLIC`                                    Default: `true`
`LAN`                                       Default: `true`
`USERNAME`                                  Default: ``
`PASSWORD`                                  Default: ``
`TOKEN`                                     Default: ``
`GAME_PASSWORD`                             Default: ``
`REQUIRE_USER_VERIFICATION`                 Default: `true`
`MAX_UPLOAD_IN_KILOBYTES_PER_SECOND`        Default: `0`
`MAX_UPLOAD_SLOTS`                          Default: `5`
`MINIMUM_LATENCY_IN_TICKS`                  Default: `0`
`MAX_HEARTBEATS_PER_SECOND`                 Default: `60`
`IGNORE_PLAYER_LIMIT_FOR_RETURNING_PLAYERS` Default: `false`
`ALLOW_COMMANDS`                            Default: `admins-only`
`AUTOSAVE_INTERVAL`                         Default: `10`
`AUTOSAVE_SLOTS`                            Default: `5`
`AFK_AUTOKICK_INTERVAL`                     Default: `0`
`AUTO_PAUSE`                                Default: `true`
`ONLY_ADMINS_CAN_PAUSE_THE_GAME`            Default: `true`
`AUTOSAVE_ONLY_ON_SERVER`                   Default: `true`
`NON_BLOCKING_SAVING`                       Default: `false`
`MINIMUM_SEGMENT_SIZE`                      Default: `25`
`MINIMUM_SEGMENT_SIZE_PEER_COUNT`           Default: `20`
`MAXIMUM_SEGMENT_SIZE`                      Default: `100`
`MAXIMUM_SEGMENT_SIZE_PEER_COUNT`           Default: `10`

## Map Gen Variables
`TERRAIN_SEGMENTATION`      Default: `1`
`WATER`                     Default: `1`
`WIDTH`                     Default: `0`
`HEIGHT`                    Default: `0`
`STARTING_AREA`             Default: `1`
`PEAVEFUL_MODE`             Default: `false`
`COAL_FREQUENCY`            Default: `1`
`COAL_SIZE`                 Default: `1`
`COAL_RICHNESS`             Default: `1`
`STONE_FREQUENCY`           Default: `1`
`STONE_SIZE`                Default: `1`
`STONE_RICHNESS`            Default: `1`
`COPPER_FREQUENCY`          Default: `1`
`COPPER_SIZE`               Default: `1`
`COPPER_RICHNESS`           Default: `1`
`IRON_FREQUENCY`            Default: `1`
`IRON_SIZE`                 Default: `1`
`IRON_RICHNESS`             Default: `1`
`URANIUM_FREQUENCY`         Default: `1`
`URANIUM_SIZE`              Default: `1`
`URANIUM_RICHNESS`          Default: `1`
`CRUDE_FREQUENCY`           Default: `1`
`CRUDE_SIZE`                Default: `1`
`CRUDE_RICHNESS`            Default: `1`
`TREES_FREQUENCY`           Default: `1`
`TREES_SIZE`                Default: `1`
`TREES_RICHNESS`            Default: `1`
`ENEMY_FREQUENCY`           Default: `1`
`ENEMY_SIZE`                Default: `1`
`ENEMY_RICHNESS`            Default: `1`
`CLIFF_ELEVATION_0`         Default: `10`
`CLIFF_ELEVATION_INTERVAL`  Default: `40`
`CLIFF_RICHNESS`            Default: `1`
`MOISTURE_FREQUENCY`        Default: `"1"`
`MOISTURE_BIAS`             Default: `"0"`
`AUX_FREQUENCY`             Default: `"1"`
`AUX_BIAS`                  Default: `"0"`
`STARTING_POINTS_X`         Default: `0`
`STARTING_POINTS_Y`         Default: `0`
`SEED`                      Default: `null`

## Map Settings
### Difficulty Settings
`RECIPE_DIFFICULTY`             Default: `0`
`TECHNOLOGY_DIFFICULTY`         Default: `0`
`TECHNOLOGY_PRICE_MULTIPLIER`   Default: `1`
`RESEARCH_QUEUE_SETTING`        Default: `after-victory`
### Polution
`POLLUTION_ENABLED`                           Default: `true`
`DIFFUSION_RATIO`                             Default: `0.02`
`MIN_TO_DIFFUSE`                              Default: `15`
`AGEING`                                      Default: `1`
`EXPECTED_MAX_PER_CHUNK`                      Default: `150`
`MIN_TO_SHOW_PER_CHUNK`                       Default: `50`
`MIN_POLLUTION_TO_DAMAGE_TREES`               Default: `60`
`POLLUTION_WITH_MAX_FOREST_DAMAGE`            Default: `150`
`POLLUTION_PER_TREE_DAMAGE`                   Default: `50`
`POLLUTION_RESTORED_PER_TREE_DAMAGE`          Default: `10`
`MAX_POLLUTION_TO_RESTORE_TREES`              Default: `20`
`ENEMY_ATTACK_POLLUTION_CONSUMPTION_MODIFIER` Default: `1`

### Enemy Evolution
`ENEMY_EVOLUTION_ENABLED`   Default: `true`
`TIME_FACTOR`               Default: `0.000004`
`DESTROY_FACTOR`            Default: `0.002`
`POLLUTION_FACTOR`          Default: `0.0000009`

### Enemy Expansion
`ENEMY_EXPANSION_ENABLED`               Default: `true`
`MIN_BASE_SPACING`                      Default: `3`
`MAX_EXPANSION_DISTANCE`                Default: `7`
`FRIENDLY_BASE_INFLUENCE_RADIUS`        Default: `2`
`ENEMY_BUILDING_INFLUENCE_RADIUS`       Default: `2`
`BUILDING_COEFFICIENT`                  Default: `0.1`
`OTHER_BASE_COEFFICIENT`                Default: `2.0`
`NEIGHBOURING_CHUNK_COEFFICIENT`        Default: `0.5`
`NEIGHBOURING_BASE_CHUNK_COEFFICIENT`   Default: `0.4`
`MAX_COLLIDING_TILES_COEFFICIENT`       Default: `0.9`
`SETTLER_GROUP_MIN_SIZE`                Default: `5`
`SETTLER_GROUP_MAX_SIZE`                Default: `20`
`MIN_EXPANSION_COOLDOWN`                Default: `14400`
`MAX_EXPANSION_COOLDOWN`                Default: `216000`

### Unit Group
`MIN_GROUP_GATHERING_TIME`              Default: `3600`
`MAX_GROUP_GATHERING_TIME`              Default: `36000`
`MAX_WAIT_TIME_FOR_LATE_MEMBERS`        Default: `7200`
`MAX_GROUP_RADIUS`                      Default: `30.0`
`MIN_GROUP_RADIUS`                      Default: `5.0`
`MAX_MEMBER_SPEEDUP_WHEN_BEHIND`        Default: `1.4`
`MAX_MEMBER_SLOWDOWN_WHEN_AHEAD`        Default: `0.6`
`MAX_GROUP_SLOWDOWN_FACTOR`             Default: `0.3`
`MAX_GROUP_MEMBER_FALLBACK_FACTOR`      Default: `3`
`MEMBER_DISOWN_DISTANCE`                Default: `10`
`TICK_TOLERANCE_WHEN_MEMBER_ARRIVES`    Default: `60`
`MAX_GATHERING_UNIT_GROUPS`             Default: `30`
`MAX_UNIT_GROUP_SIZE`                   Default: `200`

### Steering
`STEERING_RADIUS`                       Default: `1.2`
`STEERING_SEPARATION_FORCE`             Default: `0.005`
`STEERING_SEPARATION_FACTOR`            Default: `1.2`
`STEERING_UNIT_FUZZY_GOTO_BEHAVIOR`     Default: `false`
`MOVING_RADIUS`                         Default: `3`
`MOVING_SEPARATION_FORCE`               Default: `0.01`
`MOVING_SEPARATION_FACTOR`              Default: `3`
`MOVING_FORCE_UNIT_FUZZY_GOTO_BEHAVIOR` Default: `false`

### Path finder
`FWD2BWD_RATIO`                                         Default: `5`
`GOAL_PRESSURE_RATIO`                                   Default: `2`
`MAX_STEPS_WORKED_PER_TICK`                             Default: `100`
`MAX_WORK_DONE_PER_TICK`                                Default: `8000`
`USE_PATH_CACHE`                                        Default: `True`
`SHORT_CACHE_SIZE`                                      Default: `5`
`LONG_CACHE_SIZE`                                       Default: `25`
`SHORT_CACHE_MIN_CACHEABLE_DISTANCE`                    Default: `10`
`SHORT_CACHE_MIN_ALGO_STEPS_TO_CACHE`                   Default: `50`
`LONG_CACHE_MIN_CACHEABLE_DISTANCE`                     Default: `30`
`CACHE_MAX_CONNECT_TO_CACHE_STEPS_MULTIPLIER`           Default: `100`
`CACHE_ACCEPT_PATH_START_DISTANCE_RATIO`                Default: `0.2`
`CACHE_ACCEPT_PATH_END_DISTANCE_RATIO`                  Default: `0.15`
`NEGATIVE_CACHE_ACCEPT_PATH_START_DISTANCE_RATIO`       Default: `0.3`
`NEGATIVE_CACHE_ACCEPT_PATH_END_DISTANCE_RATIO`         Default: `0.3`
`CACHE_PATH_START_DISTANCE_RATING_MULTIPLIER`           Default: `10`
`CACHE_PATH_END_DISTANCE_RATING_MULTIPLIER`             Default: `20`
`STALE_ENEMY_WITH_SAME_DESTINATION_COLLISION_PENALTY`   Default: `30`
`IGNORE_MOVING_ENEMY_COLLISION_DISTANCE`                Default: `5`
`ENEMY_WITH_DIFFERENT_DESTINATION_COLLISION_PENALTY`    Default: `30`
`GENERAL_ENTITY_COLLISION_PENALTY`                      Default: `10`
`GENERAL_ENTITY_SUBSEQUENT_COLLISION_PENALTY`           Default: `3`
`EXTENDED_COLLISION_PENALTY`                            Default: `3`
`MAX_CLIENTS_TO_ACCEPT_ANY_NEW_REQUEST`                 Default: `10`
`MAX_CLIENTS_TO_ACCEPT_SHORT_NEW_REQUEST`               Default: `100`
`DIRECT_DISTANCE_TO_CONSIDER_SHORT_REQUEST`             Default: `100`
`SHORT_REQUEST_MAX_STEPS`                               Default: `1000`
`SHORT_REQUEST_RATIO`                                   Default: `0.5`
`MIN_STEPS_TO_CHECK_PATH_FIND_TERMINATION`              Default: `2000`
`START_TO_GOAL_COST_MULTIPLIER_TO_TERMINATE_PATH_FIND`  Default: `500.0`
`OVERLOAD_LEVELS`                                       Default: `0, 100, 500`
`OVERLOAD_MULTIPLIERS`                                  Default: `2, 3, 4`
`NEGATIVE_PATH_CACHE_DELAY_INTERVAL`                    Default: `20`
`MAX_FAILED_BEHAVIOR_COUNT`                             Default: `3`

# Volumes
If you want data persistance then create a named volume for `SAVE` Default: `/factorio/saves`
