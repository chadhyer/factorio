FROM frolvlad/alpine-glibc:alpine-3.12

# Build vars
ARG VERSION=1.1.94
ARG RETRIES=5
ARG USER=factorio
ARG GROUP=factorio

# ENVIRONMENT VARIABLES
ENV VERSION=${VERSION} \
    SHA256=${SHA256} \
    PORT=24197 \
    RCON_PORT=25575 \
    BIN=/factorio/bin \
    CONFIG=/factorio/config \
    DATA=/opt/factorio/data \
    MODS=/factorio/mods \
    TEMP=/factorio/temp \
    SCENARIOS=/factorio/scenarios \
    SCRIPTOUTPUT=/factorio/script-output \
    SAVE=/factorio/saves

RUN set -ox pipefail \
    && archive=/tmp/factorio_headless_x64_${VERSION}.tar.xz \
    && mkdir -p /opt /factorio \
    && apk add --update --no-cache --no-progress \
        curl \
        bash \
        binutils \
        file \
        gettext \
        libintl \
    && curl -sSL "https://factorio.com/get-download/${VERSION}\
/headless/linux64" -o "$archive" --retry $RETRIES \
    && tar -xf "$archive" --directory /opt \
    && rm -rf "$archive" \
    && ln -s "$SCENARIOS" /opt/factorio/scenarios \
    && ln -s "$SAVE" /opt/factorio/saves \
    && mkdir -p ${CONFIG} \
    && mkdir -p ${DATA} \
    && mkdir -p ${MODS} \
    && mkdir -p ${TEMP} \
    && mkdir -p ${SCENARIOS} \
    && mkdir -p ${SCRIPTOUTPUT} \
    && mkdir -p ${SAVE} \
    && addgroup -S "$GROUP" \
    && adduser -S -G "$GROUP" -s /bin/sh -h /factorio "$USER"

COPY file/config.ini /factorio/config/config.ini
COPY file/*.sh /opt/factorio/
COPY file/*.template ${DATA}

RUN chmod +x /opt/factorio/*.sh \
    && chown -R "$USER":"$GROUP" /factorio /opt/factorio

USER ${USER}
WORKDIR /factorio
VOLUME /factorio
EXPOSE ${PORT}/udp ${RCON_PORT}/tcp
ENTRYPOINT ["/bin/bash"]
#CMD ["/opt/factorio/entrypoint.sh"]
