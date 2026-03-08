from collections import defaultdict


def group_by_session(logs):
    sessions = defaultdict(list)

    for entry in logs:
        sid = entry.get("session_id")
        if sid:
            sessions[sid].append(entry)

    return sessions


def build_timelines(sessions):
    timelines = {}

    for sid, entries in sessions.items():
        entries.sort(key=lambda x: x["timestamp"])

        paths = [e["path"] for e in entries]

        timelines[sid] = paths

    return timelines


def count_paths(logs):
    counts = defaultdict(int)

    for entry in logs:
        path = entry.get("path")
        if path:
            counts[path] += 1

    return dict(counts)
