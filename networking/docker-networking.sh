#! /bin/bash

# Public network with proxy connection
docker network create --driver=bridge public
# Private network without internet connection
docker network create --driver=bridge --internal private
# Public network with tcp/udp open ports on host
docker network create --driver=bridge on_tcp