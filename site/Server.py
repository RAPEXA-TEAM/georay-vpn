#!/usr/bin/env

# import libraries that required for the service
from web3 import Web3
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import random
import string
import smtplib
import Mysql
import csv
import hashlib
import json
import CONFIG     #SERVER CONGIG

# Flask app configuration

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)
CORS(app)

# config
app.config.update(
    SECRET_KEY = CONFIG.SECRET_KEY
)

# routes

@app.route("/logout")
def logout():
    '''this function is used to logout the user'''

    return redirect(url_for('handle_main_page'))

@app.route("/logout_apk", methods=['POST','GET'])
def logout_apk():
    '''this function is used to logout the user and clean device and os from database'''

    if request.method == 'POST':
        username = request.json["email"]
        passw = request.json["pass"]
        Device_GET = request.json['Device']
        Device_OS_GET = request.json['OS']

        list_of_users_dic = {}
        List_Of_Users = Mysql.read_users_from_database()

        for user in List_Of_Users:

            user_db, password_db, phone_number, email, days, token, verified, Device, Device_OS = user
    
            if verified != "0" and days != "0":
                list_of_users_dic[user_db] = {'password' : password_db, 'username' : email, 'days' : days, 'token' : token, 'Device' : Device, 'OS' : Device_OS} 

            else:
                continue

        if (username in list_of_users_dic and passw == list_of_users_dic[username]["password"] and list_of_users_dic[username]['Device'] == Device_GET and list_of_users_dic[username]['OS'] == Device_OS_GET and int(list_of_users_dic[username]["days"]) > 0):

            if Mysql.delete_user_device_from_database(username):

                ret = {"code" : 200, "data" : "Device logout correctly!"}
                return jsonify(ret)

            else:

                ret = {"code" : 401, "data" : "Error"}
                return jsonify(ret)

        ret = {"code" : 401, "data" : "Forbidden"}
        return jsonify(ret)

@app.route("/update") 
def handle_update():
    '''this function is used to update apps'''

    ret = {"version" : CONFIG.VERSION , "force" : CONFIG.VERSION_TYPE, "links" : CONFIG.DOWNLOAD_LINK}
    return jsonify(ret)

@app.route('/seller', methods=['POST','GET'])
@limiter.limit("50 per day")
def Handle_Seller():
    '''this function is used to handle the seller login page'''

    if request.method == 'POST':

        username = request.json['username']
        password = request.json['password']

        if Check_Seller(username, password):

            hasha = hashlib.sha256(("{"+str(username)+"}{"+str(password)+"}-georay").encode("utf-8")).hexdigest()
            ret = {"code" : 200 , "Token" : hasha}
            return jsonify(ret)

        else:
            ret = {"code" : 401 , "data" : "Premission denied"}
            return jsonify(ret)

    return render_template('login.html')

@app.route('/add_sell', methods=['POST', 'GET'])
@limiter.limit("100 per day")
def handle_add_sell():
    '''this function is used to handle the add user from seller page'''

    if request.method == 'POST':
        password = generate_random_password()
        email = request.json["email"]
        Token_seller = request.json["seller"]
        token = hashlib.sha256(f"{email}-georay".encode('utf-8')).hexdigest()

        Sellers = Read_Sellers()
        Tokens = []

        for username_db, password_db in Sellers.items():  
            Tokens.append(hashlib.sha256(("{"+str(username_db)+"}{"+str(password_db)+"}-georay").encode("utf-8")).hexdigest())

        try :
            if Check_User(token) and Token_seller in Tokens:
                if Mysql.write_user_from_seller_to_database(email, password, Token_seller, token):
                    ret = {"code" : 200, "data" : "user created successfully"}
                    return jsonify(ret)
                else :
                    ret = {"code" : 501, "data" : "error creating user"}
                    return jsonify(ret)
            else:
                ret = {"code" : 401, "data" : "error creating user"}
                return jsonify(ret)

        except Exception as error:
            ret = {"code" : 406, "data" : error}
            return jsonify(ret)

    ret = {"code" : 500, "data" : "Request not valid"}
    return jsonify(ret)

@app.route('/sells_json', methods=['POST','GET'])
@limiter.limit("100 per day")
def Handle_Sellers_json():
    '''this function is used to handle the sells from one seller in json format'''

    exec(open(CONFIG.PATH_EXPIRATION).read())      

    Token = request.args.get('Token')
    Sellers = Read_Sellers()
    Tokens = []

    for username, password in Sellers.items():  
        Tokens.append(hashlib.sha256(("{"+str(username)+"}{"+str(password)+"}-georay").encode("utf-8")).hexdigest())

    if Token in Tokens:

        if request.method == 'POST':

            days = request.json["days"]
            token = str(request.json["data"])

            if (Mysql.update_user(token.strip(),days)):
                ret = {"code" : 200, "data" : f"update {token.strip()} expired days to {days} days!"}
                return jsonify(ret)

            else:
                ret = {"code" : 501, "data" : "error connecting to database"}
                return jsonify(ret)

        users = []
        all_users = Mysql.read_users_for_seller_from_database(Token)
        user_counter = 0
        total_sell = 0

        Sellers = Read_Sellers()
        Seller = {}

        for username_new, password_new in Sellers.items():

            if hashlib.sha256(("{"+str(username_new)+"}{"+str(password_new)+"}-georay").encode("utf-8")).hexdigest() == Token:
                Seller[username_new] = password_new

            else:
                continue

        for user in all_users:
            user_db, password_db, Token_seller, Token_sellerr, days, token_db, verified, Device, Device_OS  = user
            users.append({'username' : user_db, 'password' : password_db, 'days' : days, 'token' : token_db, 'Device' : Device, 'OS' : Device_OS})
            user_counter += 1
            total_sell = user_counter * CONFIG.PRICE_ONE_MONTH

        json_data = {"code" : 200, "users" : users, "sells" : total_sell, "count" : user_counter, "seller" : Seller}
        return jsonify(json_data)

    else:
        ret = {"code" : 500, "data" : "Token did not exist"}
        return jsonify(ret)

@app.route('/sells', methods=['POST','GET'])
@limiter.limit("100 per day")
def Handle_Sellers():
    '''this function is used to handle the sells from one seller'''

    exec(open(CONFIG.PATH_EXPIRATION).read())      

    Token = request.args.get('Token')
    Sellers = Read_Sellers()
    Tokens = []

    for username, password in Sellers.items():  
        Tokens.append(hashlib.sha256(("{"+str(username)+"}{"+str(password)+"}-georay").encode("utf-8")).hexdigest())

    if Token in Tokens:

        if request.method == 'POST':

            sells = str(request.json["sells"])

            if (Mysql.delete_user(sells.strip(),Token)):
                ret = {"code" : 200, "data" : f"delete user {sells.strip()} successfully !"}
                return jsonify(ret)

            else:
                ret = {"code" : 501, "data" : "error connecting to database"}
                return jsonify(ret)

        users = []
        all_users = Mysql.read_users_for_seller_from_database(Token)
        user_counter = 0
        total_sell = 0

        Sellers = Read_Sellers()
        Seller = {}

        for username_new, password_new in Sellers.items():

            if hashlib.sha256(("{"+str(username_new)+"}{"+str(password_new)+"}-georay").encode("utf-8")).hexdigest() == Token:
                
                Seller[username_new] = password_new
                break

            else:
                continue

        seller_payed = Read_Sellers_payed(username_new)

        for user in all_users:
            user_db, password_db, Token_seller, Token_sellerr, days, token_db, verified, Device, Device_OS  = user
            users.append({'username' : user_db, 'password' : password_db, 'days' : days, 'token' : token_db, 'Device' : Device, 'OS' : Device_OS})
            user_counter += 1
            total_sell = user_counter * CONFIG.PRICE_ONE_MONTH

        json_data = {"users" : users, "sells" : total_sell, "count" : user_counter, "seller" : Seller, "payed" : seller_payed}
        return render_template('seller.html', data = json_data)

    else:
        return redirect(url_for('Handle_Seller'))

@app.route('/makepaymenthash', methods=['POST','GET'])
def handle_make_payment_hash():
    '''this function is used to handle the make payment hash'''

    if request.method == 'POST':

        List_Of_Users = Mysql.read_users_from_database()
        List_of_tokens = []
        for user in List_Of_Users:
            user_db, password_db, phone_number, email, days, token_db, verified, Device, Device_OS = user 
            List_of_tokens.append(token_db)

        value = request.json['value']
        token = request.json['token']

        payment_hash = hashlib.sha256(f"{value}-{token}-georay".encode('utf-8')).hexdigest()
    
        if token in List_of_tokens:
            ret = {"code" : 200, "payment_hash" : payment_hash}
            return jsonify(ret)

        else:
            ret = {"code" : 401, "data" : "user dont exist"}
            return jsonify(ret)

    ret = {"code" : 500, "data" : "Request not valid"}
    return jsonify(ret)

@app.route("/payment",methods=["GET","POST"])
def handle_check_payment():
    '''this function is used to handle the check payment'''

    if request.method == "POST":
        
        txid = request.json["txid"]
        value = request.json['value']
        token = request.json['token']
        days = int((int(value) / 50000) * 30)
        payment_hash = hashlib.sha256(f"{value}-{token}-georay".encode('utf-8')).hexdigest()

        if Check_Payment(txid,payment_hash):
            if Mysql.update_user(token, days) and Mysql.write_txid_to_database(txid, days):

                ret = {"code" : 200, "data" : f"payment successful and payment hash {payment_hash} is valid and user remaining days update to {days}"}
                return jsonify(ret)

            else:
                ret = {"code" : 501, "data" : "error connecting to database"}
                return jsonify(ret)
        
        else:
            ret = {"code" : 404, "data" : "tx-id or payment-hash is not valid"}
            return jsonify(ret)

    ret = {"code" : 401, "data" : "request not valid"}
    return jsonify(ret)

@app.route('/d08ec689aef988a788aa6b5f6ed04a0efe57ca919d7d9d863d6322edd47f2d81',methods=["GET", "POST"])
def handle_admin_page():
    '''this function is used to handle the admin private page to manage all users'''

    if request.method == "POST":
        days = request.json["days"]
        token = str(request.json["data"])
        if (Mysql.update_user(token.strip(),days)):
            ret = {"code" : 200, "data" : f"update {token.strip()} expired days to {days} days!"}
            return jsonify(ret)

        else:
            ret = {"code" : 501, "data" : "error connecting to database"}
            return jsonify(ret)
            
    all_users = Mysql.read_users_from_database()
    users = []
    for user in all_users:
        user_db, password_db, phone_number, email, days, token, verified, Device, Device_OS = user
    
        if verified != "0":
            users.append({'username' : user_db, 'password' : password_db,'phone' : Read_Sellers_from_token(phone_number), 'days' : days, 'token' : token, 'Device' : Device, 'OS' : Device_OS})
        
        else:
            continue

    return render_template("admin.html", data = {"users" : users})   

@app.route('/register',methods=["GET", "POST"])
def handle_create_user():
    '''this function is used to handle the create user from rigisteration page'''

    if request.method == 'POST':
        password = generate_random_password()
        rpassword = password
        phone = "0"
        email = request.json["email"]
        username = email
        answer = generate_random_password()
        token = hashlib.sha256(f"{email}-georay".encode('utf-8')).hexdigest()

        try :
            if Check_User(token) and password == rpassword:
                Send_Registration_Email(email,username,password,phone,answer)
                if Mysql.write_user_to_database(username, password, phone, email, "7", token, "0"):
                    ret = {"code" : 200, "data" : "user created successfully but not verified for verification check email that you received"}
                    return jsonify(ret)
                else :
                    ret = {"code" : 501, "data" : "error creating user"}
                    return jsonify(ret)
            else:
                ret = {"code" : 401, "data" : "error creating user"}
                return jsonify(ret)

        except Exception as error:
            ret = {"code" : 406, "data" : error}
            return jsonify(ret)

    return render_template("register.html")

@app.route('/Authentication', methods=['GET', 'POST'])
def handle_Authentication_new_user():
    '''this function is used to handle the authentication of new user that rigistered a account but did not verify by the email'''

    Token = request.args.get('Token')
    exec(open(CONFIG.PATH_EXPIRATION).read())
    
    if Mysql.update_user_registration(Token) and Check_User_Reverse(Token):
    
        message = "User verified successfully"
        return render_template("index.html", message = message)


    alert = "Error verifying user"
    return render_template("index.html", alert = alert)

@app.route('/privacy',methods=["GET", "POST"])
def handle_main_page():
    '''this function is used to handle the privacy page'''

    return render_template("privacy.html")

@app.route('/',methods=["GET", "POST"])
def handle_privacy_page():
    '''this function is used to handle the main page'''

    # run Expiration.py
    exec(open(CONFIG.PATH_EXPIRATION).read())

    return render_template("index.html")

@app.route('/login',methods=["GET", "POST"])
def handle_login_user():
    '''this function is used to handle the login users from aplication'''

    # run Expiration.py
    exec(open(CONFIG.PATH_EXPIRATION).read())

    if request.method == 'POST':
        username = request.json["email"]
        passw = request.json["pass"]
        Device_GET = request.json['Device']
        Device_OS_GET = request.json['OS']

        list_of_users_dic = {}
        List_Of_Users = Mysql.read_users_from_database()

        for user in List_Of_Users:

            user_db, password_db, phone_number, email, days, token, verified, Device, Device_OS = user
    
            if verified != "0" and days != "0":
                list_of_users_dic[user_db] = {'password' : password_db, 'username' : email, 'days' : days, 'token' : token, 'Device' : Device, 'OS' : Device_OS} 

            else:
                continue

        if username == CONFIG.ALTER_USERNAME and passw == CONFIG.ALTER_PASSWORD:

            Servers_v = Read_servers()
            servers_o = [] #TODO: add it for next update

            update_info = {"version" : CONFIG.VERSION , "force" : CONFIG.VERSION_TYPE, "links" : CONFIG.DOWNLOAD_LINK}
            prices = {"1month" : CONFIG.PRICE_ONE_MONTH, "2month" : CONFIG.PRICE_TWO_MONTH, "3month" : CONFIG.PRICE_TRE_MONTH}
            ret = {"code" : 200, "data" : {'password' : CONFIG.ALTER_PASSWORD, 'username' : CONFIG.ALTER_USERNAME, 'days' : "999", 'token' : "GOD"}, "v2ray" : Servers_v , "openconnect" : servers_o, "prices" : prices, "update_info" : update_info}
            return jsonify(ret)

        elif list_of_users_dic[username]['Device'] is not None and list_of_users_dic[username]['OS'] is not None:

            Servers_v = Read_servers()
            servers_o = [] #TODO: add it for next update

            update_info = {"version" : CONFIG.VERSION , "force" : CONFIG.VERSION_TYPE, "links" : CONFIG.DOWNLOAD_LINK}

            if (username in list_of_users_dic and passw == list_of_users_dic[username]["password"] and list_of_users_dic[username]['Device'] == Device_GET and list_of_users_dic[username]['OS'] == Device_OS_GET and int(list_of_users_dic[username]["days"]) > 0):

                prices = {"1month" : CONFIG.PRICE_ONE_MONTH, "2month" : CONFIG.PRICE_TWO_MONTH, "3month" : CONFIG.PRICE_TRE_MONTH}
                ret = {"code" : 200, "data" : list_of_users_dic[username], "v2ray" : Servers_v , "openconnect" : servers_o, "prices" : prices, "update_info" : update_info}
                return jsonify(ret)
            
            else:
                ret = {"code" : 402, "data" : "Contact to Seller or provider"}
                return jsonify(ret)    

        elif Mysql.add_user_device_to_database(username, Device_GET, Device_OS_GET):

            ret = {"code" : 201, "data" : "Device and OS set correctly for this user"}
            return jsonify(ret)

        ret = {"code" : 403, "data" : "Error writing to database"}
        return jsonify(ret)
    
    ret = {"code" : 401, "data" : "request not valid"}
    return jsonify(ret)


def Read_servers():
    '''this function is used to read the servers from the csv file'''

    Servers = []

    with open(CONFIG.PATH_SERVERS, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            Servers.append(row[1])
    
    return Servers

def Read_Sellers_from_token(Token):
    '''this function is used to read the sellers from the csv file'''

    with open(CONFIG.PATH_SELLERS, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
                
            if hashlib.sha256(("{"+str(row[0])+"}{"+str(row[1])+"}-georay").encode("utf-8")).hexdigest() == Token:

                return row[0]

    return None

def Read_Sellers():
    '''this function is used to read the sellers from the csv file'''

    Sellers = {}

    with open(CONFIG.PATH_SELLERS, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            Sellers[row[0]] = row[1]

    return Sellers

def Read_Sellers_payed(Seller):
    '''this function is used to read the seller payed from the csv file'''

    with open(CONFIG.PATH_SELLERS, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        
        for row in spamreader:

            if Seller == row[0]:

                return row[2]

    return None

def Check_User(token):
    '''this function is used to check if the new token is valid or not'''

    List_Of_Users = Mysql.read_users_from_database()
    List_of_tokens = []
    for user in List_Of_Users:
        user_db, password_db, phone_number, email, days, token_db, verified, Device, Device_OS = user 
        List_of_tokens.append(token_db)

    if token in List_of_tokens:
        return False
                
    else:
        return True

def Check_User_Reverse(token):
    '''this function is used to check if the new token is valid or not'''

    List_Of_Users = Mysql.read_users_from_database()
    List_of_tokens = []
    for user in List_Of_Users:
        user_db, password_db, phone_number, email, days, token_db, verified, Device, Device_OS = user 
        List_of_tokens.append(token_db)

    if token in List_of_tokens:
        return True
                
    else:
        return False

def Check_Seller(username,password):
    Sellers = Read_Sellers()
    for username_for, password_for in Sellers.items():
        if username_for == username and password_for == password:
            return True
    return False

def Check_Payment(txid,payment_hash):
    '''This function check txid with hash made before is valid or not'''

    List_of_txids_db = Mysql.read_txids_from_database()
    List_of_txids = []

    for txid_db in List_of_txids_db:

            txid_db_each, plan_db, time_db = txid_db
            List_of_txids.append(txid_db_each)

    if txid in List_of_txids:

        return False

    else:

        try:

            web3 = Web3(Web3.HTTPProvider(CONFIG.NODE_URL))
            result = web3.eth.get_transaction(txid)
            json_result = json.loads(web3.toJSON(result))
            hash = bytes.fromhex(json_result['input'][2:]).decode('utf-8')
            
            if payment_hash == hash:
                return True

            else:
        
                return False
        
        except:

            return False

def Send_Registration_Email(email,username,password,phone,answer):
    '''this function is used to send the registration email to the user'''

    # create registration token
    token = hashlib.sha256(f"{email}-georay".encode('utf-8')).hexdigest()

    # creates Message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Georay account Registertion"
    message["From"] = CONFIG.SENDER_EMAIL
    message["To"] = email

    text = f"""\
    Hi,
    Check out the link below To register your Georay VPN account:
    https://georay.store/Authentication?Token={token}
    \n
    username: {username}
    password: {password}
    """

    html = f"""\
    <html>
    <body>
        <p>Hi,<br>
        Check out the link below To register your Georay VPN account:</p>
        <p><a href="https://georay.store/Authentication?Token={token}">Register Now!</a></p>
        <br>
        <p>Username: {username}</p>
        <p>Password: {password}</p>
    </body>
    </html>
    """
    
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    # creates SMTP session
    s = smtplib.SMTP(CONFIG.SMTP_SERVER, CONFIG.SMTP_PORT)

    # start TLS for security
    s.starttls()
    
    # Authentication
    s.login(CONFIG.SENDER_EMAIL, CONFIG.PASSWORD)
 
    # sending the mail
    s.sendmail(CONFIG.SENDER_EMAIL, email, message.as_string())
    
    # terminating the session
    s.quit()
    return True

def generate_random_password():
    '''this function is used to generate a random password'''

    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(12))
    return result_str

if __name__ == "__main__":
    app.run(CONFIG.HOST,CONFIG.RUNNING_PORT,debug=CONFIG.PRODUCTION_MODE)