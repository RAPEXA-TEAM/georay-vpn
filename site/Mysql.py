#!/usr/bin/env

#import libraries that are needed

import sys
import pymysql
import CONFIG     #SERVER CONGIG

def connect_to_database():
    '''This function make a connection with datebase'''
    
    db = pymysql.connect(host=CONFIG.MYSQL_HOST,
                       user=CONFIG.MYSQL_USER,
                       passwd=CONFIG.MYSQL_PASS,
                       db=CONFIG.MYSQL_DATABAS)
    return(db)

def update_user(token, days):
    '''this function update user expired time on database'''
    
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'UPDATE users SET days = "{days}" where token = "{token}";'
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

def update_user_registration(Token):
    '''this function update user registration status on database'''
    
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'UPDATE users SET verified = "1" where token = "{Token}";'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def write_user_to_database(username, password, phone, email, days, token, verified):
    '''this function create user on database'''
    
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'INSERT INTO users (user, password, phone, email, days, token, verified, Device, OS) VALUES ("{username}", "{password}", "{phone}", "{email}", "{days}", "{token}", "{verified}", NULL, NULL);'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def write_user_from_seller_to_database(username, password, Token_seller, token):
    '''this function create user that seller sells on database'''
    
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'INSERT INTO users (user, password, phone, email, days, token, verified, Device, OS) VALUES ("{username}", "{password}", "{Token_seller}", "{Token_seller}", "30", "{token}", "1", NULL, NULL);'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def write_txid_to_database(txid, days):
    '''this function write verified tx-ids on database'''

    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'INSERT INTO txids (txid, days, time) VALUES ("{txid}", "{days}", now());'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def write_date_to_database(date):
    '''this function write dates that expiration.py run on database'''
    
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'INSERT INTO dates (date) VALUES ("{date}");'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def read_dates_from_database():
    '''this function return all working dates that expiration.py run on database'''

    db = connect_to_database()
    cur = db.cursor()
    qury = f'SELECT * FROM dates;'
    cur.execute(qury)
    db.close()
    return cur.fetchall()

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

def read_users_for_seller_from_database(Token_seller):
    '''this function return all users information that one seller sells'''

    db = connect_to_database()
    cur = db.cursor()
    qury = f"SELECT * FROM users WHERE phone = '{Token_seller}' AND email = '{Token_seller}';"
    cur.execute(qury)
    db.close()
    return cur.fetchall()

def delete_user(token,token_seller):

    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'DELETE FROM users WHERE phone = "{token_seller}" AND token = "{token}";'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True