FROM ubuntu:20.04

# ENVIRONMENT VARIABLES FOR ROOT
ENV FACTORIO_VERSION=1.1.69
ENV FACTORIO_URL=https://factorio.com/get-download/${FACTORIO_VERSION}/headless/linux64 \
    FACTORIO_COMPRESSED=factorio_headless_x64_${FACTORIO_VERSION}.tar.xz

# Install basics
RUN apt update && apt install -y wget xz-utils net-tools vim

# Obtain/Uncompress Factorio server Files
WORKDIR /usr/local
RUN wget -O ${FACTORIO_COMPRESSED} ${FACTORIO_URL} &&\
    tar -xf ./${FACTORIO_COMPRESSED} && \
    rm -rf ${FACTORIO_COMPRESSED}

COPY ./factorio-entrypoint.sh /usr/local/factorio
RUN chmod +x /usr/local/factorio/factorio-entrypoint.sh

# Create User/Group that will execute the server
RUN groupadd factorio && useradd -rm -d /usr/local/factorio -g factorio factorio &&\
    chown -R factorio.factorio /usr/local/factorio
USER factorio
WORKDIR /usr/local/factorio

# ENVIRONMENT VARIABLES used to configure the factorio server
# They are all 'default' settings
# Override these with the docker-compose file to change the settings
# Highly recommended that you change the FACTORIO_GAME_PASSWORD
ENV FACTORIO_SAVE_FILE='world' \
    FACTORIO_NAME="MyFactorioServer" \
    FACTORIO_DESCRIPTION="A factorio server!" \
    FACTORIO_MAX_PLAYERS=0 \
    FACTORIO_PUBLIC=true \
    FACTORIO_LAN=true \
    FACTORIO_USERNAME="" \
    FACTORIO_PASSWORD="" \
    FACTORIO_TOKEN="" \
    FACTORIO_GAME_PASSWORD="CHANGEME!" \
    FACTORIO_REQUIRE_USER_VERIFICATION='true' \
    FACTORIO_MAX_UPLOAD_IN_KILOBYTES_PER_SECOND=0 \
    FACTORIO_MAX_UPLOAD_SLOTS=5 \
    FACTORIO_MINIMUM_LATENCY_IN_TICK=0 \
    FACTORIO_MAX_HEARTBEATS_PER_SECOND=60 \
    FACTORIO_IGNORE_PLAYER_LIMIT_FOR_RETURNING_PLAYERS='false' \
    FACTORIO_ALLOW_COMMANDS="admins-only" \
    FACTORIO_AUTOSAVE_INTERVAL=10 \
    FACTORIO_AUTOSAVE_SLOTS=5 \
    FACTORIO_AFK_AUTOKICK_INTERVAL=0 \
    FACTORIO_AUTO_PAUSE='true' \
    FACTORIO_ONLY_ADMINS_CAN_PAUSE_THE_GAME='true' \
    FACTORIO_AUTOSAVE_ONLY_ON_SERVER='true' \
    FACTORIO_NON_BLOCKING_SAVING='false' \
    FACTORIO_MINIMUM_SEGMENT_SIZE=25 \
    FACTORIO_MINIMUM_SEGMENT_SIZE_PEER_COUNT=20 \
    FACTORIO_MAXIMUM_SEGMENT_SIZE=100 \
    FACTORIO_MAXIMUM_SEGMENT_SIZE_PEER_COUNT=10

# Create Save Directory
RUN mkdir -p saves

#Copy Default server-settings into directory
COPY ./server-settings.json /usr/local/factorio/data/server-settings.json

# Start Server
EXPOSE 34197/udp
ENTRYPOINT ["./factorio-entrypoint.sh"]