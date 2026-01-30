from flask import Flask, render_template, request, session
from Entry.observer import observe_request
from deception.response_engine import decide
import time
from flask import redirect
app = Flask(__name__)
secret_key = "Falsefront"
app.secret_key = secret_key
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
@app.route("/login", methods=["GET", "POST"])
def login():
    # Initialize session state once
    if "id" not in session:
        session["id"] = str(id(session))
        session["attempts"] = 0
        session["last_attempt_time"] = time.time()

    session_id = session["id"]

    # Module 1: observe EVERYTHING
    observe_request(request, session_id)

    # -------- GET --------
    if request.method == "GET":
        return render_template("login.html")

    # -------- POST --------
    session["attempts"] += 1

    plan = decide({
        "attempts": session["attempts"],
        "last_attempt_time": session["last_attempt_time"]
    })

    # update AFTER decision
    session["last_attempt_time"] = time.time()

    # apply delay
    if plan["delay"] > 0:
        time.sleep(plan["delay"])

    # fake success
    if plan["fake_success"]:
        return redirect("/dashboard")

    # normal deceptive failure
    return render_template(
        "login.html",
        error_message=plan["message"]
    )

@app.route("/dashboard")
def decoy_dashboard():
    observe_request(request, session["id"])
    return render_template("decoy/dashboard.html")

@app.route("/users")
def decoy_users():
    observe_request(request, session["id"])
    return render_template("decoy/users.html")

@app.route("/settings")
def decoy_settings():
    observe_request(request, session["id"])
    return render_template("decoy/settings.html")

if __name__ == "__main__":
    app.run(debug=True)