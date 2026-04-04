
def calculate_delay(attempt_count, time_since_last):
    # Check stricter threshold first — otherwise the >= 5 branch is unreachable
    if attempt_count >= 5 and time_since_last < 1:
        return 5
    elif attempt_count >= 3 and time_since_last < 9:
        return 3
    return 0