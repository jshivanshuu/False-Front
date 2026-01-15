from messages import get_failure_message
from timing import calculate_delay
from fakesuccess import fakeadminlogin
import time
def decide(session_data):
    now = time.time()
    last_time = session_data.get('last_attempt_time' , now)
    attempts = session_data.get("attempts",0)
    time_since_last = now - last_time
    delay = calculate_delay(attempts, time_since_last)
    fake_success = fakeadminlogin(attempts, time_since_last)
    return {
        "delay": delay,
        "fake_success": fake_success,
        "message": get_failure_message()
    }
    