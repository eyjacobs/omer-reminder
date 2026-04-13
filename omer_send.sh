#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
source "$DIR/config.sh"

python3 - "$1" "$PHONE" "$GMAIL_USER" "$APP_PASSWORD_FILE" <<'EOF'
import smtplib, sys, os
from email.mime.text import MIMEText
from datetime import datetime

day, phone, gmail_user, password_file = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
gmail_password = open(os.path.expanduser(password_file)).read().strip()

carrier_number = phone.replace("+1", "").replace("-", "").replace(" ", "")
to_sms = f"{carrier_number}@tmomail.net"

msg = MIMEText(f"Don't forget to count! Day {day}")
msg["Subject"] = ""
msg["From"] = gmail_user
msg["To"] = to_sms

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(gmail_user, gmail_password)
        smtp.send_message(msg)
    result = f"SUCCESS: Day {day} sent"
except Exception as e:
    result = f"ERROR: Day {day} - {e}"

with open(os.path.expanduser("~/omer_log.txt"), "a") as f:
    f.write(f"{datetime.now()}: {result}\n")
EOF
