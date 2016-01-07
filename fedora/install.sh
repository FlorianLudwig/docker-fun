#!/bin/sh
set -e

## install
dnf update -y

## cleanup
dnf clean all
rm /install.sh
rm -rf /tmp/*

# more candidates for cleanup
# /var/lib/yum/history/
# 
