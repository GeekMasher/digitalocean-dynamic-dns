#!/bin/bash

set -e

echo "Starting do-dynamic-dns container..."

declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env

# Setup a cron schedule for every hour
echo "SHELL=/bin/bash
BASH_ENV=/container.env
*/60 * * * * python /app/do-dynamic-dns.py >> /var/log/cron.log 2>&1" > scheduler.txt

# Run once
python /app/do-dynamic-dns.py

echo "Starting cron..."

crontab scheduler.txt
cron -f
