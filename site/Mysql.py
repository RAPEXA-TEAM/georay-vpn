#!/usr/bin/env

#import libraries that are needed

import pymysql
import CONFIG     #SERVER CONGIG

def connect_to_database():
    '''This function make a connection with datebase'''
    
    db = pymysql.connect(host=CONFIG.MYSQL_HOST,
                       user=CONFIG.MYSQL_USER,
                       passwd=CONFIG.MYSQL_PASS,
                       db=CONFIG.MYSQL_DATABAS)
    return(db)

def update_user(token, new_expiration_date):
    '''this function update user expired time on database'''
    
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'UPDATE users SET ExpiredDate = "{new_expiration_date}" where token = "{token}";'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def update_user_free_plan_time(user, new_expiration_date):
    '''this function update user expired time on database'''
    
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'UPDATE users SET FreeTimeExpired = "{new_expiration_date}" where user = "{user}";'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def update_user_password(username, password):
    '''this function update user password on database'''
    
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'UPDATE users SET password = "{password}" where user = "{username}";'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def update_user_usage_from_database(username,usage):

    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'UPDATE users SET usagee = "{usage}" where user = "{username}";'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def add_user_device_to_database(email, Device, OS):
    '''this function update user expired time on database'''
    
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'UPDATE users SET Device = "{Device}", OS = "{OS}" where user = "{email}";'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def delete_user_device_from_database(email):
    '''this function update user expired time on database'''
    
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'UPDATE users SET Device = NULL, OS = NULL where user = "{email}";'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def update_user_registration(Token):
    '''this function update user registration status on database'''
    
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'UPDATE users SET verified = "1" where token = "{Token}";'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def update_seller_paid_accounts(seller,payed):
    
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'UPDATE sellers SET Paidusers = "{payed}" where selleruser = "{seller}";'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def write_user_to_database(username, password, phone, email, token, verified, CreatedDate, ExpiredDate):
    '''this function create user on database'''
    
    db = connect_to_database()
    cur = db.cursor()                
    qury = f'INSERT INTO users (user, password, phone, email, token, verified, Device, OS, CreatedDate, ExpiredDate, FreeTimeExpired, usagee) VALUES ("{username}", "{password}", "{phone}", "{email}", "{token}", "{verified}", NULL, NULL, "{CreatedDate}", "{ExpiredDate}", "{ExpiredDate}", "0");'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def write_seller_to_database(selleruser, sellerpassword, sellertoken, CreatedDate, Paidusers, Sellusers, Reseller=None):
    '''this function create seller and reseller on database'''

    db = connect_to_database()
    cur = db.cursor()
    qury = f'INSERT INTO sellers (selleruser, sellerpassword, sellertoken, CreatedDate, Paidusers, Sellusers, Reseller) VALUES ("{selleruser}", "{sellerpassword}", "{sellertoken}", "{CreatedDate}", "{Paidusers}", "{Sellusers}", "{Reseller}");'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def write_user_from_seller_to_database(username, password, Token_seller, token, CreatedDate, ExpiredDate):
    '''this function create user that seller sells on database'''
    
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'INSERT INTO users (user, password, phone, email, token, verified, Device, OS, CreatedDate, ExpiredDate, FreeTimeExpired, usagee) VALUES ("{username}", "{password}", "{Token_seller}", "{Token_seller}", "{token}", "1", NULL, NULL, "{CreatedDate}", "{ExpiredDate}", "{ExpiredDate}", "0");'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def write_txid_to_database(txid, new_expiration_date):
    '''this function write verified tx-ids on database'''

    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'INSERT INTO txids (txid, days, time) VALUES ("{txid}", "{new_expiration_date}", now());'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def read_txids_from_database():
    '''this function return all verified tx-ids that used before'''

    db = connect_to_database()
    cur = db.cursor()
    qury = f'SELECT * FROM txids;'
    cur.execute(qury)
    db.close()
    return cur.fetchall()

def read_users_from_database():
    '''this function return all users information from database'''

    db = connect_to_database()
    cur = db.cursor()
    qury = f'SELECT * FROM users;'
    cur.execute(qury)
    db.close()
    return cur.fetchall()

def read_all_sellers_from_database():
    '''this function return all users information from database'''

    db = connect_to_database()
    cur = db.cursor()
    qury = f'SELECT * FROM sellers;'
    cur.execute(qury)
    db.close()
    return cur.fetchall()

def read_one_seller_from_database_with_token_or_404(sellertoken):
    '''this function return all users information from database'''

    db = connect_to_database()
    cur = db.cursor()
    qury = f'SELECT * FROM sellers where sellertoken = "{sellertoken}";'
    cur.execute(qury)
    db.close()
    return cur.fetchone()

def read_one_seller_from_database_or_404(username):
    '''this function return all users information from database'''

    db = connect_to_database()
    cur = db.cursor()
    qury = f'SELECT * FROM sellers where selleruser = "{username}";'
    cur.execute(qury)
    db.close()
    return cur.fetchone()

def read_resellers_for_Seller_from_database_or_404(selleruser):
    '''this function return all users information from database'''

    db = connect_to_database()
    cur = db.cursor()
    qury = f'SELECT * FROM sellers where Reseller = "{selleruser}";'
    cur.execute(qury)
    db.close()
    return cur.fetchall()

def read_one_users_or_404_from_database(email):
    '''this function return all users information from database'''

    db = connect_to_database()
    cur = db.cursor()
    qury = f'select * from users where user = "{email}";'
    cur.execute(qury)
    db.close()
    return cur.fetchone()

def read_one_users_with_token_or_404_from_database(token):
    '''this function return all users information from database'''

    db = connect_to_database()
    cur = db.cursor()
    qury = f'select * from users where token = "{token}";'
    cur.execute(qury)
    db.close()
    return cur.fetchone()

def read_users_for_seller_from_database(Token_seller):
    '''this function return all users information that one seller sells'''

    db = connect_to_database()
    cur = db.cursor()
    qury = f"SELECT * FROM users WHERE phone = '{Token_seller}' AND email = '{Token_seller}';"
    cur.execute(qury)
    db.close()
    return cur.fetchall()

def read_users_count_for_seller_from_database(Token_seller):
    '''this function return all users information that one seller sells'''

    db = connect_to_database()
    cur = db.cursor()
    qury = f"SELECT count(*) FROM users WHERE phone = '{Token_seller}' AND email = '{Token_seller}';"
    cur.execute(qury)
    db.close()
    return cur.fetchone()

def delete_user(token,token_seller):

    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'DELETE FROM users WHERE phone = "{token_seller}" AND token = "{token}";'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def delete_user_with_token(token):

    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'DELETE FROM users WHERE token = "{token}";'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def delete_seller(seller):

    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'DELETE FROM sellers WHERE selleruser = "{seller}";'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def delete_reseller_for_seller(seller,reseller):

    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'DELETE FROM sellers WHERE selleruser = "{reseller}" AND Reseller = "{seller}";'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True