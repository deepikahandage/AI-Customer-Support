import json
import os
import time
from datetime import datetime


LOG_FILE = "workflow_logs.json"


def log_workflow(
    customer_message,
    status,
    response="",
    error="",
    duration=0
):
    """Store workflow activity and performance information."""

    log_entry = {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "customer_message": customer_message,
        "status": status,
        "response": response,
        "error": error,
        "duration_seconds": round(duration, 2)
    }

    logs = []

    if os.path.exists(LOG_FILE):

        try:
            with open(
                LOG_FILE,
                "r",
                encoding="utf-8"
            ) as file:
                logs = json.load(file)

        except (json.JSONDecodeError, OSError):
            logs = []

    logs.append(log_entry)

    with open(
        LOG_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            logs,
            file,
            indent=4,
            ensure_ascii=False
        )


def get_workflow_logs():

    if not os.path.exists(LOG_FILE):
        return []

    try:

        with open(
            LOG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return []