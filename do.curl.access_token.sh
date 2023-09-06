#!/bin/sh

ACCESS_TOKEN=$(curl --silent -X 'POST' \
  'http://todo.yops.fun:8000/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=roybebru%40gmail.com&password=123456&scope=&client_id=&client_secret=' \
| jq '.access_token' | cut -d\" -f2)

echo "ACCESS_TOKEN=$ACCESS_TOKEN" > ./ACCESS_TOKEN.sh
