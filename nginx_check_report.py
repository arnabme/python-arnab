#!/usr/bin/env python3

import requests
import time
from datetime import datetime
import os

# Configuration
URL = "http://localhost"
LOG_FILE = "/var/log/py-http"

def log_to_file(message):
    try:
        with open(LOG_FILE, "a") as log_file:
            log_file.write(message + "\n")
    except PermissionError:
        print(f"[ERROR] Permission denied writing to {LOG_FILE}. Run as sudo/root.")
        exit(1)

def check_nginx():
    try:
        start = time.time()
        response = requests.get(URL, timeout=5)
        end = time.time()

        response_time_ms = round((end - start) * 1000, 2)
        status = response.status_code
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = f"{timestamp} | Status: {status} | Response Time: {response_time_ms} ms"
        print(log_entry)
        log_to_file(log_entry)

    except requests.exceptions.RequestException as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_message = f"{timestamp} | ERROR: {str(e)}"
        print(error_message)
        log_to_file(error_message)

if __name__ == "__main__":
    check_nginx()
