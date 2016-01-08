FROM fedora:23
MAINTAINER "Florian Ludwig" <f.ludwig@greyrook.com>

COPY ./install_fedora_deps.py /usr/local/bin/install_fedora_deps.py


RUN dnf -y update \
    && dnf -y install python-pip \
                      python-devel \
    && dnf clean all


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ONBUILD COPY requirements.txt /usr/src/app/
ONBUILD RUN install_fedora_deps.py requirements.txt \
            && pip install --no-cache-dir -r requirements.txt
