from Profiling.signals import extract_signals
from Profiling.scorer import score_behavior
from Profiling.classifier import classify
from Profiling.ai_profiler import ai_profile_session


def profile_session(session):
    """
    Profiles the current session using the AI-powered profiler.
    Falls back to rule-based scoring automatically on any failure.

    Returns:
        profile (str)       : attacker classification label
        signals (dict)      : raw behavioral signals
        scores  (dict)      : rule-based scores (kept for dashboard compatibility)
        ai_result (dict)    : full AI profile with confidence, risk, reasoning
    """
    signals = extract_signals(session)

    # Rule-based scores — kept for backward compatibility with dashboard
    scores = score_behavior(signals)
    rule_profile = classify(scores)

    # AI-powered profile (with automatic fallback to rule-based)
    ai_result = ai_profile_session(signals, session)

    # Prefer AI result as the primary profile
    profile = ai_result.get("profile", rule_profile)

    return profile, signals, scores, ai_result
