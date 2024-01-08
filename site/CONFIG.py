#!/usr/bin/env

# PLANS

FREE_DAYS    = 7
MONTHLY_DAYS = 30

# Flask Secret key

SECRET_KEY     = "secret!"
HOST           = "0.0.0.0"
ALTER_USERNAME = "georayadmin@gmail.com"
ALTER_PASSWORD = "georayadminpassword"

# MySQL Configs

MYSQL_HOST    = "127.0.0.1"
MYSQL_USER    = "selleruserr"
MYSQL_PASS    = "Sellerpass1!"
MYSQL_DATABAS = "sells"

# Smtp Email Configs

SMTP_PORT    = 587
SMTP_SERVER  = "smtp.gmail.com"
SENDER_EMAIL = "georayvpn@gmail.com"
PASSWORD     = "ikmajfetagfvxbfr"

# Web3 Configs

NODE_URL = "https://ethereum.publicnode.com"

# VPN Prices

FREE_PLAN_HOURS = 1
PRICE_ONE_MONTH = 50000
PRICE_TWO_MONTH = 100000
PRICE_TRE_MONTH = 150000

# Update version

VERSION       = "0.2.0"
VERSION_TYPE  = "0" # 0 : False, 1 : True
DOWNLOAD_LINK = "http://dv.d4rk4pp.sbs/"

# Config Production
# /var/www/vpn/site/
# PATH_EXPIRATION = '/var/www/vpn/site/Expiration.py'

PATH_SERVERS        = '/var/www/vpn/site/Servers.csv'
PATH_FREE_SERVER    = '/var/www/vpn/site/ServerFree.csv'
PATH_SERVERS_MTN    = "/var/www/vpn/site/ServersMTN.csv"
PATH_SERVERS_MCI    = "/var/www/vpn/site/ServersMCI.csv"
PATH_SERVERS_MKH    = "/var/www/vpn/site/ServersMOKH.csv"
PATH_APK            = "/var/www/vpn/site/georay4.apk"
RUNNING_PORT        = 80
DEBUG_MODE          = False

# LANGUAGES

ENGLISH = "en"
FARSI   = "fa"