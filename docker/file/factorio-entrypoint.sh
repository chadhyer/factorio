#!/bin/sh
set -eoux pipefail

FACTORIO_VOL=/factorio
UPDATE_MODS_ON_START="${UPDATE_MODS_ON_START:-false}"
GENERATE_NEW_SAVE="${GENERATE_NEW_SAVE:-false}"
SAVE_FILE="${SAVE}/${FACTORIO_SAVE_FILE:-"world"}"
BIND="${BIND:-""}"
LOAD_LATEST_SAVE="${LOAD_LATEST_SAVE:-true}"

mkdir -p "${FACTORIO_VOL}"
mkdir -p "${CONFIG}"
mkdir -p "${DATA}"
mkdir -p "${MODS}"
mkdir -p "${TEMP}"
mkdir -p "${SAVE}"
mkdir -p "${SCENARIOS}"
mkdir -p "${SCRIPTOUTPUT}"

if [[ ! -f $CONFIG/rconpw ]];then
    # Generate a new RCON password if none exists
    pwgen 15 1 >"$CONFIG/rconpw"
fi

# Copy default settings files if they don't exist
if [[ ! -f $CONFIG/server-settings.json ]]; then
    cp ${DATA}/server-settings.example.json \
        "$CONFIG/server-settings.json"
fi

if [[ ! -f $CONFIG/map-gen-settings.json ]]; then
    cp ${DATA}/map-gen-settings.example.json \
        "$CONFIG/map-gen-settings.json"
fi

if [[ ! -f $CONFIG/map-settings.json ]]; then
    cp ${DATA}/map-settings.example.json \
        "$CONFIG/map-settings.json"
fi

# not sure what the c\ is doing...
sed -i '|write-data=|c\write-data=/factorio|' /factorio/config/config.ini

NRTMPSAVES=$( find -L "$SAVE_FILE" -iname \*.tmp.zip -mindepth 1 | wc -l )
if [[ $NRTMPSAVES -gt 0 ]]; then
  # Delete incomplete saves (such as after a forced exit)
  rm -f "$SAVE_FILE"/*.tmp.zip
fi

if [[ $GENERATE_NEW_SAVE == true ]]; then
    if [[ -z "$SAVE_FILE" ]]; then
        echo "If \$GENERATE_NEW_SAVE is true, you must specify \$SAVE_NAME"
        exit 1
    fi
    if [[ -f "$SAVE/$SAVE_FILE.zip" ]]; then
        echo "Map $SAVE/$SAVE_FILE.zip already exists, skipping map \
generation"
    else
        /factorio/bin/x64/factorio \
            --create "$SAVE_FILE" \
            --map-gen-settings "$CONFIG/map-gen-settings.json" \
            --map-settings "$CONFIG/map-settings.json"
    fi
fi

# if [[ ${UPDATE_MODS_ON_START} == "true" ]]; then
#   ./docker-update-mods.sh
# fi

# if [[ $(id -u) = 0 ]]; then
#   # Update the User and Group ID based on the PUID/PGID variables
#   usermod -o -u "$PUID" factorio
#   groupmod -o -g "$PGID" factorio
#   # Take ownership of factorio data if running as root
#   chown -R factorio:factorio "$FACTORIO_VOL"
#   # Drop to the factorio user
#   SU_EXEC="su-exec factorio"
# else
#   SU_EXEC=""
# fi

FLAGS=(\
  --port "$PORT" \
  --server-settings "$CONFIG/server-settings.json" \
  --server-banlist "$CONFIG/server-banlist.json" \
  --rcon-port "$RCON_PORT" \
  --server-whitelist "$CONFIG/server-whitelist.json" \
  --use-server-whitelist \
  --server-adminlist "$CONFIG/server-adminlist.json" \
  --rcon-password "$(cat "$CONFIG/rconpw")" \
  --server-id /factorio/config/server-id.json \
)

if [ -n "$BIND" ]; then
  FLAGS+=( --bind "$BIND" )
fi

if [[ $LOAD_LATEST_SAVE == true ]]; then
    FLAGS+=( --start-server-load-latest )
else
    FLAGS+=( --start-server "$SAVE_FILE" )
fi

if [[ "${DEBUG:-false}" == false ]];then
    exec $SU_EXEC /factorio/bin/x64/factorio "${FLAGS[@]}" "$@"
else
    exec $SU_EXEC /factorio/bin/x64/factorio "${FLAGS[@]}" "$@" &
    tail -f /dev/null
fi

#### My old shiz