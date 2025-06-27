# utils/logger.py

import datetime
import os

LOG_FILE = "logs/session_log.txt"

def log_event(event_type, message):
    timestamp = datetime.datetime.utcnow().isoformat()
    log_entry = f"[{timestamp}] [{event_type.upper()}] {message}\n"
    print(log_entry.strip())  # Optional: console output for live feedback

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
