#!/bin/bash

if [[ ! -f .env ]]; then
  echo "Error: .env file not found"
  exit 1
fi

source .env

if [[ -z "$TELEGRAM_BOT_TOKEN" || -z "$DOMAIN" ]]; then
  echo "Error: TELEGRAM_BOT_TOKEN or DOMAIN is not set in the .env file."
  exit 1
fi

WEBHOOK_URL="https://$DOMAIN/telegram/webhook/"

echo "1) Set webhook"
echo "2) Get webhook"
echo "3) Delete webhook"
echo "4) Exit"
read -p "Your choice: " choice

case $choice in
    1)
        response=$(curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook" -d "url=$WEBHOOK_URL")
        echo -e "\n$response"
        ;;
    2)
        response=$(curl -s -X GET "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getWebhookInfo")
        echo -e "\n$response"
        ;;
    3)
        response=$(curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook?url=")
        echo -e "\n$response"
        ;;
    4)
        echo "Exiting"
        exit 0
        ;;
    *)
        echo "Invalid choice!"
        ;;
esac