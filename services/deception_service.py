import time
from deception.decision_engine import decide


def handle_deception(session):

    session["attempts"] += 1

    plan = decide({
        "attempts": session["attempts"],
        "last_attempt_time": session["last_attempt_time"]
    })

    session["last_attempt_time"] = time.time()

    return plan
