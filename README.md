# FalseFront — Deception-Based Web Security System

> A modular honeypot that silently **observes**, **misleads**, and **profiles** attackers instead of blocking them — extracting maximum intelligence while staying invisible.

---

## How It Works

```
HTTP Request
    ↓
Observation Layer    →  Logs IP, path, user-agent, payload size, timestamps
    ↓
Deception Engine     →  Artificial delays · Rotating error messages · Fake success redirect
    ↓
Decoy Environment    →  Fake internal dashboard, users, settings pages
    ↓
Attacker Profiling   →  Rule-based scoring + Claude AI classification
    ↓
Admin Dashboard      →  Real-time session timelines, route usage, attack patterns
```

Each layer is fully independent and modular.

---

## Features

Module | Description
--- | ---
**Observation** | Logs every request with timestamp, session ID, route, method, IP, user-agent
**Deception Engine** | Applies delays, rotating error messages, and fake-success redirects based on behavior
**Decoy Environment** | Serves convincing fake internal pages (`/dashboard`, `/users`, `/settings`)
**Attacker Profiling** | Classifies sessions as `automation`, `low_skill`, `high_skill`, or `benign`
**AI Profiling** | Uses Claude API for rich behavioral analysis with rule-based fallback
**Admin Dashboard** | Visualizes session timelines, route usage, and attack patterns at `/admin/dashboard`

---

## Attacker Profiles

Profile | Description
--- | ---
`automation` | Bots, scanners, credential stuffing tools — fast, repetitive, uniform timing
`low_skill` | Human attacker using basic techniques, exploring naively
`high_skill` | Methodical and patient — mimics normal user behaviour to avoid detection
`benign` | Likely a legitimate or curious user

---

## Tech Stack

- **Python 3** + **Flask**
- **python-dotenv** for environment variable loading
- **JSON** log storage
- **Jinja2** templates
- **Claude API** (Anthropic) for AI-powered profiling

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/jshivanshuu/False-Front.git
cd False-Front
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env and set your FALSEFRONT_SECRET_KEY and ANTHROPIC_API_KEY
```

The app uses `python-dotenv` and will automatically load your `.env` file on startup.

### 5. Run the Application
```bash
# Development mode (enables debug, allows missing secret key)
APP_ENV=development python app.py

# Production mode (requires FALSEFRONT_SECRET_KEY to be set)
python app.py
```

Access at: `http://127.0.0.1:5000/login`

---

## Key Endpoints

Route | Description
--- | ---
`/login` | Entry point — deception triggers on repeated attempts
`/dashboard` | Decoy internal dashboard (shown to suspected attackers)
`/users` | Decoy users page
`/settings` | Decoy settings page
`/profile_session` | Debug endpoint — returns AI/rule-based behavioral analysis for current session
`/admin/dashboard` | Real admin panel — session timelines, route usage, attack patterns

---

## Security Philosophy

FalseFront follows a **deception-first** model:

- ❌ No immediate blocking
- ❌ No alerting the attacker
- ❌ No visible defense mechanisms
- ✅ Maximum intelligence extraction

The attacker believes they are interacting with a real system while every action is logged and analyzed.

---

## Testing

Simulate different attacker profiles:

- **Automation:** Rapid repeated login attempts with minimal delay
- **Low-skill:** Manual exploration of decoy pages after a few failed logins
- **High-skill:** Slow, deliberate navigation that mimics real user behaviour
- **Benign:** 1–2 requests with natural timing

Verify via `/profile_session` and `/admin/dashboard`.

---

## Future Enhancements

- [ ] Authentication on `/admin/dashboard`
- [ ] ML-based profiling with training data from logs
- [ ] Log rotation and archival
- [ ] Automated threat report generation
- [ ] Threat intelligence feed integration
- [ ] Blockchain-backed log integrity

---

## Author

**Shivanshu Jha**
Engineering Student · Cybersecurity Enthusiast

---

## Acknowledgements

Inspired by modern honeypot systems, deception technologies, and behavioural security research.

---

> **Disclaimer:** This project is intended for educational and research purposes only.
