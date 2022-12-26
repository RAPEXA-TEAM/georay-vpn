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

def update_user(token, days):
    '''this function update user expired time on database'''
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'UPDATE users SET days = "{days}" where token = "{token}";'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def write_user_to_database(username, password, phone, email, days, token):
    '''this function create user on database'''
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'INSERT INTO users (user, password, phone, email, days, token) VALUES ("{username}", "{password}", "{phone}", "{email}", "{days}", "{token}");'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def write_txid_to_database(txid, days):
    '''this function write txid on database'''
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'INSERT INTO txids (txid, days, time) VALUES ("{txid}", "{days}", now());'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def write_date_to_database(date):
    '''this function create user on database'''
    db = connect_to_database()
    cur = db.cursor()                       
    qury = f'INSERT INTO dates (date) VALUES ("{date}");'
    cur.execute(qury)
    db.commit()
    db.close()    
    return True

def read_dates_from_database():
    '''this function return all working dates'''
    db = connect_to_database()
    cur = db.cursor()
    qury = f'SELECT * FROM dates;'
    cur.execute(qury)
    db.close()
    return cur.fetchall()

def read_txids_from_database():
    '''this function return all working dates'''
    db = connect_to_database()
    cur = db.cursor()
    qury = f'SELECT * FROM txids;'
    cur.execute(qury)
    db.close()
    return cur.fetchall()

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
    db = connect_to_database()
    print("[+] Start creating Users table...")
    qury = "CREATE TABLE users (user VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, phone VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, days VARCHAR(255) NOT NULL, token VARCHAR(255) NOT NULL, PRIMARY KEY (token), UNIQUE (token));"
    cur.execute(qury)
    db.commit()
    db.close()
    print("[+] Create Users table done.")
    db = connect_to_database()
    print("[+] Start creating date table...")
    qury = "CREATE TABLE dates (date VARCHAR(255) NOT NULL, UNIQUE (date));"
    cur.execute(qury)
    db.commit()
    db.close()
    print("[+] Create date table done.")
    return True

try:
    if sys.argv[1] == "execute":
        if Make_Database():
            print("[+] Done!")
        else :
            print("[-] Error...")
except:
    pass