FROM debian:wheezy

RUN set -ex; \
    apt-get update -qq; \
    apt-get install -y \
        locales \
        gcc \
        make \
        zlib1g \
        zlib1g-dev \
        libssl-dev \
        git \
        ca-certificates \
        curl \
        libsqlite3-dev \
    ; \
    rm -rf /var/lib/apt/lists/*

# Build Python 2.7.9 from source
RUN set -ex; \
    curl -L https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz | tar -xz; \
    cd Python-2.7.9; \
    ./configure --enable-shared; \
    make; \
    make install; \
    cd ..; \
    rm -rf /Python-2.7.9

# Make libpython findable
ENV LD_LIBRARY_PATH /usr/local/lib

# Install setuptools
RUN set -ex; \
    curl -L https://bootstrap.pypa.io/ez_setup.py | python

# Install pip
RUN set -ex; \
    curl -L https://pypi.python.org/packages/source/p/pip/pip-8.1.1.tar.gz | tar -xz; \
    cd pip-8.1.1; \
    python setup.py install; \
    cd ..; \
    rm -rf pip-8.1.1

WORKDIR /code/

RUN pip install virtualenv \
    && virtualenv /code/venv \
    && /code/venv/bin/pip install pyinstaller==3.1.1

ENTRYPOINT ["/code/entry.sh"]
