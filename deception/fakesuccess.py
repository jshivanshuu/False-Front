def fakeadminlogin(attempt_count, time_since_last):
    if attempt_count >= 3 and time_since_last < 9:
        return True
    else:
        return False