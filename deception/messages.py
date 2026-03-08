import random
failure_messages = ["Invalid username or password", "Incorrect username or password", "Invalid credentials", "Incorrect username or password", "Invalid username or password"]
def get_failure_message():
    return random.choice(failure_messages)