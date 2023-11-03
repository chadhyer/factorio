#!/bin/bash

echo "--- factorio ${VERSION} entrypoint.sh ---"
# Main ENV VARs
if [ -z "${SAVE}" ];then
    SAVE=world
fi
if [ -z "${PORT}" ];then
    PORT=24197
fi
if [ -z "${RCON_PORT}" ];then
    RCON_PORT=25575
fi
if [ -z "${LOAD_LATEST_SAVE}" ];then
    LOAD_LATEST_SAVE=true
fi
if [ -z "${GENERATE_NEW_SAVE}" ];then
    GENERATE_NEW_SAVE=false
fi

# Directory ENV VARs
if [ -z "${FACTORIO_VOL}" ];then
    FACTORIO_VOL=/factorio
fi
if [ -z "${CONFIG}" ];then
    CONFIG=/factorio/config
fi
if [ -z "${DATA}" ];then
    DATA=/factorio/data
fi
if [ -z "${MODS}" ];then
    MODS=/factorio/mods
fi
if [ -z "${TEMP}" ];then
    TEMP=/factorio/temp
fi
if [ -z "${SCENARIOS}" ];then
    SCENARIOS=SCENARIOS
fi
if [ -z "${SAVE}" ];then
    SAVE=/factorio/save
fi

if [ -n "${DEBUG}" ];then
    echo 'ENV VAR LIST:'
    echo $(env|sort)
fi

# Create directories
mkdir -p ${FACTORIO_VOL}
mkdir -p ${CONFIG}
mkdir -p ${DATA}
mkdir -p ${MODS}
mkdir -p ${TEMP}
mkdir -p ${SCENARIOS}
mkdir -p ${SAVE}

# File ENV VARs
server_settings_file="${CONFIG}/server-settings.json"
map_gen_settings_file="${CONFIG}/map-gen-settings.json"
map_settings_file="${CONFIG}/map-settings.json"
rcon_passwd_file="${CONFIG}/rconpwd"
save_path="${SAVE}/${SAVE_NAME}.zip"
server_banlist_file="${CONFIG}/server-banlist.json"
server_whitelist_file="${CONFIG}/server-whitelist.json"
server_adminlist_file="${CONFIG}/server-adminlist.json"
server_id_file="${CONFIG}/server-id.json"

# Generate Configs
echo 'Generating config files with templates'
source /opt/factorio/default.sh
envsubst < "${DATA}/server-settings.template" > ${server_settings_file}
envsubst < "${DATA}/map-gen-settings.template" > ${map_gen_settings_file}
envsubst < "${DATA}/map-settings.template" > ${map_settings_file}

# Update rcon password if defined
if [ -n "${RCON_PASSWORD}" ];then
    echo 'Updating rcon password'
    echo "${RCON_PASSWORD}" > "${rcon_passwd_file}"
fi

# Delete incomplete saves
echo 'Deleting incomplete saves'
if [ -n ${DEBUG} ];then
    echo 'before:'
    find "${SAVE}" -name '*.tmp.zip'
fi
rm -f $(find "${SAVE}" -name '*.tmp.zip')
if [ -n ${DEBUG} ];then
    echo 'after:'
    find "${SAVE}" -name '*.tmp.zip'
fi

# Generate a new save
    
if [ "${GENERATE_NEW_SAVE}" != 'false' ] || [ ! -f "${save_path}" ];then
    echo 'Generating a new save'
    if [ -f "${save_path}" ];then
        rm -rf "${save_path}"
    fi
    /opt/factorio/bin/x64/factorio \
        --create "${save_path}" \
        --map-gen-settings "${map_gen_settings_file}" \
        --map-settings "${map_settings_file}"
fi

if [ -z "${BIND}"];then
    bind_cmd="--bind ${BIND}"
else
    bind_cmd=""
fi

if [ "${LOAD_LATEST_SAVE}" == 'true' ];then
    load_cmd="--start-server-load-latest"
else
    load_cmd="--start-server ${save_path}"
fi

exec  /opt/factorio/bin/x64/factorio \
    --port "${PORT}" \
    --rcon-port "${RCON_PORT}" \
    --rcon-password "$(cat ${rcon_passwd_file})" \
    --server-settings "${server_settings_file}" \
    --server-banlist "${server_banlist_file}" \
    --server-whitelist "${server_whitelist_file}" \
    --use-server-whitelist \
    --server-adminlist "${server_adminlist_file}" \
    --server-id "${server_id_file}" \
    "$load_cmd" \
    "$bind_cmd"

sleep 10
echo 'Container going down!'
exit 0
