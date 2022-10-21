#!/bin/sh

cd /factorio/config
server_settings=/factorio/config/server-settings.json

SAVE_FILE="${SAVE_FILE:-"world"}"
NAME="${NAME:-"MyFactorioServer"}"
DESCRIPTION="${DESCRIPTION:-"A factorio server!"}"
MAX_PLAYERS=${MAX_PLAYERS:-0}
PUBLIC="${PUBLIC:-true}"
LAN="${LAN:-true}"
USERNAME="${USERNAME:-""}"
PASSWORD="${PASSWORD:-""}"
TOKEN="${TOKEN:-""}"
GAME_PASSWORD="${GAME_PASSWORD:-""}"
REQUIRE_USER_VERIFICATION="${REQUIRE_USER_VERIFICATION:-true}"
MAX_UPLOAD_IN_KILOBYTES_PER_SECOND=${MAX_UPLOAD_IN_KILOBYTES_PER_SECOND:-0}
MAX_UPLOAD_SLOTS=${MAX_UPLOAD_SLOTS:-5}
MINIMUM_LATENCY_IN_TICK=${MINIMUM_LATENCY_IN_TICK:-0}
MAX_HEARTBEATS_PER_SECOND=${MAX_HEARTBEATS_PER_SECOND:-60}
IGNORE_PLAYER_LIMIT_FOR_RETURNING_PLAYERS="${IGNORE_PLAYER_LIMIT_FOR_RETURNING_PLAYERS:-false}"
ALLOW_COMMANDS="${ALLOW_COMMANDS:-"admins-only"}"
AUTOSAVE_INTERVAL=${AUTOSAVE_INTERVAL:-10}
AUTOSAVE_SLOTS=${AUTOSAVE_SLOTS:-5}
AFK_AUTOKICK_INTERVAL=${AFK_AUTOKICK_INTERVAL:-0}
AUTO_PAUSE="${AUTO_PAUSE:-true}"
ONLY_ADMINS_CAN_PAUSE_THE_GAME="${ONLY_ADMINS_CAN_PAUSE_THE_GAME:-true}"
AUTOSAVE_ONLY_ON_SERVER="${AUTOSAVE_ONLY_ON_SERVER:-true}"
NON_BLOCKING_SAVING="${NON_BLOCKING_SAVING:-false}"
MINIMUM_SEGMENT_SIZE=${MINIMUM_SEGMENT_SIZE:-25}
MINIMUM_SEGMENT_SIZE_PEER_COUNT=${MINIMUM_SEGMENT_SIZE_PEER_COUNT:-20}
MAXIMUM_SEGMENT_SIZE=${MAXIMUM_SEGMENT_SIZE:-100}
MAXIMUM_SEGMENT_SIZE_PEER_COUNT=${MAXIMUM_SEGMENT_SIZE_PEER_COUNT:-10}

# Update the config file with the ENVIRONMENT variables
update_server_settings(){
    local key=$1
    local value=$2
    local string=$3
    if [[ "$string" == "false" ]];then
        sed -i -e "s|\"${key}\"|\"${key}\": ${value}|" $server_settings
    elif [[ "$string" == "true" ]];then
        sed -i -e "s|\"${key}\"|\"${key}\": \"${value}\"|" $server_settings
    fi
}

update_server_settings
sed -i -e \
    "s/\"name\": \".*\",\/\"name\": \"${NAME}\",/" \
    $server_settings
sed -i -e \
    "s/\"description\": \".*\",/\"description\": \"${DESCRIPTION}\",/" \
    $server_settings
sed -i -e \
    "s/\"max_players\": .*,/\"max_players\": ${MAX_PLAYERS},/" \
    $server_settings
sed -i -e \
    "s/\"public\": .*,/\"public\": ${PUBLIC},/" \
    $server_settings
sed -i -e \
    "s/\"lan\": .*/\"lan\": ${LAN}/" \
    $server_settings
sed -i -e \
    "s/\"username\": \".*\"/\"username\": \"${USERNAME}\"/" \
    $server_settings
sed -i -e \
    "s/\"password\": \".*\"/\"password\": \"${PASSWORD}\"/" \
    $server_settings
sed -i -e \
    "s/\"token\": \".*\"/\"token\": \"${TOKEN}\"/" \
    $server_settings
sed -i -e \
    "s/\"game_password\": \".*\",/\"game_password\": \"${GAME_PASSWORD}\",/" \
    $server_settings
sed -i -e \
    "s/\"require_user_verification\": .*,/\"require_user_verification\": ${REQUIRE_USER_VERIFICATION},/" \
    $server_settings
sed -i -e \
    "s/\"max_upload_in_kilobytes_per_second\": .*,/\"max_upload_in_kilobytes_per_second\": ${MAX_UPLOAD_IN_KILOBYTES_PER_SECOND},/" \
    $server_settings
sed -i -e \
    "s/\"max_upload_slots\": .*,/\"max_upload_slots\": ${MAX_UPLOAD_SLOTS},/" \
    $server_settings
sed -i -e \
    "s/\"minimum_latency_in_ticks\": .*,/\"minimum_latency_in_ticks\": ${MINIMUM_LATENCY_IN_TICK},/" \
    $server_settings
sed -i -e \
    "s/\"max_heartbeats_per_second\": .*,/\"max_heartbeats_per_second\": ${MAX_HEARTBEATS_PER_SECOND},/" \
    $server_settings
sed -i -e \
    "s/\"ignore_player_limit_for_returning_players\": .*,/\"ignore_player_limit_for_returning_players\": ${IGNORE_PLAYER_LIMIT_FOR_RETURNING_PLAYERS},/" \
    $server_settings
sed -i -e \
    "s/\"allow_commands\": \".*\"/\"allow_commands\": \"${ALLOW_COMMANDS}\"/" \
    $server_settings
sed -i -e \
    "s/\"autosave_interval\": .*,/\"autosave_interval\": ${AUTOSAVE_INTERVAL},/" \
    $server_settings
sed -i -e \
    "s/\"autosave_slots\": .*,/\"autosave_slots\": ${AUTOSAVE_SLOTS},/" \
    $server_settings
sed -i -e \
    "s/\"afk_autokick_interval\": .*,/\"afk_autokick_interval\": ${AFK_AUTOKICK_INTERVAL},/" \
    $server_settings
sed -i -e \
    "s/\"auto_pause\": .*,/\"auto_pause\": ${AUTO_PAUSE},/" \
    $server_settings
sed -i -e \
    "s/\"only_admins_can_pause_the_game\": .*,/\"only_admins_can_pause_the_game\": ${ONLY_ADMINS_CAN_PAUSE_THE_GAME},/" \
    $server_settings
sed -i -e \
    "s/\"autosave_only_on_server\": .*,/\"autosave_only_on_server\": ${AUTOSAVE_ONLY_ON_SERVER},/" \
    $server_settings
sed -i -e \
    "s/\"non_blocking_saving\": .*,/\"non_blocking_saving\": ${NON_BLOCKING_SAVING},/" \
    $server_settings
sed -i -e \
    "s/\"minimum_segment_size\": .*,/\"minimum_segment_size\": ${MINIMUM_SEGMENT_SIZE},/" \
    $server_settings
sed -i -e \
    "s/\"minimum_segment_size_peer_count\": .*,/\"minimum_segment_size_peer_count\": ${MINIMUM_SEGMENT_SIZE_PEER_COUNT},/" \
    $server_settings
sed -i -e \
    "s/\"maximum_segment_size\": .*,/\"maximum_segment_size\": ${MAXIMUM_SEGMENT_SIZE},/" \
    $server_settings
sed -i -e \
    "s/\"maximum_segment_size_peer_count\": .*,/\"maximum_segment_size_peer_count\": ${MAXIMUM_SEGMENT_SIZE_PEER_COUNT},/" \
    $server_settings

if [ ! -f saves/${SAVE_FILE}.zip ];then # Create the save file if it is missing
    bin/x64/factorio --create saves/${SAVE_FILE}.zip
fi

# Start the server
run_game(){
    echo '1' > ./.alive &&\
    bin/x64/factorio \
        --start-server saves/${SAVE_FILE}.zip \
        --server-settings \
        /usr/local/factorio/data/server-settings.json &
}
run_game
tail -f ./.alive
rm ./.alive
print('end')
exit 0