#!/usr/bin/env
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
    
def write_user_to_database(username, password, phone, email, days, token):
    '''this function create user on database'''
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'INSERT INTO users (user, password, phone, email, days, token) VALUES ("{username}", "{password}", "{phone}", "{email}", "{days}", "{token}");'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def read_users_from_database():
    '''this function return all users informations'''
    db = connect_to_database()
    cur = db.cursor()
    qury = f'SELECT * FROM users;'
    cur.execute(qury)
    db.close()
    return cur.fetchall()

def Make_Database():
    '''This function make database'''
    print("[+] Connecting to MySQl Server")
    db = connect_to_database()
    print("[+] Connected to MySQL Server")
    cur = db.cursor()                       
    qury = "DROP TABLE IF EXISTS users;"
    cur.execute(qury)
    db.commit()
    db.close()
    qury = "CREATE TABLE users (user VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, phone VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, days VARCHAR(255) NOT NULL, token VARCHAR(255) NOT NULL, PRIMARY KEY (token), UNIQUE (token));"
    cur.execute(qury)
    db.commit()
    db.close()
    print("[+] Create Users table")
    return True

try:
    if sys.argv[1] == "execute":
        if Make_Database():
            print("[+] Done!")
        else :
            print("[-] Error...")
except:
    pass