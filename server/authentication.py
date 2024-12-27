from flask import Flask, render_template, request, redirect
import bcrypt, sqlite3

app = Flask(__name__, template_folder="../client/templates")

@app.route("/", methods=["POST", "GET"])
def log_verification():
    ...


def registration(usr, pswrd) -> bool:
    con = sqlite3.connect("server/database/recommendations.db")
    cursor = con.cursor()

    cursor.execute("SELECT id FROM users WHERE username=?", (usr,))
    if cursor.fetchone():
        return True
    else:
        newpass = bcrypt.hashpw(pswrd.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("INSERT INTO users(username, hashed_pass) VALUES(?,?)", (usr, newpass))

        con.commit()
        con.close()
        return False