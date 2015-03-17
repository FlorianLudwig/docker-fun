#!/bin/sh
set -e

## install
yum update -y
yum install -y httpd php php-gd php-mysqlnd

curl -L https://github.com/kelseyhightower/confd/releases/download/v0.7.1/confd-0.7.1-linux-amd64 -o /usr/local/bin/confd
chmod +x /usr/local/bin/confd


# apache config
rm /etc/httpd/conf.d/welcome.conf

## cleanup
yum clean all
