FROM fedora:24
MAINTAINER "Florian Ludwig" <f.ludwig@greyrook.com>

COPY ./install_fedora_deps.py /usr/local/bin/install_fedora_deps.py


RUN dnf -y update \
    && dnf -y install python-pip \
                      python-devel \
    && dnf clean all


RUN mkdir -p /app && touch /app/pre-install.sh  && touch /app/after-install.sh && chmod +x /app/*.sh

WORKDIR /app
ONBUILD COPY requirements.txt /app/
ONBUILD RUN /app/pre-install.sh && \
            install_fedora_deps.py requirements.txt && \
            pip install -e /app && \
            pip install --no-cache-dir -r /app/requirements.txt && \
            /app/pre-install.sh
