#!/usr/bin/env

from web3 import Web3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googletrans import Translator

import TEXT
import smtplib
import datetime
import hashlib
import CONFIG
import Mysql
import random
import string
import json
import csv

def Send_Registration_Email(username,password,token):
    '''this function is used to send the registration email to the user'''

    # creates Message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Georay account Registertion"
    message["From"] = CONFIG.SENDER_EMAIL
    message["To"] = username

    text = f"""\
    Hi,
    Check out the link below To register your Georay VPN account:
    http://dv.d4rk4pp.sbs/Authentication?Token={token}
    \n
    username: {username}
    password: {password}
    """

    html = f"""\
    <html>
    <body>
        <p>Hi,<br>
        Check out the link below To register your Georay VPN account:</p>
        <p><a href="http://dv.d4rk4pp.sbs/Authentication?Token={token}">Register Now!</a></p>
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
    s.sendmail(CONFIG.SENDER_EMAIL, username, message.as_string())
    
    # terminating the session
    s.quit()
    return True

def generate_random_password():
    '''this function is used to generate a random password'''

    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(12))
    return result_str

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
        
def Read_servers():
    '''this function is used to read the servers from the csv file'''

    Servers = []

    with open(CONFIG.PATH_SERVERS, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            Servers.append(row[1])
    
    return Servers

def One_Hour_from_Now():

    return str(datetime.datetime.now() + datetime.timedelta(hours=CONFIG.FREE_PLAN_HOURS))

def Server_time():

    return str(datetime.datetime.now())

def Check_Free_Plan_Time(username):
    """this function checks the free plan time for one user"""

    user = Mysql.read_one_users_or_404_from_database(username)

    if user != None:

        user_db, password_db, phone_number, email_db, token_db, verified, Device, Device_OS , created_date, expierd_date, FreeTimeExpired, usage = user

        if FreeTimeExpired != None:

            # convert string to datetime
            dt1 = datetime.datetime.strptime(str(datetime.datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
            dt2 = datetime.datetime.strptime(FreeTimeExpired, "%Y-%m-%d %H:%M:%S.%f")

            if dt2 > dt1:

                return True
        
            else:

                return False
            
        else:

            date = str(datetime.datetime.now())

            if Mysql.update_user_free_plan_time(username, date):

                return False

    else:

        return False

def Read_servers_irancell():
    '''this function is used to read the irancell servers from the csv file'''

    Servers = []

    with open(CONFIG.PATH_SERVERS_MTN, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            Servers.append(row[1])
    
    return Servers

def Read_servers_DNSs():
    '''this function is used to read the DNS servers from the csv file'''

    Servers = []

    with open(CONFIG.PATH_SERVERS_DNS, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            Servers.append(row[1])
    
    return Servers

def Read_servers_hamrah():
    '''this function is used to read the hamrah aval servers from the csv file'''

    Servers = []

    with open(CONFIG.PATH_SERVERS_MCI, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            Servers.append(row[1])
    
    return Servers

def Read_servers_MOKH():

    Servers = []

    with open(CONFIG.PATH_SERVERS_MKH, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            Servers.append(row[1])

    return Servers

def Read_free_servers():
    '''this function is used to read the Free Saw Adds servers from the csv file'''

    Servers = []

    with open(CONFIG.PATH_FREE_SERVER, newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            Servers.append(row[1])
    
    return Servers

def Check_Seller_Login(username,password):
    Sellers = Read_Sellers()
    for username_for, password_for in Sellers.items():
        if username_for == username and password_for == password:
            return True
    return False

def Check_User_Reverse(token):
    '''this function is used to check if the new token is valid or not'''

    user = Mysql.read_one_users_with_token_or_404_from_database(token)

    if user != None:

        user_db, password_db, phone_number, email_db, token_db, verified, Device, Device_OS , created_date, expierd_date, FreeTimeExpired, usage = user

        if token == token_db:

            return True
                
    else:
        return False
    
def Check_User(email,token):
    '''this function is used to check if the new token is valid or not'''
    
    user = Mysql.read_one_users_or_404_from_database(email)

    if user != None:

        user_db, password_db, phone_number, email_db, token_db, verified, Device, Device_OS , created_date, expierd_date, FreeTimeExpired, usage = user
        
        if token == token_db:
               
            return False
                
    else:
        return True

def Check_Seller(token):
    '''this function is used to check if the new token is valid or not'''
    
    seller = Mysql.read_one_seller_from_database_or_404(token)

    if seller != None:

        selleruser, sellerpassword, sellertoken, sellerCreatedDate, Paidusers, Sellusers, Reseller = seller
        
        if token == sellertoken:
               
            return False
                
    else:
        return True

def check_seller_from_token(Token):
    
    Sellers = Read_Sellers()
    Tokens = []

    for username, password in Sellers.items():  
        Tokens.append(seller_hash(username,password))

    if Token in Tokens:

        return True
    
    return False

def Calculate_expired_days_from_date(expierd_date):
    """this function calculates expired days from date"""

    date_format = "%Y-%m-%d" #2023-03-12
    current_time = str(datetime.datetime.now())
    date = current_time.split(" ")[0]
    a = datetime.datetime.strptime(date, date_format)
    b = datetime.datetime.strptime(expierd_date, date_format)
    delta = b - a
    exdays = str(delta).split(" ")[0]
    
    if exdays == "0:00:00":

        return "0"
    
    return exdays

def free_plan_dates():

    current_time = str(datetime.datetime.now())
    current_date = current_time.split(" ")[0]
    Expired_time = datetime.datetime.today() + datetime.timedelta(days=CONFIG.FREE_DAYS)
    Expired_date = str(Expired_time).split(" ")[0] 

    return current_date, Expired_date

def monthly_plan_dates():

    current_time = str(datetime.datetime.now())
    current_date = current_time.split(" ")[0]
    Expired_time = datetime.datetime.today() + datetime.timedelta(days=CONFIG.MONTHLY_DAYS)
    Expired_date = str(Expired_time).split(" ")[0] 

    return current_date, Expired_date

def Read_Sellers():
    '''this function is used to read the sellers from the csv file'''

    Sellers = {}
    all_sellers = Mysql.read_all_sellers_from_database()
    
    for seller in all_sellers:
        selleruser, sellerpassword, sellertoken, sellerCreatedDate, Paidusers, Sellusers, Reseller = seller
        Sellers[selleruser] = sellerpassword
    
    return Sellers

def Read_Sellers_from_token(Token):
    '''this function is used to read the sellers from the csv file'''

    seller = Mysql.read_one_seller_from_database_with_token_or_404(Token)
    
    if seller != None:

        selleruser, sellerpassword, sellertoken, sellerCreatedDate, Paidusers, Sellusers, Reseller = seller
        
        if Token == sellertoken:

            return selleruser
        
        return "WebSite"

    return "WebSite"

def Read_Sellers_payed(Seller):
    '''this function is used to read the seller payed from the csv file'''

    sellerinfo = Mysql.read_one_seller_from_database_or_404(Seller)

    if sellerinfo != None:

        selleruser, sellerpassword, sellertoken, sellerCreatedDate, Paidusers, Sellusers, Reseller = sellerinfo
        
        if Seller == selleruser:

            return Paidusers

        return None
    
    return None

def generate_token(email):
    return hashlib.sha256(f"{email}-georay".encode('utf-8')).hexdigest()

def seller_hash(username,password):

    #return hashlib.sha256(("{"+str(username)+"}{"+str(password)+"}-georay").encode("utf-8")).hexdigest()
    return hashlib.sha256(("{"+str(username)+"}-georay").encode("utf-8")).hexdigest()

def reseller_hash_from_seller(username):
    return hashlib.sha256(("{"+str(username)+"}-georay").encode("utf-8")).hexdigest()

def make_payment_hash(value,token):
    return hashlib.sha256(f"{value}-{token}-georay".encode('utf-8')).hexdigest()

def calculate_new_expiration_date(value):
    """this function calculates the new expiration date from payed value"""

    days = int((int(value) / int(CONFIG.PRICE_ONE_MONTH)) * 30)
    New_Expired_Day_Date = datetime.datetime.today() + datetime.timedelta(days=days)
    date = str(New_Expired_Day_Date).split(" ")[0]

    return date

def return_usage(usage):

    if usage == None:

        return "0"
    
    return usage

def app_data_in_lang(lang):
    
    ENGLISH_DATA = TEXT.APP_DATA_ENGLISH
    PERSIAN_DATA = TEXT.APP_DATA_PERSIAN

    if lang == 'en':

        return ENGLISH_DATA
    
    if lang == 'fa':

        return PERSIAN_DATA

    else:
        
        trans = Translator()
        
        for key, value in ENGLISH_DATA.items():
        
            ENGLISH_DATA[key] = trans.translate(value,src="en",dest=lang).text
        
        return ENGLISH_DATA