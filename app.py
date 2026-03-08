from flask import Flask, render_template, request, session, redirect
import time

# Core
from core.session import ensure_session, update_behavior
from core.config import SECRET_KEY

# Logging
from Entry.observer import observe_request

# Services
from services.deception_service import handle_deception
from services.profiling_service import profile_session

# Dashboard
from dashboard.parser import load_logs
from dashboard.analytics import group_by_session, build_timelines, count_paths


app = Flask(__name__)
app.secret_key = SECRET_KEY


# ---------------- Home ----------------

@app.route("/")
def home():
    return render_template("generic.html")


# ---------------- Login ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    ensure_session()

    observe_request(request, session["id"])
    update_behavior(request.path)

    if request.method == "GET":
        return render_template("login.html")

    plan = handle_deception(session)

    if plan["delay"] > 0:
        time.sleep(plan["delay"])

    if plan["fake_success"] and not session["fake_used"]:
        session["fake_used"] = True
        return redirect("/dashboard")

    return render_template(
        "login.html",
        error_message=plan["message"]
    )


# ---------------- Decoy Pages ----------------

@app.route("/dashboard")
def decoy_dashboard():

    ensure_session()
    observe_request(request, session["id"])
    update_behavior(request.path)

    return render_template("decoy/dashboard.html")


@app.route("/users")
def decoy_users():

    ensure_session()
    observe_request(request, session["id"])
    update_behavior(request.path)

    return render_template("decoy/users.html")


@app.route("/settings")
def decoy_settings():

    ensure_session()
    observe_request(request, session["id"])
    update_behavior(request.path)

    return render_template("decoy/settings.html")


# ---------------- Profiling ----------------

@app.route("/profile_session")
def profile_debug():

    ensure_session()

    profile, signals, scores, ai_result = profile_session(session)

    return {
        "session_id": session.get("id"),
        "profile": profile,
        "signals": signals,
        "scores": scores,
        "ai_analysis": ai_result
    }


# ---------------- Dashboard ----------------

@app.route("/admin/dashboard")
def admin_dashboard():

    logs = load_logs()

    sessions = group_by_session(logs)
    timelines = build_timelines(sessions)
    path_counts = count_paths(logs)

    return render_template(
        "admin/dashboard.html",
        total_requests=len(logs),
        total_sessions=len(sessions),
        timelines=timelines,
        path_counts=path_counts
    )


# ---------------- AI Session Analysis (AJAX) ----------------

@app.route("/admin/ai_analyse_session")
def ai_analyse_session():
    """
    Returns an AI profile for the current admin's own session,
    or can be called with ?session_data=... for any session.
    Used by the dashboard's Analyse button.
    """
    ensure_session()
    profile, signals, scores, ai_result = profile_session(session)

    return {
        "profile": profile,
        "signals": signals,
        "ai_analysis": ai_result
    }


# ---------------- Run ----------------

if __name__ == "__main__":
    app.run(debug=True)
