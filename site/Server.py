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
import TEXT       #SERVER RESPONSE

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

            user_db, password_db, phone_number, email, token, verify, Device, Device_OS , created_date, expierd_date, FreeTimeExpired, usage_db = user
            
            if (username == user_db and passw == password_db and Device == Device_GET and Device_OS == Device_OS_GET):

                if Mysql.delete_user_device_from_database(username):

                    return jsonify({"code" : 200, "data" : TEXT.LOGOUT_CORRECTLY})
                
                else:

                    return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})
            
            return jsonify({"code" : 401, "data" : TEXT.ERROR_USER_OR_PASS_WRONG})
        
        return jsonify({"code" : 404, "data" : TEXT.ERROR_USER_NOT_EXIST})
    
    return jsonify({"code" : 402, "data" : TEXT.ERROR_REQUEST_NOT_VALID})

@app.route(Routes.ROUTE_UPDATE_DATA_USAGE, methods=['POST','GET'])
def update_user_usage():
    '''this function is used to update one gig more user'''

    if request.method == 'POST':
        
        username = request.json["email"]
        password = request.json["password"]
        
        user = Mysql.read_one_users_or_404_from_database(username)

        if user != None:

            user_db, password_db, phone_number, email, token, verify, Device, Device_OS , created_date, expierd_date, FreeTimeExpired, usage_db = user
            
            if usage_db is not None:

                usage = int(usage_db) + 1

                if username == user_db and password == password_db:

                    if Mysql.update_user_usage_from_database(username,str(usage)):

                        return jsonify({"code" : 200, "data" : TEXT.USED_ONE_GIG_MORE})
                    
                    else:

                        return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})
            
                return jsonify({"code" : 401, "data" : TEXT.ERROR_USER_OR_PASS_WRONG})
            
            else:

                usage = 1

                if username == user_db and password == password_db:

                    if Mysql.update_user_usage_from_database(username,str(usage)):

                        return jsonify({"code" : 200, "data" : TEXT.USED_ONE_GIG_MORE})
                    
                    else:

                        return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})
            
            return jsonify({"code" : 401, "data" : TEXT.ERROR_USER_OR_PASS_WRONG})
        
        return jsonify({"code" : 404, "data" : TEXT.ERROR_USER_NOT_EXIST})
    
    return jsonify({"code" : 402, "data" : TEXT.ERROR_REQUEST_NOT_VALID})

@app.route(Routes.ROUTE_UPDATE, defaults={'lng': None})
@app.route(Routes.ROUTE_UPDATE+"/<lng>") 
def handle_update(lng):
    '''this function is used to update apps'''

    if lng == None:
        
        time = Helper.Server_time()
        ret = {"version" : CONFIG.VERSION , "force" : CONFIG.VERSION_TYPE, "links" : CONFIG.DOWNLOAD_LINK, "ServerTime" : time, "data" : Helper.app_data_in_lang(CONFIG.ENGLISH)}
        return jsonify(ret)

    elif lng == "en":

        time = Helper.Server_time()
        ret = {"version" : CONFIG.VERSION , "force" : CONFIG.VERSION_TYPE, "links" : CONFIG.DOWNLOAD_LINK, "ServerTime" : time, "data" : Helper.app_data_in_lang(CONFIG.ENGLISH)}
        return jsonify(ret)
    
    elif lng == "fa":

        time = Helper.Server_time()
        ret = {"version" : CONFIG.VERSION , "force" : CONFIG.VERSION_TYPE, "links" : CONFIG.DOWNLOAD_LINK, "ServerTime" : time, "data" : Helper.app_data_in_lang(CONFIG.FARSI)}
        return jsonify(ret)

    time = Helper.Server_time()
    ret = {"version" : CONFIG.VERSION , "force" : CONFIG.VERSION_TYPE, "links" : CONFIG.DOWNLOAD_LINK, "ServerTime" : time, "data" : Helper.app_data_in_lang(lng)}
    return jsonify(ret)

@app.route(Routes.ROUTE_SELLER, methods=['POST','GET'])
@limiter.limit("50 per day")
def Handle_Seller():
    '''this function is used to handle the seller login page'''

    if request.method == 'POST':

        username = request.json['username']
        password = request.json['password']

        if Helper.Check_Seller_Login(username, password):

            token = Helper.seller_hash(username,password)
            ret = {"code" : 200 , "Token" : token}
            return jsonify(ret)

        else:
            return jsonify({"code" : 401, "data" : TEXT.ERROR_USER_OR_PASS_WRONG})

    return render_template('login.html')

@app.route(Routes.ROUTE_ADD_RESELLER,methods=['GET', 'POST'])
def handle_seller_add_reseller():

    if request.method == "POST":
        
        reseller = str(request.json["reseller"])
        seller = str(request.json["seller"]).strip()
        Token_seller = str(request.json["tokenseller"])

        password = Helper.generate_random_password()
        Sellers = Helper.Read_Sellers()
        Tokens = []
        Token = Helper.reseller_hash_from_seller(reseller)
        CreatedDate, ExpiredDate = Helper.monthly_plan_dates()

        for username_db, password_db in Sellers.items():  
            Tokens.append(Helper.seller_hash(username_db,password_db))

        if Helper.Check_Seller(reseller) and Token_seller in Tokens:

            if Mysql.write_seller_to_database(reseller.strip(), password, Token, CreatedDate, "1", "0", seller):
                ret = {"code" : 200, "data" : f"add reseller {reseller.strip()} successfully for seller {seller.strip()}!"}
                return jsonify(ret)

            return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})
        
        return jsonify({"code" : 401, "data" : TEXT.ERROR_USER_OR_PASS_WRONG})
    
    return jsonify({"code" : 402, "data" : TEXT.ERROR_REQUEST_NOT_VALID})

@app.route(Routes.ROUTE_DEL_RESELLER,methods=["GET", "POST"])
def handle_seller_delete_reseller():

    if request.method == "POST":
        
        reseller = str(request.json["reseller"])
        seller = str(request.json["seller"])
        Token_seller = str(request.json["tokenseller"])

        Sellers = Helper.Read_Sellers()
        Tokens = []

        for username_db, password_db in Sellers.items():  
            Tokens.append(Helper.seller_hash(username_db,password_db))

        if Token_seller in Tokens:

            if (Mysql.delete_reseller_for_seller(seller.strip(),reseller.strip())):
                ret = {"code" : 200, "data" : f"delete reseller {reseller.strip()} successfully for seller {seller.strip()}!"}
                return jsonify(ret)

            return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})
        
        return jsonify({"code" : 401, "data" : TEXT.ERROR_USER_OR_PASS_WRONG})
    
    return jsonify({"code" : 402, "data" : TEXT.ERROR_REQUEST_NOT_VALID})

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
            
                    return jsonify({"code" : 200, "data" : TEXT.CREATE_USER_CORRECTLY})
                
                else :
                    return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})
            
            else:
                return jsonify({"code" : 401, "data" : TEXT.ERROR_USER_OR_PASS_WRONG})

        except:
            return jsonify({"code" : 404, "data" : TEXT.ERROR_USER_NOT_EXIST})

    return jsonify({"code" : 402, "data" : TEXT.ERROR_REQUEST_NOT_VALID})

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
                return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})

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

            user_db, password_db, Token_seller, Token_seller, token_db, verified, Device, Device_OS , created_date, expierd_date, FreeTimeExpired, usage = user

            exdays = Helper.Calculate_expired_days_from_date(expierd_date)

            users.append({'username' : user_db, 'password' : password_db, 'days' : exdays, 'token' : token_db, 'Device' : Device, 'OS' : Device_OS})
            user_counter += 1

        json_data = {"code" : 200, "users" : users, "count" : user_counter, "seller" : Seller}
        return jsonify(json_data)

    else:
        return jsonify({"code" : 401, "data" : TEXT.ERROR_USER_OR_PASS_WRONG})

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
                return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})

        users = []
        Sellerslist = []
        all_users = Mysql.read_users_for_seller_from_database(Token)
        user_counter = 0

        Sellers = Helper.Read_Sellers()
        Seller = {}

        for username_new, password_new in Sellers.items():

            if Helper.seller_hash(username_new,password_new) == Token:
                
                Seller[username_new] = password_new
                allsellers = Mysql.read_resellers_for_Seller_from_database_or_404(username_new)
                break

            else:
                continue

        seller_payed = int(Helper.Read_Sellers_payed(username_new))
        reseller_sells = 0

        for user in all_users:
            
            user_db, password_db, Token_seller, Token_seller, token_db, verified, Device, Device_OS , created_date, expierd_date, FreeTimeExpired, usage = user
            
            exdays = Helper.Calculate_expired_days_from_date(expierd_date)

            users.append({'username' : user_db, 'password' : password_db, 'days' : exdays, 'ExDate' : expierd_date, 'CrDate' : created_date, 'FrDate' : FreeTimeExpired, 'token' : token_db, 'Device' : Device, 'OS' : Device_OS})
            user_counter += 1

        for seller in allsellers:
            
            selleruser, sellerpassword, sellertoken, sellerCreatedDate, Paidusers, Sellusers_db, Reseller = seller
            Sellusers,=Mysql.read_users_count_for_seller_from_database(sellertoken)

            Sellerslist.append({'username' : selleruser, 'password' : sellerpassword,'CrDate' : sellerCreatedDate, 'token' : sellertoken, 'Paids' : Paidusers, 'Sells' : str(Sellusers) , "Reseller" : Reseller})
            
            reseller_sells += int(Sellusers)
            seller_payed += int(Paidusers)

        json_data = {"users" : users, "sellers" : Sellerslist, "count" : user_counter, "seller" : Seller, "payed" : str(seller_payed) ,"resellersSells" : str(reseller_sells)}
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

            user_db, password_db, phone_number, email, token_db, verified, Device, Device_OS , created_date, expierd_date, FreeTimeExpired, usage = user

            if token == token_db:

                payment_hash = Helper.make_payment_hash(value,token)
                ret = {"code" : 200, "payment_hash" : payment_hash}
                return jsonify(ret)
            
            return jsonify({"code" : 401, "data" : TEXT.ERROR_USER_OR_PASS_WRONG})    

        return jsonify({"code" : 401, "data" : TEXT.ERROR_USER_OR_PASS_WRONG})

    return jsonify({"code" : 402, "data" : TEXT.ERROR_REQUEST_NOT_VALID})

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

                return jsonify({"code" : 200, "data" : TEXT.PAYMENT_SUCCESSFULLY})

            else:
                return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})
        
        else:
            return jsonify({"code" : 405, "data" : TEXT.ERROR_PAYMENT_NOT_VALID})

    return jsonify({"code" : 402, "data" : TEXT.ERROR_REQUEST_NOT_VALID})

@app.route(Routes.ROUTE_ADMIN_DEL_SELLER,methods=["GET", "POST"])
def handle_admin_delete_seller():

    if request.method == "POST":
            
        seller = str(request.json["seller"]).strip()

        if (Mysql.delete_seller(seller)):
            ret = {"code" : 200, "data" : f"delete seller {seller} successfully !"}
            return jsonify(ret)

        else:
            return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})

    return jsonify({"code" : 402, "data" : TEXT.ERROR_REQUEST_NOT_VALID})

@app.route(Routes.ROUTE_ADMIN_ADD_SELLER,methods=["GET", "POST"])
def handle_admin_add_seller():

    if request.method == "POST":

        seller = str(request.json["seller"]).strip()
        password = Helper.generate_random_password()
        current_date, Expired_date = Helper.free_plan_dates()

        if (Mysql.write_seller_to_database(seller, password, Helper.reseller_hash_from_seller(seller), current_date, "1", "0", None)):
            ret = {"code" : 200, "data" : f"add seller {seller} successfully !"}
            return jsonify(ret)

        else:
            return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})

    return jsonify({"code" : 402, "data" : TEXT.ERROR_REQUEST_NOT_VALID})

@app.route(Routes.ROUTE_ADMIN_EDI_SELLER,methods=["GET", "POST"])
def handle_admin_edit_seller():

    if request.method == "POST":

        seller = str(request.json["seller"]).strip()
        payed = str(request.json["payed"]).strip()

        if (Mysql.update_seller_paid_accounts(seller,payed)):
            ret = {"code" : 200, "data" : f"update seller {seller} successfully to {payed} payed accounts!"}
            return jsonify(ret)

        else:
            return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})

    return jsonify({"code" : 402, "data" : TEXT.ERROR_REQUEST_NOT_VALID})

@app.route(Routes.ROUTE_ADMIN_DEL_USER,methods=["GET", "POST"])
def handle_admin_delete_user():

    if request.method == "POST":
            
        token = str(request.json["token"]).strip()

        if (Mysql.delete_user_with_token(token)):
            ret = {"code" : 200, "data" : f"delete user {token} successfully !"}
            return jsonify(ret)

        else:
            return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})

    return jsonify({"code" : 402, "data" : TEXT.ERROR_REQUEST_NOT_VALID})

@app.route(Routes.ROUTE_ADMIN,methods=["GET", "POST"])
def handle_admin_page():
    '''this function is used to handle the admin private page to manage all users'''

    if request.method == "POST":
        new_expiration_date = request.json["NewExDate"]
        token = str(request.json["data"])
        if (Mysql.update_user(token.strip(),new_expiration_date)):
            ret = {"code" : 200, "data" : f"update {token.strip()} expired days!"}
            return jsonify(ret)

        else:
            return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})
            
    all_users = Mysql.read_users_from_database()
    users = []
    for user in all_users:
        
        user_db, password_db, phone_number, email, token, verified, Device, Device_OS , created_date, expierd_date, FreeTimeExpired, usage_db = user
    
        exdays = Helper.Calculate_expired_days_from_date(expierd_date)

        if verified != "0":
            users.append({'username' : user_db, 'password' : password_db,'phone' : Helper.Read_Sellers_from_token(phone_number), 'days' : exdays, 'ExDate' : expierd_date, 'CrDate' : created_date, 'FrDate' : FreeTimeExpired , 'token' : token, 'Device' : Device, 'OS' : Device_OS, 'usage' : Helper.return_usage(usage_db)})
        
        else:
            continue

    all_sellers = Mysql.read_all_sellers_from_database()
    Sellers = []

    for Seller in all_sellers:
        
        selleruser, sellerpassword, sellertoken, sellerCreatedDate, Paidusers, Sellusers_db, Reseller = Seller
        Sellusers,=Mysql.read_users_count_for_seller_from_database(sellertoken)
        mount = int(Sellusers) - int(Paidusers)
        Sellers.append({'username' : selleruser, 'password' : sellerpassword,'CrDate' : sellerCreatedDate, 'token' : sellertoken, 'Paids' : Paidusers, 'Sells' : str(Sellusers) , 'Amount' : str(mount) ,"Reseller" : Reseller})

    return render_template("admin.html", data = {"users" : users, "sellers" : Sellers})   

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
                    
                    return jsonify({"code" : 200, "data" : TEXT.CREATE_USER_CORRECTLY_NOT_VERIFIED})
                
                else :
                
                    return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})
            
            else:
            
                return jsonify({"code" : 401, "data" : TEXT.ERROR_USER_OR_PASS_WRONG})

        except:

            return jsonify({"code" : 404, "data" : TEXT.ERROR_USER_NOT_EXIST})

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

            user_db, password_db, phone_number, email, token, verified, Device, Device_OS , created_date, expierd_date, FreeTimeExpired, usage = user
            
            if username == user_db and password == password_db:

                if Mysql.update_user_password(username, new_password):

                    return jsonify({"code" : 200, "data" : TEXT.CHANGE_PASSWORD_CORRECTLY})
                
                else:

                    return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})
            
            return jsonify({"code" : 401, "data" : TEXT.ERROR_USER_OR_PASS_WRONG})
        
        return jsonify({"code" : 404, "data" : TEXT.ERROR_USER_NOT_EXIST})
    
    return jsonify({"code" : 402, "data" : TEXT.ERROR_REQUEST_NOT_VALID})

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

            user_db, password_db, phone_number, email, token, verified, Device, Device_OS , created_date, expierd_date, FreeTimeExpired, usage = user
            
            if username == user_db and password == password_db and Device == Device_GET and Device_OS == Device_OS_GET:
                
                new_expiration_date = Helper.One_Hour_from_Now()

                if Mysql.update_user_free_plan_time(username, new_expiration_date):

                    return jsonify({"code" : 200, "data" : TEXT.UPDATE_FREE_PLAN_CORRECTLY, "ExpiredTime" : new_expiration_date})
                
                else:

                    return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})
            
            return jsonify({"code" : 401, "data" : TEXT.ERROR_USER_OR_PASS_WRONG})
        
        return jsonify({"code" : 404, "data" : TEXT.ERROR_USER_NOT_EXIST})
    
    return jsonify({"code" : 402, "data" : TEXT.ERROR_REQUEST_NOT_VALID})


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

            user_db, password_db, phone_number, email, token, verified, Device, Device_OS , created_date, expierd_date, FreeTimeExpired, usage = user

            exdays = Helper.Calculate_expired_days_from_date(expierd_date)

            if verified != "0":

                user_data[username] = {'password' : password_db, 'username' : user_db, 'days' : exdays, 'token' : token, 'Device' : Device, 'OS' : Device_OS, 'usage' : Helper.return_usage(usage)} 

                if Device is not None and Device_OS is not None:

                    Servers_v = Helper.Read_servers()
                    Servers_v_MTN = Helper.Read_servers_irancell()
                    Servers_v_MCI = Helper.Read_servers_hamrah()
                    Servers_v_MKH = Helper.Read_servers_MOKH()
                    Servers_free_v = Helper.Read_free_servers()
                    servers_o = [] #TODO: add it for next update

                    update_info = {"version" : CONFIG.VERSION , "force" : CONFIG.VERSION_TYPE, "links" : CONFIG.DOWNLOAD_LINK}

                    if (username == user_db and passw == password_db and Device == Device_GET and Device_OS == Device_OS_GET and int(exdays) > 0 and int(Helper.return_usage(usage)) < 20):

                        prices = {"1month" : CONFIG.PRICE_ONE_MONTH, "2month" : CONFIG.PRICE_TWO_MONTH, "3month" : CONFIG.PRICE_TRE_MONTH}
                        ret = {"code" : 200, "data" : user_data[username], "v2ray" : Servers_v , "MTN" : Servers_v_MTN, "MCI" : Servers_v_MCI, "MKH" : Servers_v_MKH , "openconnect" : servers_o, "prices" : prices, "update_info" : update_info}
                        return jsonify(ret)
                    
                    elif (username == user_db and passw == password_db and Device == Device_GET and Device_OS == Device_OS_GET and Helper.Check_Free_Plan_Time(username)):

                        prices = {"1month" : CONFIG.PRICE_ONE_MONTH, "2month" : CONFIG.PRICE_TWO_MONTH, "3month" : CONFIG.PRICE_TRE_MONTH}
                        ret = {"code" : 200, "data" : user_data[username], "v2ray" : Servers_v , "MTN" : Servers_v_MTN, "MCI" : Servers_v_MCI, "MKH" : Servers_v_MKH , "openconnect" : servers_o, "prices" : prices, "update_info" : update_info}
                        return jsonify(ret)

                    elif (Device != Device_GET or Device_OS != Device_OS_GET):

                        ret = {"code" : 202, "data" : TEXT.ERROR_YOU_HAVE_AN_OTHER_DEVICE_LOGIN, "Devices" : [{'os': Device_OS, 'Device': Device}]}
                        return jsonify(ret)

                    else:

                        ret = {"code" : 407, "data" : TEXT.ERROR_DONE_EXPIRE_TIME, "AddsServer" : Servers_free_v, "MTN" : Servers_v_MTN, "MCI" : Servers_v_MCI}                   
                        return jsonify(ret)    

                elif Mysql.add_user_device_to_database(username, Device_GET, Device_OS_GET):

                    return jsonify({"code" : 201, "data" : TEXT.DEVICE_AND_OS_SET_CORRECTLY})

                return jsonify({"code" : 403, "data" : TEXT.ERROR_DATABASE})

            return jsonify({"code" : 406, "data" : TEXT.ERROR_USER_NOT_VERIFIED})

        return jsonify({"code" : 404, "data" : TEXT.ERROR_USER_NOT_EXIST})

    return jsonify({"code" : 402, "data" : TEXT.ERROR_REQUEST_NOT_VALID})

if __name__ == "__main__":
    
    app.run(CONFIG.HOST,CONFIG.RUNNING_PORT,debug=CONFIG.DEBUG_MODE)
