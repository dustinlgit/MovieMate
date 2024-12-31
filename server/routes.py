from authentication import registration, verification
from tokens import create_token, decrypt_token
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify

import requests
from dotenv import load_dotenv
import os

load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
# print(BEARER_TOKEN)

app = Flask(__name__, template_folder="../client/templates")

@app.route("/")
def landing_page():
    return render_template("landingPage.html")

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
            response = make_response(redirect(url_for("main_page"))) #this way we can return 2 things
            response.set_cookie("auth_token", token, httponly=True, secure=True, samesite="Lax") #pass token as a cookie
            return response
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

@app.route("/mainpage", methods=["GET"])
def main_page():
    return render_template("main.html")
    
app.route("/favorites", methods=["GET"])
def user_fav():
    return render_template("favorites.html")
    
@app.route("/search", methods=["POST", "GET"])
def search_movies():
    query = request.args.get("query")
    #print(query)
    if not query:
        return render_template("search.html", movies=[]) #this way we can default to an empty page
    
    url = "https://api.themoviedb.org/3/search/movie"
    headers = {
        "accept": "application/json",
        "Authorization": BEARER_TOKEN
    }
    params={
        "query": query
    }
    response = requests.get(url, headers=headers, params=params)

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    if response.status_code == 200:
        movies = response.json().get("results", []) #search for key: results, default val: empty list
        return render_template("search.html", query=query, movies=movies)
    else:
        return render_template("search.html", query=query, movies=[], error="Movie title not found")

if __name__ == "__main__":
    app.run(debug=True)