#!/bin/bash

# start confd
confd $CONFD_OPT &


# cleanup from
rm -rf /run/httpd/*

exec /usr/sbin/apachectl -D FOREGROUND
