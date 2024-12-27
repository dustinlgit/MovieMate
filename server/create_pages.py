from authentication import registration
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="../client/templates")

@app.route("/")
def create_login_page():
    return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def create_registration():
    if request.method == "POST":
        usr = request.form["username"]
        pswrd = request.form["password"]
        
        if registration(usr,pswrd):
            return render_template("register.html", message="Username in use already")
        else:
            return render_template("register.html", message="Succesfully created account")
    else:
        return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)