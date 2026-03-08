def extract_signals(session_data):
    """
    Extract behavioral signals from session data.

    session_data should include:
    - attempts
    - timestamps (list of request times)
    - pages_visited (list of paths)
    """

    timestamps = session_data.get("timestamps", [])
    pages = session_data.get("pages_visited", [])
    attempts = session_data.get("attempts", 0)

    avg_delay = None
    if len(timestamps) > 1:
        deltas = []
        for i in range(1, len(timestamps)):
            deltas.append(timestamps[i] - timestamps[i - 1])

        avg_delay = sum(deltas) / len(deltas)

    return {
        "attempts": attempts,
        "pages_visited": pages,
        "avg_delay": avg_delay,
        "unique_pages": len(set(pages))
    }
