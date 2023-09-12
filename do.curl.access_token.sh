#!/bin/sh

ACCESS_TOKEN=$(curl --silent -X 'POST' \
  'http://localhost:8000/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=roybebru%40gmail.com&password=123456' \
| jq '.access_token' | cut -d\" -f2)

echo "ACCESS_TOKEN=$ACCESS_TOKEN" > ./ACCESS_TOKEN.sh

echo "Bearer $ACCESS_TOKEN"
