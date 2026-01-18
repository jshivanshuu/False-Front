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
@app.route("/login",methods=["GET","POST"])
def login():
    session_id = session.get("session_id") #creates and store session
    if not session_id:
        session["id"] = session_id = str(id(session))
        session["attempts"] = 0
        session["last_attempt_time"] = time.time()
    session_id = session["id"]
    observe_request(request,session_id)
    if request.method == "GET":
        return render_template("login.html")
    session["attempts"] += 1

    plan = decide({
        "attempts": session["attempts"],
        "last_attempt_time": session["last_attempt_time"]
    })

    session["last_attempt_time"] = time.time()
    if plan["delay"] > 0:
        time.sleep(plan["delay"])
    if plan["fake_success"]:
        return redirect("/dashboard")

    return render_template("login.html",error_message=plan["message"])
@app.route("/dashboard")
def fake_dashboard():
    # decoy page (very basic for now)
    return "<h2>Internal Dashboard</h2><p>System status: OK</p>"

if __name__ == "__main__":
    app.run(debug=True)