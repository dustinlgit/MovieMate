from flask import Flask
import bcrypt, sqlite3

app = Flask(__name__, template_folder="../client/templates")

def verification(usr, pswrd) -> dict:
    con = sqlite3.connect("server/database/recommendations.db")
    cursor = con.cursor()

    cursor.execute("SELECT id, hashed_pass FROM users WHERE username = ?", (usr,))
    stored_pass = cursor.fetchone()
    # print(stored_pass[0])

    if stored_pass:
       if bcrypt.checkpw(pswrd.encode("utf-8"), stored_pass[1]):
            cursor.close()
            con.close()
            return {"success": True, "id" : stored_pass[0]}
       else:
            cursor.close()
            con.close()
            return {"success": False, "message":  "Wrong password!"} 
    else:
        cursor.close()
        con.close()
        return {"success": False, "message": "Username not found!"}


def registration(usr, pswrd) -> bool:
    con = sqlite3.connect("server/database/recommendations.db")
    cursor = con.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (usr,))
    is_intable = cursor.fetchone()

    if is_intable:
        # print("inside if")
        return True
    else:
        # print("inside else")
        new_pass = bcrypt.hashpw(pswrd.encode("utf-8"), bcrypt.gensalt()) #hashing and using a 'salt' to further the encryptiom
        cursor.execute("INSERT INTO users(username, hashed_pass) VALUES(?, ?)", (usr, new_pass)) #id auto increments
        con.commit()

        # #---tests insertion works---
        # print("above false")
        # cursor.execute("SELECT * FROM users")
        # rows = cursor.fetchall()
        # print(rows)

        cursor.close()
        con.close()

        return False # returning false since we didn't find the username, so an account is generated for the user
