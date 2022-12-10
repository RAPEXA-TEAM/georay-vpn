#!/usr/bin/env
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import Mysql
import hashlib
import CONFIG     #SERVER CONGIG

app = Flask(__name__)
CORS(app)

# config
app.config.update(
    SECRET_KEY = CONFIG.SECRET_KEY
)

@app.route('/',methods=["GET", "POST"])
def handle_main_page():
    return render_template("index.html")

@app.route('/admin',methods=["GET", "POST"])
def handle_admin_page():
    if request == "POST":
        pass

@app.route('/dashbourd',methods=["GET", "POST"])
def handle_dashbourd_page():
    return render_template("dashbourd.html")

#TODO
@app.route("/Server_list",methods=["GET","POST"])
def handle_dashbourd_page():
    if request.method == 'POST':
        ret = {"1" : {"url" : "" , "user" : "" , "pass" : ""} , }
        return jsonify(ret)
    return 200

@app.route('/register',methods=["GET", "POST"])
def handle_create_user():
    if request.method == 'POST':
        password = request.json["pass"]
        username = request.json["user"]
        phone = request.json["phone"]
        email = request.json["email"]
        answer = request.json["answer"]
        token = hashlib.sha256(f"{username}-{password}-{phone}-{email}-{answer}-georay".encode('utf-8')).hexdigest()
        try :
            if Check_User(token):
                if Mysql.write_user_to_database(username, password, phone, email, "1", token):
                    ret = {'status':'ok','code':'200'}
                    return jsonify(ret)
                else :
                    ret = {'status':'failed','error':'writing user to database'}
                    return jsonify(ret)
            else:
                ret = {'status':'failed','error':'user not valid'}
                return jsonify(ret)
        except Exception as error:
            ret = {'code' : '404', 'error' : error}
            return jsonify(ret)

@app.route('/login',methods=["GET", "POST"])
def handle_login_user():
    if request.method == 'POST':
        password = request.json["pass"]
        username = request.json["user"]
        token_in = request.json["token"]
        try:

            list_of_users_dic = {}
            List_Of_Users = Mysql.read_users_from_database()

            for user in List_Of_Users:

                user_db, password_db, phone_number, email, days, token = user
                list_of_users_dic[user_db] = {'password' : password_db,'phone' : phone_number, 'email' : email, 'days' : days, 'token' : token} 
            
            if (username in list_of_users_dic and token_in == list_of_users_dic[username]['token'] and password == list_of_users_dic[username]['password']):

                ret = {'code' : '200', 'data' : list_of_users_dic[username]}
                return jsonify(ret)

            else :
                return render_template("login.html")

        except Exception as error:
                    ret = {'code' : '404', 'error' : error}
                    return jsonify(ret)

    return render_template("login.html")

def Check_User(token):
    
    List_Of_Users = Mysql.read_users_from_database()
    List_of_tokens = []
    for user in List_Of_Users:
        user_db, password_db, phone_number, email, days, token_db = user 
        List_of_tokens.append(token_db)
        
    if token in List_of_tokens:
        return False
                
    else:
        return True

if __name__ == "__main__":
    app.run("0.0.0.0",5550,debug=True)