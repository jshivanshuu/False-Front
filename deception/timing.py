
def calculate_delay(attempt_count, time_since_last):
    if attempt_count >= 3 and time_since_last < 9:
        return 3
    elif attempt_count >= 5 and time_since_last < 1:
        return 5
    return 0