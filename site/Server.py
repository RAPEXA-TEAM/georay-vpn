#!/usr/bin/env
from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS
import Mysql
import csv
import hashlib
import CONFIG     #SERVER CONGIG

app = Flask(__name__)
CORS(app)

# config
app.config.update(
    SECRET_KEY = CONFIG.SECRET_KEY
)


@app.route('/admin',methods=["GET", "POST"])
def handle_admin_page():
    if request.method == "POST":
        days = request.json["days"]
        token = str(request.json["data"])
        if (Mysql.update_user(token.strip(),days)):
            ret = {"code" : 200, "data" : f"update {token.strip()} expired days to {days} days!"}
            return jsonify(ret)

        else:
            ret = {"code" : 501, "data" : "'مشکل اتصال به دیتابیس'"}
            return jsonify(ret)
            
    all_users = Mysql.read_users_from_database()
    users = []
    for user in all_users:
        user_db, password_db, phone_number, email, days, token = user
        users.append({'username' : user_db, 'password' : password_db,'phone' : phone_number, 'email' : email, 'days' : days, 'token' : token})
    return render_template("admin.html", data = {"users" : users})   

@app.route('/register',methods=["GET", "POST"])
def handle_create_user():
    if request.method == 'POST':
        password = request.json["pass"]
        rpassword = request.json["rpass"]
        username = request.json["user"]
        phone = request.json["phone"]
        email = request.json["email"]
        answer = request.json["answer"]
        token = hashlib.sha256(f"{username}-{password}-{rpassword}-{phone}-{email}-{answer}-georay".encode('utf-8')).hexdigest()

        try :
            if Check_User(token) and password == rpassword:
                if Mysql.write_user_to_database(username, password, phone, email, "7", token):
                    ret = {"code" : 200, "data" : "یوزر با موفقیت ساخته شد"}
                    return jsonify(ret)
                else :
                    ret = {"code" : 501, "data" : "'مشکل اتصال به دیتابیس'"}
                    return jsonify(ret)
            else:
                ret = {"code" : 404, "data" : "یوزری با مشخصات ذیل موجود میباشد"}
                return jsonify(ret)

        except Exception as error:
            ret = {"code" : 406, "data" : error}
            return jsonify(ret)

    return render_template("register.html")

@app.route('/',methods=["GET", "POST"])
def handle_main_page():
    return render_template("index.html")

@app.route('/login',methods=["GET", "POST"])
def handle_login_user():

    if request.method == 'POST':
        password = request.json["pass"]
        username = request.json["user"]
        token_in = request.json["token"]

        list_of_users_dic = {}
        List_Of_Users = Mysql.read_users_from_database()

        for user in List_Of_Users:

            user_db, password_db, phone_number, email, days, token = user
            list_of_users_dic[user_db] = {'password' : password_db,'phone' : phone_number, 'email' : email, 'days' : days, 'token' : token} 

        Servers = Read_servers()

        if (username in list_of_users_dic and token_in == list_of_users_dic[username]["token"] and password == list_of_users_dic[username]["password"]):
            
            ret = {"code" : 200, "data" : list_of_users_dic[username], "Servers" : Servers}
            return jsonify(ret)
        
        else:
            ret = {"code" : 401, "data" : "Error"}
            return jsonify(ret)    
    
    ret = {"code" : 500, "data" : "Request not valid"}
    return jsonify(ret)

def Read_servers():
    Servers = []

    with open('Servers.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            Servers.append(row[1])
    
    return Servers

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