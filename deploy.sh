#!/bin/bash
set -e
STATE_FILE=/var/run/active_slot
ACTIVE=$(cat $STATE_FILE 2>/dev/null || echo "blue")
if [ "$ACTIVE" == "blue" ]; then
    NEW_SLOT="green"
    OLD_SLOT="blue"
    NEW_PORT=8011
    OLD_PORT=8010
else
    NEW_SLOT="blue"
    OLD_SLOT="green"
    NEW_PORT=8010
    OLD_PORT=8011
fi

update_env() {
    local slot=$1
    local url=$2
    local env_file=".env.$slot"
    
    # Create .env file if missing
    if [ ! -f "$env_file" ]; then
        touch "$env_file"
    fi
    
    # Update or add SITE_URL
    if grep -q "^SITE_URL=" "$env_file"; then
        sed -i "s|^SITE_URL=.*|SITE_URL=$url|" "$env_file"
    else
        echo "SITE_URL=$url" >> "$env_file"
    fi
}

deploy_test() {
    echo "Deploying new test version: $NEW_SLOT on port $NEW_PORT ..."
    # Pull latest code
    git fetch --depth=1 origin production
    git reset --hard origin/production
    
    # Set preview URL for new slot
    update_env "$NEW_SLOT" "https://preview.vibereach.gatara.org"
    
    # Start new slot
    docker compose up -d --build web_$NEW_SLOT
    
    # Health check
    until curl -s http://127.0.0.1:$NEW_PORT/health/ > /dev/null; do
        echo "Waiting for $NEW_SLOT to be healthy..."
        sleep 2
    done
    
    # Point preview domain
    sed -i "s/server 127.0.0.1:[0-9]*/server 127.0.0.1:$NEW_PORT/" \
        /etc/nginx/sites-available/preview.vibereach.gatara.org
    nginx -s reload
    echo "Preview domain now serving $NEW_SLOT ($NEW_PORT)."
}

promote() {
    echo "Promoting $NEW_SLOT to production on port $NEW_PORT ..."
    # Set production URL for new slot
    update_env "$NEW_SLOT" "https://vibereach.gatara.org"
    
    # Health check before switch
    until curl -s http://127.0.0.1:$NEW_PORT/health/ > /dev/null; do
        echo "Waiting for $NEW_SLOT to be healthy..."
        sleep 2
    done
    
    echo "Setting telegram webhook on $NEW_SLOT ..."
    docker compose exec web_$NEW_SLOT python manage.py set_telegram_webhook
    
    # Point production domain
    sed -i "s/server 127.0.0.1:[0-9]*/server 127.0.0.1:$NEW_PORT/" \
        /etc/nginx/sites-available/vibereach.gatara.org
    nginx -s reload
    echo "Production domain now serving $NEW_SLOT ($NEW_PORT)."
    
    # Save state
    echo "$NEW_SLOT" > $STATE_FILE
}

rollback() {
    echo "Rolling back to $OLD_SLOT on port $OLD_PORT ..."
    sed -i "s/server 127.0.0.1:[0-9]*/server 127.0.0.1:$OLD_PORT/" \
        /etc/nginx/sites-available/vibereach.gatara.org
    nginx -s reload
    echo "Rollback complete: production back to $OLD_SLOT ($OLD_PORT)."
}

cleanup() {
    # Cleanup old slot
    echo "Stopping old slot $OLD_SLOT ..."
    docker compose stop web_$OLD_SLOT
    docker compose rm -f web_$OLD_SLOT
    echo "Old slot $OLD_SLOT cleaned up."
}

case "$1" in
    test)
        deploy_test
        ;;
    promote)
        promote
        ;;
    rollback)
        rollback
        ;;
    cleanup)
        cleanup
        ;;
    *)
        echo "Usage: $0 {test|promote|rollback|cleanup}"
        exit 1
        ;;
esac