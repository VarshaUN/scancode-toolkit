#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

FROM --platform=linux/amd64 python:3.12-slim-bookworm

# OCI Labels 
LABEL org.opencontainers.image.title="ScanCode Toolkit" 
LABEL org.opencontainers.image.description="ScanCode Toolkit for code scanning and analysis." 
LABEL org.opencontainers.image.url="https://github.com/nexB/scancode-toolkit" 
LABEL org.opencontainers.image.source="https://github.com/nexB/scancode-toolkit" 
LABEL org.opencontainers.image.documentation="https://scancode-toolkit.readthedocs.io/"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.authors="https://github.com/nexB/scancode-toolkit"
LABEL org.opencontainers.image.version="v32.3.0"
LABEL org.opencontainers.image.vendor="nexB Inc."
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.ref.name="latest"


# Python settings: Force unbuffered stdout and stderr (i.e. they are flushed to terminal immediately)
ENV PYTHONUNBUFFERED 1
# Python settings: do not write pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# OS requirements as per
# https://scancode-toolkit.readthedocs.io/en/latest/getting-started/install.html
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
       bzip2 \
       xz-utils \
       zlib1g \
       libxml2-dev \
       libxslt1-dev \
       libgomp1 \
       libsqlite3-0 \
       libgcrypt20 \
       libpopt0 \
       libzstd1 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create directory for scancode sources
WORKDIR /scancode-toolkit

# Copy sources into docker container
COPY . /scancode-toolkit

# Initial configuration using ./configure, scancode-reindex-licenses to build
# the base license index
RUN ./configure \
 && ./venv/bin/scancode-reindex-licenses

# Add scancode to path
ENV PATH=/scancode-toolkit:$PATH

# Set entrypoint to be the scancode command, allows to run the generated docker
# image directly with the scancode arguments: `docker run (...) <containername> <scancode arguments>`
ENTRYPOINT ["./scancode"]
