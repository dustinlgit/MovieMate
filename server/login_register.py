import create_pages
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="../client/templates")

@app.route("/", methods=["POST", "GET"])
def login_verification():
    ...

@app.route("/register", method=["POST", "GET"])
def registration():
    if request.method == "POST":
        ...
    else:
        return render_template("register.html")