import json
import urllib.request
import urllib.error


ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-20250514"

SYSTEM_PROMPT = """You are a cybersecurity analyst embedded in a deception-based honeypot system called FalseFront.
Your job is to analyse attacker behavioral signals and classify the session.

You will receive JSON behavioral data from a session and must respond ONLY with a valid JSON object.
Do not include any explanation, markdown, or text outside the JSON.

Classify the session into ONE of these profiles:
- "automation"   : Bots, scanners, credential stuffing tools — fast, repetitive, uniform timing
- "low_skill"    : Human attacker using basic techniques, exploring naively, inconsistent behaviour
- "high_skill"   : Methodical, patient, deliberate — mimics normal user behaviour to avoid detection
- "benign"       : Likely a legitimate or curious user, no clear attack pattern

Return this exact JSON structure:
{
  "profile": "<one of the four labels above>",
  "confidence": <integer 0-100>,
  "risk_level": "<low|medium|high|critical>",
  "reasoning": "<2-3 sentences explaining your classification based on the signals>",
  "key_indicators": ["<indicator 1>", "<indicator 2>", "<indicator 3>"]
}"""


def build_prompt(signals: dict, session_meta: dict) -> str:
    data = {
        "behavioral_signals": {
            "login_attempts": signals.get("attempts", 0),
            "average_delay_between_requests_seconds": round(signals.get("avg_delay") or 0, 3),
            "pages_visited_sequence": signals.get("pages_visited", []),
            "unique_pages_visited": signals.get("unique_pages", 0),
        },
        "session_meta": {
            "total_requests": session_meta.get("total_requests", 0),
            "session_duration_seconds": round(session_meta.get("duration", 0), 2),
            "fake_success_triggered": session_meta.get("fake_used", False),
            "reached_decoy_environment": session_meta.get("reached_decoy", False),
        }
    }
    return f"Analyse this honeypot session and classify the attacker:\n\n{json.dumps(data, indent=2)}"


def call_claude(prompt: str) -> dict:
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 1000,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")

    req = urllib.request.Request(
        ANTHROPIC_API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=10) as resp:
        body = json.loads(resp.read().decode("utf-8"))

    raw_text = body["content"][0]["text"].strip()

    # Strip markdown fences if present
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]

    return json.loads(raw_text.strip())


def ai_profile_session(signals: dict, session: dict) -> dict:
    """
    Main entry point. Returns a rich AI profile dict.
    Falls back to rule-based classifier on any failure.
    """
    pages = signals.get("pages_visited", [])
    session_meta = {
        "total_requests": len(session.get("timestamps", [])),
        "duration": (
            session["timestamps"][-1] - session["timestamps"][0]
            if len(session.get("timestamps", [])) > 1 else 0
        ),
        "fake_used": session.get("fake_used", False),
        "reached_decoy": "/dashboard" in pages or "/users" in pages or "/settings" in pages,
    }

    try:
        prompt = build_prompt(signals, session_meta)
        result = call_claude(prompt)

        # Validate expected keys are present
        required = {"profile", "confidence", "risk_level", "reasoning", "key_indicators"}
        if not required.issubset(result.keys()):
            raise ValueError("Incomplete response from AI")

        result["source"] = "ai"
        return result

    except (urllib.error.URLError, TimeoutError) as e:
        return _fallback_profile(signals, reason=f"Network error: {e}")
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        return _fallback_profile(signals, reason=f"Parse error: {e}")
    except Exception as e:
        return _fallback_profile(signals, reason=f"Unexpected error: {e}")


def _fallback_profile(signals: dict, reason: str = "AI unavailable") -> dict:
    """Rule-based fallback — mirrors the original scorer logic."""
    from Profiling.scorer import score_behavior
    from Profiling.classifier import classify

    scores = score_behavior(signals)
    profile = classify(scores)

    risk_map = {
        "automation": "critical",
        "high_skill": "high",
        "low_skill": "medium",
        "benign": "low"
    }

    return {
        "profile": profile,
        "confidence": 60,
        "risk_level": risk_map.get(profile, "medium"),
        "reasoning": f"Classified using rule-based fallback. ({reason})",
        "key_indicators": [
            f"{signals.get('attempts', 0)} login attempts",
            f"avg delay {round(signals.get('avg_delay') or 0, 2)}s",
            f"{signals.get('unique_pages', 0)} unique pages visited"
        ],
        "source": "fallback"
    }
