import json
import time
from pathlib import Path
LOG_FILE = Path("logs/requests.json")
def observe_request(request,session_id = None):
    record = {
        "timestamp" : time.time(),
        "path": request.path,
        "method" : request.method,
        "ip" : request.remote_addr,
        "session_id" : session_id,
        "useragent" : request.headers.get("User-Agent"),
        "Payload_size" : len(request.get_data())
    }
    LOG_FILE.parent.mkdir(exist_ok=True)
    with LOG_FILE.open("a") as f:
        f.write(json.dumps(record))
        f.write("\n")