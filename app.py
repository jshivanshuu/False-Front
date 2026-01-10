from flask import Flask, render_template, request, session
from Entry.observer import observe_request
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

    observe_request(request,session_id)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print("Observed credentials:", username, password)
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)