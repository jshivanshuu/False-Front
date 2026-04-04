import time
import uuid
from flask import session


def ensure_session():
    if "id" not in session:
        session["id"] = str(uuid.uuid4())
        session["attempts"] = 0
        session["last_attempt_time"] = time.time()
        session["timestamps"] = []
        session["pages_visited"] = []
        session["fake_used"] = False


def update_behavior(path):
    session["timestamps"].append(time.time())
    session["pages_visited"].append(path)

