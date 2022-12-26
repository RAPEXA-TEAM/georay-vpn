#!/usr/bin/env

from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS
import Mysql
import csv
import hashlib
import requests
import names
import random
import CONFIG     #SERVER CONGIG

app = Flask(__name__)
CORS(app)

# config
app.config.update(
    SECRET_KEY = CONFIG.SECRET_KEY
)

@app.route("/payment",methods=["GET","POST"])
def handle_check_payment():
    if request.method == "POST":
        
        txid = request.json["txid"]
        days = request.json["days"]

        if Check_Payment(txid,days):
            username , password = names.get_full_name().split()
            phone = random.randint(0, 9999999999)
            email = names.get_full_name().split()[0] + "@gmail.com"
            answer = names.get_full_name().split()[1]
            token = hashlib.sha256(f"{username}-{password}-{phone}-{email}-{answer}-georay".encode('utf-8')).hexdigest()

            if Mysql.write_user_to_database(username, password, phone, email, str((int(days)+7)), token):

                ret = {"code" : 200, "data" : {"username" : username , "token" : token}}
                return jsonify(ret)

            else:
                ret = {"code" : 501, "data" : "'مشکل اتصال به دیتابیس'"}
                return jsonify(ret)
        
        else:
            ret = {"code" : 404, "data" : f"txid ({txid}) is not valid"}
            return jsonify(ret)
        
    prices = {"1month" : CONFIG.PRICE_ONE_MONTH, "2month" : CONFIG.PRICE_TWO_MONTH, "3month" : CONFIG.PRICE_TRE_MONTH}
    ret = {"code" : 200, "prices" : prices}
    return jsonify(ret)

@app.route('/d08ec689aef988a788aa6b5f6ed04a0efe57ca919d7d9d863d6322edd47f2d81',methods=["GET", "POST"])
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
        username = request.json["user"]
        token_in = request.json["token"]

        list_of_users_dic = {}
        List_Of_Users = Mysql.read_users_from_database()

        for user in List_Of_Users:

            user_db, password_db, phone_number, email, days, token = user
            list_of_users_dic[user_db] = {'password' : password_db,'phone' : phone_number, 'email' : email, 'days' : days, 'token' : token} 

        Servers = Read_servers()

        if (username in list_of_users_dic and token_in == list_of_users_dic[username]["token"]):
            
            ret = {"code" : 200, "data" : list_of_users_dic[username], "Servers" : Servers}
            return jsonify(ret)
        
        else:
            print(list_of_users_dic)
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

def Check_Payment(txid,days):
    '''This function check txid is valid or not'''

    List_of_txids_db = Mysql.read_txids_from_database()
    List_of_txids = []
    for txid_db in List_of_txids_db:

            txid_db_each, plan_db, time_db = txid_db
            List_of_txids.append(txid_db_each)

    if txid in List_of_txids:
        return False

    else:

        apikey = CONFIG.APIKEY
        baseurl = CONFIG.APIURL
        query = f"?module=transaction&action=getstatus&txhash={txid}&apikey={apikey}"

        url = baseurl + query
        response = requests.get(url)

        try:

            if int(response.json()['result']['isError']) == 0 : 
                Mysql.write_txid_to_database(txid,days)
                return True

            if int(response.json()['result']['isError']) == 1 :
                return False

            else:
                return False

        except:
            return False

if __name__ == "__main__":
    app.run("0.0.0.0",5550,debug=True)