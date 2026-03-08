def score_behavior(signals):
    score = {
        "automation": 0,
        "low_skill": 0,
        "high_skill": 0,
        "benign": 0
    }

    attempts = signals["attempts"]
    avg_delay = signals["avg_delay"]
    pages = signals["pages_visited"]
    unique_pages = signals["unique_pages"]

    # Automation signals
    if attempts >= 5 and avg_delay is not None and avg_delay < 1:
        score["automation"] += 3

    if unique_pages <= 1 and attempts >= 5:
        score["automation"] += 2

    # Low-skill attacker signals
    if "/users" in pages and unique_pages > 2:
        score["low_skill"] += 3

    if attempts >= 3 and avg_delay is not None and avg_delay < 2:
        score["low_skill"] += 1

    # High-skill attacker signals
    if "/settings" in pages and avg_delay is not None and avg_delay > 1.5:
        score["high_skill"] += 3

    if unique_pages <= 2 and attempts >= 3:
        score["high_skill"] += 1

    # Benign signals
    if attempts <= 2 and (avg_delay is None or avg_delay > 3):
        score["benign"] += 3

    return score
