```markdown
# 📌 FalseFront — Deception-Based Web Security System
```

FalseFront is a modular, behavior-driven web security system that uses deception, decoy environments, and attacker profiling to analyze malicious activity at the application layer.

Instead of blocking attackers immediately, FalseFront observes, misleads, and studies them to extract intelligence.

🚀 Features

✅ Passive Request Logging (Module 1)

✅ Behavior-Based Deception (Module 2)

✅ Decoy Internal Environment (Module 3)

✅ Attacker Profiling Engine (Module 4)

✅ Security Visualization Dashboard (Module 5)

✅ Modular, Scalable Architecture

🧠 System Architecture
Request
   ↓
Observation Layer
   ↓
Deception Engine
   ↓
Decoy Environment
   ↓
Behavior Profiling
   ↓
Security Dashboard


Each layer is independent and modular to ensure maintainability and clarity.

📂 Project Structure
False-Front/
│
├── app.py                 # Main application
│
├── core/                  # Core utilities
│   ├── session.py
│   └── config.py
│
├── entry/                 # Observation module
│   └── observer.py
│
├── deception/             # Deception engine
│
├── profiling/             # Attacker profiling
│
├── services/              # Service layer
│
├── dashboard/             # Log analytics
│
├── templates/             # HTML templates
│
├── logs/                  # Runtime logs (ignored in git)
│
└── requirements.txt

⚙️ Technologies Used

Python 3

Flask

JSON (log storage)

HTML / CSS

Jinja2 Templates

🛠️ Installation
1. Clone Repository
git clone https://github.com/your-username/FalseFront.git
cd FalseFront

2. Create Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Run Application
python app.py


Access:

http://127.0.0.1:5000/login

🔍 How It Works
Module 1 — Observation

Logs every incoming request with metadata such as timestamp, session ID, route, and method.

Module 2 — Deception

Applies:

Artificial delays

Rotating error messages

Fake authentication success

Based on user behavior.

Module 3 — Decoy Environment

Redirects suspicious users to fake internal pages to observe post-compromise behavior.

Module 4 — Profiling

Classifies attackers as:

Automation

Low-skill

High-skill

Benign

Using rule-based behavioral analysis.

Module 5 — Dashboard

Provides visualization of:

Session timelines

Route usage

Attack patterns

Available at:

/admin/dashboard

📊 Profiling Debug Endpoint

For development and testing:

/profile_session


Returns behavioral analysis for the current session.

🔐 Security Philosophy

FalseFront follows a deception-first security model:

No immediate blocking

No alerting attackers

No visible defense mechanisms

Maximum intelligence extraction

This approach improves attacker understanding and reduces detection risk.

🧪 Testing

Recommended tests:

Rapid login attempts (automation simulation)

Slow manual navigation

Decoy exploration

Dashboard inspection

Verify:

Logs are consistent

Deception triggers correctly

Profiles match behavior

📈 Future Enhancements

Blockchain-backed log integrity

Machine learning profiling

Automated report generation

Advanced visualization

Threat intelligence integration

📄 License

This project is licensed under the MIT License.

👤 Author

Shivanshu Jha
Engineering Student | Cybersecurity Enthusiast

⭐ Acknowledgements

Inspired by modern honeypot systems, deception technologies, and behavioral security research.

📝 Disclaimer

This project is intended for educational and research purposes only.

Do not deploy in production environments without proper security review.