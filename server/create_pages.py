from authentication import registration, verification
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="../client/templates")

@app.route("/login", methods=["POST", "GET"])
def create_login_page():
    if request.method == "POST":
        usr = request.form["username"]
        pswrd = request.form["password"]
        this_dict = verification(usr, pswrd)

        if this_dict.get(): #key is either t/f
            print("Login successful")
            return redirect(url_for("create_landingpage"))
        else: #should tell the user what went wrong
            return render_template("login.html", message=this_dict[this_dict.get()])
    else:
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

@app.route("/landingpage")
def create_landingpage():
    ...

if __name__ == "__main__":
    app.run(debug=True)