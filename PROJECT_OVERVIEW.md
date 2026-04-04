# 📌 FalseFront — Project Overview

## What It Is
FalseFront is a **deception-based web honeypot** built with Python + Flask. Instead of blocking attackers, it silently observes, misleads, and profiles them — then logs everything for analysis.

---

## 🗂️ Module Breakdown

| Module | Folder | Purpose | Status |
|---|---|---|---|
| **Observation** | `Entry/` | Logs every HTTP request (IP, path, user-agent, payload size, timestamp) to `logs/requests.json` | ✅ Working |
| **Session Core** | `core/` | Manages Flask session state: attempts, timestamps, pages visited, fake_used flag | ✅ Working |
| **Deception Engine** | `deception/` | Applies artificial delays, rotating error messages, fake-success redirects based on behavior | ✅ Working |
| **Profiling (Rule-based)** | `Profiling/` | Extracts signals → scores → classifies into: `automation`, `low_skill`, `high_skill`, `benign` | ✅ Working |
| **AI Profiler** | `Profiling/ai_profiler.py` | Sends behavioral signals to Claude API for richer classification; falls back to rule-based on failure | ✅ Working |
| **Decoy Environment** | `templates/decoy/` | Fake dashboard/users/settings pages to trap and observe post-compromise exploration | ✅ Working |
| **Admin Dashboard** | `dashboard/` + `templates/admin/` | Real-time visualization of request logs, session timelines, route usage | ✅ Working |
| **Service Layer** | `services/` | Thin wrappers that connect `deception` and `profiling` modules to `app.py` | ✅ Working |

---

## 🧱 Architecture Flow

```
HTTP Request
    ↓
Entry/observer.py     → logs to logs/requests.json
    ↓
core/session.py       → initialises/updates session state
    ↓
deception/            → calculates delay + fake_success + error message
    ↓
Profiling/            → extracts signals → scores → classifies attacker
    ↓
templates/decoy/      → serves fake internal environment to suspected attackers
    ↓
dashboard/            → admin can view all activity in real time
```

---

## 📊 Project Level Assessment

**Overall Level: Intermediate (Early-Stage Research Tool)**

| Area | Rating | Notes |
|---|---|---|
| Architecture | ⭐⭐⭐⭐ | Clean modular separation, good service layer pattern |
| Deception Logic | ⭐⭐⭐ | Functional but very basic (only 3 triggers) |
| AI Integration | ⭐⭐⭐⭐ | Claude API with graceful fallback — solid pattern |
| Security of the App Itself | ⭐⭐ | Hardcoded secret key, debug=True in production, no auth on /admin |
| Code Quality | ⭐⭐⭐ | Some inconsistent style, duplicate file (`profiling service.py`), empty stub files |
| Testing | ⭐ | No tests at all |
| Documentation | ⭐⭐⭐⭐ | Good README but some details outdated |

---

## 🔧 What Should Be Changed (Priority Order)

### 🔴 Critical (Security)
1. **Hardcoded secret key** — `core/config.py` has `SECRET_KEY = "Falsefront"` in plaintext. Move to `.env` / environment variable.
2. **`debug=True` in production** — `app.py` runs with `debug=True` unconditionally. Only enable in dev mode.
3. **No auth on `/admin/dashboard`** — Anyone can access the real admin dashboard. Add a simple password gate or IP allowlist.
4. **API key missing** — `ai_profiler.py` never injects the `x-api-key` header for Anthropic, so AI calls will always fail silently and fall back.

### 🟡 Bugs / Broken Code
5. **Import casing mismatch** — `services/profiling_service.py` imports from `profiling.signals` (lowercase) but the folder is `Profiling/` (uppercase). This will crash on case-sensitive file systems (Linux/Docker).
6. **Duplicate file** — `services/profiling service.py` (with a space in the name) is a copy of `profiling_service.py`. Should be deleted.
7. **Empty stub files** — `Entry/routes.py`, `Entry/session_manager.py`, `core/tracker.py` are empty stubs. Either implement them or remove them.
8. **`timing.py` logic order is wrong** — The `>= 5 and < 1` check (line 5) is unreachable because `>= 3 and < 9` (line 3) always matches first.

### 🟢 Improvements
9. **Add `requirements.txt`** — Not present in the repo; other developers can't install dependencies.
10. **Add `.env.example`** — Document required environment variables (SECRET_KEY, ANTHROPIC_API_KEY).
11. **Session ID is weak** — `str(id(session))` is not cryptographically random. Use `uuid.uuid4()`.
12. **Log rotation** — `logs/requests.json` grows forever. Add rotation or a max size limit.
