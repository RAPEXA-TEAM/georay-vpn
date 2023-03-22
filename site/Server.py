#!/usr/bin/env

# import libraries that required for the service

from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import Mysql      #SERVER MYSQL
import CONFIG     #SERVER CONGIG
import Routes     #SERVER ROUTES
import Helper     #SERVER HELPER
import Response   #SERVER RESPONSE

# Flask app configuration

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# CORS
CORS(app)

# CONFIG

app.config.update(
    SECRET_KEY = CONFIG.SECRET_KEY
)

# ROUTER

@app.route(Routes.ROUTE_LOGOUT)
def logout():
    '''this function is used to logout the user'''

    return redirect(url_for('handle_main_page'))

@app.route(Routes.ROUTE_LOGOUT_APK, methods=['POST','GET'])
def logout_apk():
    '''this function is used to logout the user and clean device and os from database'''

    if request.method == 'POST':
        
        username = request.json["email"]
        passw = request.json["pass"]
        Device_GET = request.json['Device']
        Device_OS_GET = request.json['OS']

        user = Mysql.read_one_users_or_404_from_database(username)

        if user != None:

            user_db, password_db, phone_number, email, token, verify, Device, Device_OS , created_date, expierd_date, FreeTimeExpired = user
            
            if (username == user_db and passw == password_db and Device == Device_GET and Device_OS == Device_OS_GET):

                if Mysql.delete_user_device_from_database(username):

                    return jsonify(Response.LOGOUT_CORRECTLY)
                
                else:

                    return jsonify(Response.ERROR_DATABASE)
            
            return jsonify(Response.ERROR_USER_OR_PASS_WRONG)
        
        return jsonify(Response.ERROR_USER_NOT_EXIST)
    
    return jsonify(Response.ERROR_REQUEST_NOT_VALID)

@app.route(Routes.ROUTE_UPDATE) 
def handle_update():
    '''this function is used to update apps'''

    ret = {"version" : CONFIG.VERSION , "force" : CONFIG.VERSION_TYPE, "links" : CONFIG.DOWNLOAD_LINK}
    return jsonify(ret)

@app.route(Routes.ROUTE_SELLER, methods=['POST','GET'])
@limiter.limit("50 per day")
def Handle_Seller():
    '''this function is used to handle the seller login page'''

    if request.method == 'POST':

        username = request.json['username']
        password = request.json['password']

        if Helper.Check_Seller(username, password):

            token = Helper.seller_hash(username,password)
            ret = {"code" : 200 , "Token" : token}
            return jsonify(ret)

        else:
            return jsonify(Response.ERROR_USER_OR_PASS_WRONG)

    return render_template('login.html')

@app.route(Routes.ROUTE_ADD_SELL, methods=['POST', 'GET'])
@limiter.limit("100 per day")
def handle_add_sell():
    '''this function is used to handle the add user from seller page'''

    if request.method == 'POST':
        
        password = Helper.generate_random_password()
        email = request.json["email"]
        Token_seller = request.json["seller"]

        token = Helper.generate_token(email)

        Sellers = Helper.Read_Sellers()
        Tokens = []

        for username_db, password_db in Sellers.items():  
            Tokens.append(Helper.seller_hash(username_db,password_db))

        try :
            
            if Helper.Check_User(email,token) and Token_seller in Tokens:
                
                CreatedDate, ExpiredDate = Helper.monthly_plan_dates()

                if Mysql.write_user_from_seller_to_database(email, password, Token_seller, token, CreatedDate, ExpiredDate):
            
                    return jsonify(Response.CREATE_USER_CORRECTLY)
                
                else :
                    return jsonify(Response.ERROR_DATABASE)
            
            else:
                return jsonify(Response.ERROR_USER_OR_PASS_WRONG)

        except:
            return jsonify(Response.ERROR_USER_NOT_EXIST)

    return jsonify(Response.ERROR_REQUEST_NOT_VALID)

@app.route(Routes.ROUTE_SELLS_APK, methods=['POST','GET'])
@limiter.limit("100 per day")
def Handle_Sellers_json():
    '''this function is used to handle the sells from one seller in json format'''

          

    Token = request.args.get('Token')

    if Helper.check_seller_from_token(Token):

        if request.method == 'POST':

            sells = str(request.json["sells"])

            if (Mysql.delete_user(sells.strip(),Token)):
                ret = {"code" : 200, "data" : f"delete user {sells.strip()} successfully !"}
                return jsonify(ret)

            else:
                return jsonify(Response.ERROR_DATABASE)

        users = []
        all_users = Mysql.read_users_for_seller_from_database(Token)
        user_counter = 0

        Sellers = Helper.Read_Sellers()
        Seller = {}

        for username_new, password_new in Sellers.items():

            if Helper.seller_hash(username_new,password_new) == Token:
                Seller[username_new] = password_new

            else:
                continue

        for user in all_users:

            user_db, password_db, Token_seller, Token_seller, token_db, verified, Device, Device_OS , created_date, expierd_date= user

            exdays = Helper.Calculate_expired_days_from_date(expierd_date)

            users.append({'username' : user_db, 'password' : password_db, 'days' : exdays, 'token' : token_db, 'Device' : Device, 'OS' : Device_OS})
            user_counter += 1

        json_data = {"code" : 200, "users" : users, "count" : user_counter, "seller" : Seller}
        return jsonify(json_data)

    else:
        return jsonify(Response.ERROR_USER_OR_PASS_WRONG)

@app.route(Routes.ROUTE_SELLS_WEB, methods=['POST','GET'])
@limiter.limit("100 per day")
def Handle_Sellers():
    '''this function is used to handle the sells from one seller'''

          

    Token = request.args.get('Token')

    if Helper.check_seller_from_token(Token):

        if request.method == 'POST':

            sells = str(request.json["sells"])

            if (Mysql.delete_user(sells.strip(),Token)):
                ret = {"code" : 200, "data" : f"delete user {sells.strip()} successfully !"}
                return jsonify(ret)

            else:
                return jsonify(Response.ERROR_DATABASE)

        users = []
        all_users = Mysql.read_users_for_seller_from_database(Token)
        user_counter = 0

        Sellers = Helper.Read_Sellers()
        Seller = {}

        for username_new, password_new in Sellers.items():

            if Helper.seller_hash(username_new,password_new) == Token:
                
                Seller[username_new] = password_new
                break

            else:
                continue

        seller_payed = Helper.Read_Sellers_payed(username_new)

        for user in all_users:
            
            user_db, password_db, Token_seller, Token_seller, token_db, verified, Device, Device_OS , created_date, expierd_date= user
            
            exdays = Helper.Calculate_expired_days_from_date(expierd_date)

            users.append({'username' : user_db, 'password' : password_db, 'days' : exdays, 'token' : token_db, 'Device' : Device, 'OS' : Device_OS})
            user_counter += 1

        json_data = {"users" : users, "count" : user_counter, "seller" : Seller, "payed" : seller_payed}
        return render_template('seller.html', data = json_data)

    else:
        return redirect(url_for('Handle_Seller'))

@app.route(Routes.ROUTE_MAKE_PHASH, methods=['POST','GET'])
def handle_make_payment_hash():
    '''this function is used to handle the make payment hash'''

    if request.method == 'POST':

        value = request.json['value']
        token = request.json['token']

        user = Mysql.read_one_users_with_token_or_404_from_database(token)

        if user != None:

            user_db, password_db, phone_number, email, token_db, verified, Device, Device_OS , created_date, expierd_date, FreeTimeExpired = user

            if token == token_db:

                payment_hash = Helper.make_payment_hash(value,token)
                ret = {"code" : 200, "payment_hash" : payment_hash}
                return jsonify(ret)
            
            return jsonify(Response.ERROR_USER_OR_PASS_WRONG)    

        return jsonify(Response.ERROR_USER_OR_PASS_WRONG)

    return jsonify(Response.ERROR_REQUEST_NOT_VALID)

@app.route(Routes.ROUTE_CHECK_PAY,methods=["GET","POST"])
def handle_check_payment():
    '''this function is used to handle the check payment'''

    if request.method == "POST":
        
        txid = request.json["txid"]
        value = request.json['value']
        token = request.json['token']
        
        
        new_expiration_date = Helper.calculate_new_expiration_date(value)
        payment_hash = Helper.make_payment_hash(value,token)

        if Helper.Check_Payment(txid,payment_hash):
            if Mysql.update_user(token, new_expiration_date) and Mysql.write_txid_to_database(txid, new_expiration_date):

                return jsonify(Response.PAYMENT_SUCCESSFULLY)

            else:
                return jsonify(Response.ERROR_DATABASE)
        
        else:
            return jsonify(Response.ERROR_PAYMENT_NOT_VALID)

    return jsonify(Response.ERROR_REQUEST_NOT_VALID)

@app.route(Routes.ROUTE_ADMIN,methods=["GET", "POST"])
def handle_admin_page():
    '''this function is used to handle the admin private page to manage all users'''

    if request.method == "POST":
        new_expiration_date = request.json["days"]
        token = str(request.json["data"])
        if (Mysql.update_user(token.strip(),new_expiration_date)):
            ret = {"code" : 200, "data" : f"update {token.strip()} expired days to {new_expiration_date} days!"}
            return jsonify(ret)

        else:
            return jsonify(Response.ERROR_DATABASE)
            
    all_users = Mysql.read_users_from_database()
    users = []
    for user in all_users:
        
        user_db, password_db, phone_number, email, token, verified, Device, Device_OS , created_date, expierd_date, FreeTimeExpired = user
    
        #exdays = Helper.Calculate_expired_days_from_date(expierd_date)

        if verified != "0":
            users.append({'username' : user_db, 'password' : password_db,'phone' : Helper.Read_Sellers_from_token(phone_number), 'days' : expierd_date, 'token' : token, 'Device' : Device, 'OS' : Device_OS})
        
        else:
            continue

    return render_template("admin.html", data = {"users" : users})   

@app.route(Routes.ROUTE_RIGISTER,methods=["GET", "POST"])
def handle_create_user():
    '''this function is used to handle the create user from rigisteration page'''

    if request.method == 'POST':
        password = Helper.generate_random_password()
        rpassword = password
        phone = "0"
        email = request.json["email"]
        username = email
        
        token = Helper.generate_token(email)

        try :
            if Helper.Check_User(email,token) and password == rpassword:
                
                Helper.Send_Registration_Email(username,password,token)

                current_date, Expired_date = Helper.free_plan_dates()

                if Mysql.write_user_to_database(username, password, phone, email, token, "0", current_date, Expired_date):
                    
                    return jsonify(Response.CREATE_USER_CORRECTLY_NOT_VERIFIED)
                
                else :
                
                    return jsonify(Response.ERROR_DATABASE)
            
            else:
            
                return jsonify(Response.ERROR_USER_OR_PASS_WRONG)

        except:

            return jsonify(Response.ERROR_USER_NOT_EXIST)

    return render_template("register.html")

@app.route(Routes.ROUTE_AUTHENTICATE, methods=['GET', 'POST'])
def handle_Authentication_new_user():
    '''this function is used to handle the authentication of new user that rigistered a account but did not verify by the email'''

    Token = request.args.get('Token')
    
    
    if Mysql.update_user_registration(Token) and Helper.Check_User_Reverse(Token):
    
        message = "User verified successfully"
        return render_template("index.html", message = message)


    alert = "Error verifying user"
    return render_template("index.html", alert = alert)

@app.route('/privacy',methods=["GET", "POST"])
def handle_privacy_page():
    '''this function is used to handle the privacy page'''

    return render_template("privacy.html")

@app.route(Routes.ROUTE_MAIN,methods=["GET", "POST"])
def handle_main_page():
    '''this function is used to handle the main page'''

    # run Expiration.py
    

    return render_template("index.html")

@app.route(Routes.ROUTE_CHANGE_PASS, methods=["GET", "POST"])
def handle_change_password():
    """this function is used to handle the change password by user """
    
    if request.method == 'POST':

        username = request.json["email"]
        password = request.json["pass"]
        new_password = request.json["newpass"]

        user = Mysql.read_one_users_or_404_from_database(username)

        if user != None:

            user_db, password_db, phone_number, email, token, verified, Device, Device_OS , created_date, expierd_date, FreeTimeExpired = user
            
            if username == user_db and password == password_db:

                if Mysql.update_user_password(username, new_password):

                    return jsonify(Response.CHANGE_PASSWORD_CORRECTLY)
                
                else:

                    return jsonify(Response.ERROR_DATABASE)
            
            return jsonify(Response.ERROR_USER_OR_PASS_WRONG)
        
        return jsonify(Response.ERROR_USER_NOT_EXIST)
    
    return jsonify(Response.ERROR_REQUEST_NOT_VALID)

@app.route(Routes.ROUTE_ADDS, methods=["GET", "POST"])
def handle_Free_Plan_By_Adds():
    """this function is used to handle the get free plan by watching adds"""
    
    if request.method == 'POST':

        username = request.json["email"]
        password = request.json["pass"]
        Device_GET = request.json['Device']
        Device_OS_GET = request.json['OS']

        user = Mysql.read_one_users_or_404_from_database(username)

        if user != None:

            user_db, password_db, phone_number, email, token, verified, Device, Device_OS , created_date, expierd_date, FreeTimeExpired = user
            
            if username == user_db and password == password_db and Device == Device_GET and Device_OS == Device_OS_GET:
                
                new_expiration_date = Helper.One_Hour_from_Now()

                if Mysql.update_user_free_plan_time(username, new_expiration_date):

                    return jsonify(Response.UPDATE_FREE_PLAN_CORRECTLY)
                
                else:

                    return jsonify(Response.ERROR_DATABASE)
            
            return jsonify(Response.ERROR_USER_OR_PASS_WRONG)
        
        return jsonify(Response.ERROR_USER_NOT_EXIST)
    
    return jsonify(Response.ERROR_REQUEST_NOT_VALID)


@app.route(Routes.ROUTE_LOGIN,methods=["GET", "POST"])
def handle_login_user():
    '''this function is used to handle the login users from aplication'''

    # run Expiration.py
    

    if request.method == 'POST':

        username = request.json["email"]
        passw = request.json["pass"]
        Device_GET = request.json['Device']
        Device_OS_GET = request.json['OS']

        if username == CONFIG.ALTER_USERNAME and passw == CONFIG.ALTER_PASSWORD:

            Servers_v = Helper.Read_servers()
            Servers_v_MTN = Helper.Read_servers_irancell()
            Servers_v_MCI = Helper.Read_servers_hamrah()
            servers_o = [] #TODO: add it for next update

            update_info = {"version" : CONFIG.VERSION , "force" : CONFIG.VERSION_TYPE, "links" : CONFIG.DOWNLOAD_LINK}
            prices = {"1month" : CONFIG.PRICE_ONE_MONTH, "2month" : CONFIG.PRICE_TWO_MONTH, "3month" : CONFIG.PRICE_TRE_MONTH}
            ret = {"code" : 200, "data" : {'password' : CONFIG.ALTER_PASSWORD, 'username' : CONFIG.ALTER_USERNAME, 'days' : "999", 'token' : "GOD"}, "v2ray" : Servers_v, "MTN" : Servers_v_MTN, "MCI" : Servers_v_MCI, "openconnect" : servers_o, "prices" : prices, "update_info" : update_info}
            return jsonify(ret)

        user = Mysql.read_one_users_or_404_from_database(username)
        user_data = {}

        if user != None:

            user_db, password_db, phone_number, email, token, verified, Device, Device_OS , created_date, expierd_date, FreeTimeExpired = user

            exdays = Helper.Calculate_expired_days_from_date(expierd_date)

            if verified != "0":

                user_data[username] = {'password' : password_db, 'username' : email, 'days' : exdays, 'token' : token, 'Device' : Device, 'OS' : Device_OS} 

                if Device is not None and Device_OS is not None:

                    Servers_v = Helper.Read_servers()
                    Servers_v_MTN = Helper.Read_servers_irancell()
                    Servers_v_MCI = Helper.Read_servers_hamrah()
                    servers_o = [] #TODO: add it for next update

                    update_info = {"version" : CONFIG.VERSION , "force" : CONFIG.VERSION_TYPE, "links" : CONFIG.DOWNLOAD_LINK}

                    if (username == user_db and passw == password_db and Device == Device_GET and Device_OS == Device_OS_GET and int(exdays) > 0):

                        prices = {"1month" : CONFIG.PRICE_ONE_MONTH, "2month" : CONFIG.PRICE_TWO_MONTH, "3month" : CONFIG.PRICE_TRE_MONTH}
                        ret = {"code" : 200, "data" : user_data[username], "v2ray" : Servers_v , "MTN" : Servers_v_MTN, "MCI" : Servers_v_MCI , "openconnect" : servers_o, "prices" : prices, "update_info" : update_info}
                        return jsonify(ret)
                    
                    elif (username == user_db and passw == password_db and Device == Device_GET and Device_OS == Device_OS_GET and Helper.Check_Free_Plan_Time(username)):

                        prices = {"1month" : CONFIG.PRICE_ONE_MONTH, "2month" : CONFIG.PRICE_TWO_MONTH, "3month" : CONFIG.PRICE_TRE_MONTH}
                        ret = {"code" : 200, "data" : user_data[username], "v2ray" : Servers_v , "MTN" : Servers_v_MTN, "MCI" : Servers_v_MCI , "openconnect" : servers_o, "prices" : prices, "update_info" : update_info}
                        return jsonify(ret)

                    elif (Device != Device_GET or Device_OS != Device_OS_GET):

                        ret = {"code" : 202, "data" : "You have an other device logged in this account", "Devices" : [{'os': Device_OS, 'Device': Device}]}
                        return jsonify(ret)

                    else:
                        
                        return jsonify(Response.ERROR_DONE_EXPIRE_TIME)    

                elif Mysql.add_user_device_to_database(username, Device_GET, Device_OS_GET):

                    return jsonify(Response.DEVICE_AND_OS_SET_CORRECTLY)

                return jsonify(Response.ERROR_DATABASE)

            return jsonify(Response.ERROR_USER_NOT_VERIFIED)

        return jsonify(Response.ERROR_USER_NOT_EXIST)

    return jsonify(Response.ERROR_REQUEST_NOT_VALID)

if __name__ == "__main__":
    app.run(CONFIG.HOST,CONFIG.RUNNING_PORT,debug=CONFIG.DEBUG_MODE)