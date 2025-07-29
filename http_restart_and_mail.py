#!/usr/bin/env python3

import subprocess
import time
import smtplib
from datetime import datetime
from email.message import EmailMessage
import requests

LOG_PATH = "/var/log/py-http"
URL = "http://localhost"
RETRY_COUNT = 5
RETRY_WAIT = 5  # seconds

# --- Configure your email details here ---
EMAIL_FROM = "your_email@example.com"
EMAIL_TO = "admin@example.com"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "your_email@example.com"
SMTP_PASS = "your_smtp_password"
# ----------------------------------------

def restart_nginx():
    try:
        print("[ACTION] Restarting nginx...")
        subprocess.run(["systemctl", "restart", "nginx"], check=True)
        print("[INFO] nginx restarted.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to restart nginx: {e}")

def check_http_status():
    try:
        response = requests.get(URL, timeout=5)
        return response.status_code
    except Exception as e:
        print(f"[ERROR] Exception during HTTP check: {e}")
        return None

def send_email_alert():
    msg = EmailMessage()
    msg["Subject"] = "ALERT: NGINX not serving HTTP 200"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.set_content(f"""
NGINX failed to return HTTP 200 after {RETRY_COUNT} retries.

Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
URL Checked: {URL}
Log File: {LOG_PATH}
""")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)
        print(f"[INFO] Alert email sent to {EMAIL_TO}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

def parse_last_status():
    try:
        with open(LOG_PATH, "r") as log:
            lines = log.readlines()
            if not lines:
                print("[WARN] Log file is empty.")
                return None
            last_line = lines[-1]
            if "Status:" in last_line:
                parts = last_line.split("Status:")
                status_part = parts[1].split("|")[0].strip()
                return int(status_part)
            else:
                return None
    except FileNotFoundError:
        print(f"[ERROR] Log file not found: {LOG_PATH}")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to read log: {e}")
        return None

def main():
    status = parse_last_status()
    if status == 200:
        print("[OK] Last HTTP status is 200. All good.")
        return

    print(f"[WARN] Last status not 200 (got {status}). Starting retries...")

    for attempt in range(RETRY_COUNT):
        restart_nginx()
        time.sleep(RETRY_WAIT)
        new_status = check_http_status()

        if new_status == 200:
            print(f"[RECOVERED] HTTP 200 OK after {attempt + 1} retry(ies).")
            return
        else:
            print(f"[RETRY {attempt + 1}] Still not 200 (got {new_status})...")

    # If here, all retries failed
    print("[FAIL] HTTP status not 200 after all retries. Sending alert...")
    send_email_alert()

if __name__ == "__main__":
    main()
