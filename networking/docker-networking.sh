#! /bin/bash

docker network create --driver=bridge public
docker network create --driver=bridge --internal private
docker network create --driver=bridge gaming