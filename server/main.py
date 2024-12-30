from authentication import registration, verification
from tokens import create_token, decrypt_token
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="../client/templates")

@app.route("/login", methods=["POST", "GET"])
def login_page():
    if request.method == "POST":
        usr = request.form["username"]
        pswrd = request.form["password"]
        this_dict = verification(usr, pswrd)

        if this_dict.get("success"):
            print("Login successful")
            token = create_token(this_dict.get("id"))
            print(token)
            return redirect(url_for("main_page"))
        else:
            print("Login unsuccessful")
            return render_template("login.html", message=this_dict["message"])
    else:
        return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def registration_page():
    if request.method == "POST":
        usr = request.form["username"]
        pswrd = request.form["password"]
        
        if registration(usr,pswrd):
            return render_template("register.html", message="Username in use already")
        else:
            return render_template("register.html", message="Succesfully created account")
    else:
        return render_template("register.html")

@app.route("/")
def landing_page():
    return render_template("landing_page.html")

@app.route("/mainpage")
def main_page():
    return render_template("main_page.html")

if __name__ == "__main__":
    app.run(debug=True)