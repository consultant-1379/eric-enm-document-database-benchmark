#!/bin/bash

while true; do
    result=$(curl -s -o /dev/null -w "%{http_code}" "http://$AGENT_HOSTNAME:$AGENT_PORT/start_request/$BENCH_GROUP/$BENCH_NAME")
    echo "Received $result response from server"
    ((result == 202)) && break
    echo "Retrying..."
    sleep 10
done