#!/bin/bash
server_settings=/usr/local/factorio/data/server-settings.json
cd /usr/local/factorio
sed -i -e "s/\"name\": \".*\",/\"name\": \"${SERVER_NAME}\",/" $server_settings
sed -i -e "s/\"description\": \".*\",/\"description\": \"${SERVER_DESCRIPTION}\",/" $server_settings
sed -i -e "s/\"max_players\": .*,/\"max_players\": ${SERVER_MAX_PLAYERS},/" $server_settings
sed -i -e "s/\"public\": .*,/\"public\": ${SERVER_PUBLIC},/" $server_settings
sed -i -e "s/\"lan\": .*/\"lan\": ${SERVER_LAN}/" $server_settings
sed -i -e "s/\"game_password\": \".*\",/\"game_password\": \"${SERVER_PASSWORD}\",/" $server_settings

if [ ! -f saves/${FACTORIO_SAVE_FILE}.zip ];then
    bin/x64/factorio --create saves/${FACTORIO_SAVE_FILE}.zip
fi

bin/x64/factorio --start-server saves/${FACTORIO_SAVE_FILE}.zip --server-settings /usr/local/factorio/data/server-settings.json