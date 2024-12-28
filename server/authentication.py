from flask import Flask
import bcrypt, sqlite3

app = Flask(__name__, template_folder="../client/templates")

def verification(usr, pswrd) -> dict:
    con = sqlite3.connect("server/database/recommendations.db")
    cursor = con.cursor()

    cursor.execute("SELECT hashed_pass FROM users WHERE username = ?", (usr,))
    stored_pass = cursor.fetchone()

    if stored_pass:
       if bcrypt.checkpw(pswrd.encode("utf-8"), stored_pass):
            return {"success": True, "message": "Username and password match!"}
       else:
           return {"success": False, "message":  "Wrong password!"} 
    else:
        return {"success": False, "message": "Username not found!"}

    #make a jwt (web token) to allow us to access back end w out having to log back in


def registration(usr, pswrd) -> bool:
    con = sqlite3.connect("server/database/recommendations.db")
    cursor = con.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (usr,))
    is_intable = cursor.fetchone()
    print(" under is_intable")

    if is_intable:
        # print("exists verifed")
        return True #this means we have found the username, meaning that the username is already taken
    else:
        # print("doesnt exist above new pass")
        new_pass = bcrypt.hashpw(pswrd.encode("utf-8"), bcrypt.gensalt()) #hashing and using a 'salt' to further the encryptiom
        cursor.execute("INSERT INTO users(username, hashed_pass) VALUES(?, ?)", (usr, new_pass)) #id auto increments
        con.commit()

        # #-------------tests
        # print("above false")
        # cursor.execute("SELECT * FROM users")
        # rows = cursor.fetchall()
        # print(rows)

        cursor.close()
        con.close()
        
        return False # returning false since we didn't find the username, so an account is generated for the user
    