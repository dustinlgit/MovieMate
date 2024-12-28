from flask import Flask
import bcrypt, sqlite3

app = Flask(__name__, template_folder="../client/templates")

def verification(usr, pswrd) -> dict:
    con = sqlite3.connect("server/database/recommendations.db")
    cursor = con.cursor()

    cursor.execute("SELECT hashed_pass WHERE username = ?", (usr,))
    stored_pass = cursor.fetchone()

    if stored_pass:
       if bcrypt.checkpw(pswrd.encode("utf-8"), stored_pass):
            return {True : "Username and password match!"}
       else:
           return {False : "Wrong password!"} 
    else:
        return {False : "Username not found!"}

    #make a jwt (web token) to allow us to access back end w out having to log back in


def registration(usr, pswrd) -> bool:
    con = sqlite3.connect("server/database/recommendations.db")
    cursor = con.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (usr,))
    is_intable = cursor.fetchone()

    if is_intable:
        return True #this means we have found the username, meaning that the username is already taken
    else:
        new_pass = bcrypt.hashpw(pswrd.encode("utf-8"), bcrypt.gensalt()) #hashing and using a 'salt' to further the encryptiom
        cursor.execute("INSERT INTO users VALUES(?, ?)", (usr, pswrd)) #id auto increments
        return False # returning false since we didn't find the username, so an account is generated for the user
    