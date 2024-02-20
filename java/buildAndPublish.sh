#!/bin/bash

# Build Maven project
mvn clean install -DskipTests=true
echo "Maven build finished"

# Build Docker image locally
docker build -t scrapper-image .
echo "Docker build finished"

# Run Docker image locally
docker run -p 8080:8080 \
  -v /snap/bin/chromium.chromedriver:/usr/local/bin \
  -e DB_URL="jdbc:mysql://192.168.69.207:3306/scrapper" \
  -e DB_USER="scrapper" \
  -e DB_PASS="trustno1x" \
  -e DB_MIN_CONN="1" \
  -e DB_MAX_CONN="10" \
  -e DB_MAX_STS="100" \
  scrapper-image

echo "Docker image started locally"

