# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

FROM ghcr.io/anaticulae/baw:0b21f1b-test

COPY /requirements.txt\
     /requirements.dev\
        /var/install/

WORKDIR /var/install

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt &&\
    pip install -r requirements.dev

COPY . /var/install

# TODO: Remove no-build later
RUN pip install . --no-build-isolation

ENTRYPOINT ["sh", "-c"]
