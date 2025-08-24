#!/bin/bash
set -e

STATE_FILE=/var/run/active_slot
ACTIVE=$(cat $STATE_FILE 2>/dev/null || echo "blue")

# Determine slots and ports
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

# Helper for colored output
print_status() {
    local status="$1"
    local message="$2"
    local color

    case "$status" in
        info)
            color="\033[34m" ;;   # Blue
        success)
            color="\033[32m" ;;   # Green
        error)
            color="\033[31m" ;;   # Red
        *)
            color="\033[0m" ;;
    esac

    echo -e "${color}${message}\033[0m"
}

update_env() {
    local slot=$1
    local url=$2
    local env_file=".env.$slot"

    if [ ! -f "$env_file" ]; then
        touch "$env_file"
    fi

    if grep -q "^SITE_URL=" "$env_file"; then
        sed -i "s|^SITE_URL=.*|SITE_URL=$url|" "$env_file"
    else
        echo "SITE_URL=$url" >> "$env_file"
    fi
}

deploy_test() {
    print_status info "Deploying new test version: $NEW_SLOT on port $NEW_PORT ..."
    
    git fetch --depth=1 origin production
    git reset --hard origin/production

    update_env "$NEW_SLOT" "https://preview.vibereach.gatara.org"

    docker compose up -d --build web_$NEW_SLOT

    until curl -s http://127.0.0.1:$NEW_PORT/health/ > /dev/null; do
        print_status info "Waiting for $NEW_SLOT to be healthy..."
        sleep 2
    done

    sed -i "s/server 127.0.0.1:[0-9]*/server 127.0.0.1:$NEW_PORT/" \
        /etc/nginx/sites-available/preview.vibereach.gatara.org
    nginx -s reload

    print_status success "Preview domain now serving $NEW_SLOT ($NEW_PORT)."
}

promote() {
    print_status info "Promoting $NEW_SLOT to production on port $NEW_PORT ..."

    update_env "$NEW_SLOT" "https://vibereach.gatara.org"

    until curl -s http://127.0.0.1:$NEW_PORT/health/ > /dev/null; do
        print_status info "Waiting for $NEW_SLOT to be healthy..."
        sleep 2
    done

    print_status info "Setting telegram webhook on $NEW_SLOT ..."
    docker compose exec web_$NEW_SLOT python manage.py set_telegram_webhook

    sed -i "s/server 127.0.0.1:[0-9]*/server 127.0.0.1:$NEW_PORT/" \
        /etc/nginx/sites-available/vibereach.gatara.org
    nginx -s reload

    print_status success "Production domain now serving $NEW_SLOT ($NEW_PORT)."

    echo "$NEW_SLOT" > $STATE_FILE
}

rollback() {
    print_status info "Rolling back to $OLD_SLOT on port $OLD_PORT ..."
    sed -i "s/server 127.0.0.1:[0-9]*/server 127.0.0.1:$OLD_PORT/" \
        /etc/nginx/sites-available/vibereach.gatara.org
    nginx -s reload
    print_status success "Rollback complete: production back to $OLD_SLOT ($OLD_PORT)."
}

cleanup() {
    print_status info "Stopping old slot $OLD_SLOT ..."
    docker compose stop web_$OLD_SLOT
    docker compose rm -f web_$OLD_SLOT
    print_status success "Old slot $OLD_SLOT cleaned up."
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
        print_status error "Usage: $0 {test|promote|rollback|cleanup}"
        exit 1
        ;;
esac
