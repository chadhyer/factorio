#!/bin/bash

cd /usr/local/factorio
server_settings=/usr/local/factorio/data/server-settings.json

# Update the config file with the ENVIRONMENT variables
sed -i -e "s/\"name\": \".*\",/\"name\": \"${FACTORIO_NAME}\",/" $server_settings
sed -i -e "s/\"description\": \".*\",/\"description\": \"${FACTORIO_DESCRIPTION}\",/" $server_settings
sed -i -e "s/\"max_players\": .*,/\"max_players\": ${FACTORIO_MAX_PLAYERS},/" $server_settings
sed -i -e "s/\"public\": .*,/\"public\": ${FACTORIO_PUBLIC},/" $server_settings
sed -i -e "s/\"lan\": .*/\"lan\": ${FACTORIO_LAN}/" $server_settings
sed -i -e "s/\"username\": \".*\"/\"username\": \"${FACTORIO_USERNAME}\"/" $server_settings
sed -i -e "s/\"password\": \".*\"/\"password\": \"${FACTORIO_PASSWORD}\"/" $server_settings
sed -i -e "s/\"token\": \".*\"/\"token\": \"${FACTORIO_TOKEN}\"/" $server_settings
sed -i -e "s/\"game_password\": \".*\",/\"game_password\": \"${FACTORIO_GAME_PASSWORD}\",/" $server_settings
sed -i -e "s/\"require_user_verification\": .*,/\"require_user_verification\": ${FACTORIO_REQUIRE_USER_VERIFICATION},/" $server_settings
sed -i -e "s/\"max_upload_in_kilobytes_per_second\": .*,/\"max_upload_in_kilobytes_per_second\": ${FACTORIO_MAX_UPLOAD_IN_KILOBYTES_PER_SECOND},/" $server_settings
sed -i -e "s/\"max_upload_slots\": .*,/\"max_upload_slots\": ${FACTORIO_MAX_UPLOAD_SLOTS},/" $server_settings
sed -i -e "s/\"minimum_latency_in_ticks\": .*,/\"minimum_latency_in_ticks\": ${FACTORIO_MINIMUM_LATENCY_IN_TICK},/" $server_settings
sed -i -e "s/\"max_heartbeats_per_second\": .*,/\"max_heartbeats_per_second\": ${FACTORIO_MAX_HEARTBEATS_PER_SECOND},/" $server_settings
sed -i -e "s/\"ignore_player_limit_for_returning_players\": .*,/\"ignore_player_limit_for_returning_players\": ${FACTORIO_IGNORE_PLAYER_LIMIT_FOR_RETURNING_PLAYERS},/" $server_settings
sed -i -e "s/\"allow_commands\": \".*\"/\"allow_commands\": \"${FACTORIO_ALLOW_COMMANDS}\"/" $server_settings
sed -i -e "s/\"autosave_interval\": .*,/\"autosave_interval\": ${FACTORIO_AUTOSAVE_INTERVAL},/" $server_settings
sed -i -e "s/\"autosave_slots\": .*,/\"autosave_slots\": ${FACTORIO_AUTOSAVE_SLOTS},/" $server_settings
sed -i -e "s/\"afk_autokick_interval\": .*,/\"afk_autokick_interval\": ${FACTORIO_AFK_AUTOKICK_INTERVAL},/" $server_settings
sed -i -e "s/\"auto_pause\": .*,/\"auto_pause\": ${FACTORIO_AUTO_PAUSE},/" $server_settings
sed -i -e "s/\"only_admins_can_pause_the_game\": .*,/\"only_admins_can_pause_the_game\": ${FACTORIO_ONLY_ADMINS_CAN_PAUSE_THE_GAME},/" $server_settings
sed -i -e "s/\"autosave_only_on_server\": .*,/\"autosave_only_on_server\": ${FACTORIO_AUTOSAVE_ONLY_ON_SERVER},/" $server_settings
sed -i -e "s/\"non_blocking_saving\": .*,/\"non_blocking_saving\": ${FACTORIO_NON_BLOCKING_SAVING},/" $server_settings
sed -i -e "s/\"minimum_segment_size\": .*,/\"minimum_segment_size\": ${FACTORIO_MINIMUM_SEGMENT_SIZE},/" $server_settings
sed -i -e "s/\"minimum_segment_size_peer_count\": .*,/\"minimum_segment_size_peer_count\": ${FACTORIO_MINIMUM_SEGMENT_SIZE_PEER_COUNT},/" $server_settings
sed -i -e "s/\"maximum_segment_size\": .*,/\"maximum_segment_size\": ${FACTORIO_MAXIMUM_SEGMENT_SIZE},/" $server_settings
sed -i -e "s/\"maximum_segment_size_peer_count\": .*,/\"maximum_segment_size_peer_count\": ${FACTORIO_MAXIMUM_SEGMENT_SIZE_PEER_COUNT},/" $server_settings

if [ ! -f saves/${FACTORIO_SAVE_FILE}.zip ];then # Create the save file if it is missing
    bin/x64/factorio --create saves/${FACTORIO_SAVE_FILE}.zip
fi

# Start the server
bin/x64/factorio --start-server saves/${FACTORIO_SAVE_FILE}.zip --server-settings /usr/local/factorio/data/server-settings.json