#!/bin/bash

set -e
set -x  # Debugowanie - wyświetla każdą komendę przed wykonaniem

APP_VERSION=$1

if [ -z "$APP_VERSION" ]; then
  echo "Podaj wersję jako argument. Przykład: ./developer.sh 1.0.1"
  exit 1
fi

LOG_FILE="../deploy.log"  # Plik logów w katalogu nadrzędnym

echo ">>> Ubijanie kontenerów (jeśli istnieją)..."
docker-compose --env-file ../env/dev.env -f ../dev.docker-compose.yaml down

echo ">>> Budowanie obrazu z wersją: $APP_VERSION..."
APP_VERSION=${APP_VERSION} docker-compose --env-file ../env/dev.env -f ../dev.docker-compose.yaml build --build-arg APP_VERSION=${APP_VERSION}

echo ">>> Uruchamianie nowych kontenerów..."
docker-compose --env-file ../env/dev.env -f ../dev.docker-compose.yaml up -d

echo ">>> Usuwanie nieużywanych obrazów..."
docker image prune -f

DEPLOY_DATE=$(date '+%Y-%m-%d %H:%M:%S')
DEPLOY_MESSAGE="Wdrożenie zakończone pomyślnie. Wersja: $APP_VERSION, Data: $DEPLOY_DATE"

echo ">>> $DEPLOY_MESSAGE"

# Dodanie loga do pliku
echo "$DEPLOY_MESSAGE" >> "$LOG_FILE"
