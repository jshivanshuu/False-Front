from profiling.signals import extract_signals
from profiling.scorer import score_behavior
from profiling.classifier import classify


def profile_session(session):

    signals = extract_signals(session)
    scores = score_behavior(signals)
    profile = classify(scores)

    return profile, signals, scores
