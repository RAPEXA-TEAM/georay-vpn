#!/usr/bin/env

# Flask Secret key

SECRET_KEY = "secret!"
HOST = "0.0.0.0"

# MySQL Configs

MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "selleruserr"
MYSQL_PASS = "Sellerpass1!"
MYSQL_DATABAS = "sells"

# Smtp Email Configs

SMTP_PORT = 587
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "georayvpn@gmail.com"
PASSWORD = "ikmajfetagfvxbfr"

# Web3 Configs

NODE_URL = "https://ethereum.publicnode.com"

# VPN Prices

PRICE_ONE_MONTH = 50000
PRICE_TWO_MONTH = 100000
PRICE_TRE_MONTH = 150000

# Update version

VERSION = "0.2.0"
VERSION_TYPE = "0" # 0 : False, 1 : True
DOWNLOAD_LINK = ""

# Config Production

PATH_EXPIRATION = '/var/www/vpn/site/Expiration.py'
PATH_SELLERS = '/var/www/vpn/site/Sellers.csv'
PATH_SERVERS = '/var/www/vpn/site/Servers.csv'
RUNNING_PORT = 80
PRODUCTION_MODE = False

# Config Development

PATH_EXPIRATION_DEV = 'Expiration.py'
PATH_SELLERS_DEV = 'Sellers.csv'
PATH_SERVERS_DEV = 'Servers.csv'
RUNNING_PORT_DEV = 5550
DEBUG_MODE = True