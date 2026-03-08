import json


LOG_FILE = "logs/requests.json"


def load_logs():
    logs = []

    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    except FileNotFoundError:
        pass

    return logs
