def extractsignals(session_data):
     """
    Extract behavioral signals from session data.

    session_data should include:
    - attempts
    - timestamps (list of request times)
    - pages_visited (list of paths)
    """
    
    timestamps = session_data.get("timestamps", [])
    pages = session_data.get("pages_visited", [])
    attempts = session_data.get("attempts",0)

    avg_delay = None
    if len(timestamps) > 1:
        deltas = [ timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
        avg_delay = sum(deltas) / len(deltas)
    return {
        "avg_delay": avg_delay,
        "pages_visited": pages,
        "attempts": attempts,
        "unique_pages": len(set(pages))
    }