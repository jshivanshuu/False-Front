from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username,password)
        return render_template("login.html")
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)