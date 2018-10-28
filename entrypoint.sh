#!/bin/sh
set -e

# wait for postgres and rabbitmq to come online
sleep 30

exec "$@"