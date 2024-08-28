#!/bin/bash

while true; do
  pgready=$(pg_isready -p 5432  -h postgres -U postgres)
  echo $pgready
  if [ "$pgready" = "postgres:5432 - accepting connections" ]; then
            echo "postgres is up and running"
            exit 0;
  fi
done
