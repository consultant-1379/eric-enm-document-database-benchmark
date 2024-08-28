#!/bin/bash

while true; do
    result=$(curl -s -o /dev/null -w "%{http_code}" "http://$ORCH_HOSTNAME:$ORCH_PORT/ready")
    echo "Received $result response from server"
    ((result == 202)) && break
    echo "Retrying..."
    sleep 5
done