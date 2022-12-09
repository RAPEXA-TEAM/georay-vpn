#!/usr/bin/env

# Flask

SECRET_KEY = "secret!"

# MySQL config

MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "selleruser"
MYSQL_PASS = "sellerpass"
MYSQL_DATABAS = "sells"

# CREATE DATABASE sells;
# CREATE USER 'selleruser'@'localhost' IDENTIFIED BY 'sellerpass';
# GRANT ALL PRIVILEGES ON sells.* TO 'selleruser'@'localhost';
# USE sells;
# CREATE TABLE users (user VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, phone VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, days VARCHAR(255) NOT NULL, token VARCHAR(255) NOT NULL, PRIMARY KEY (token), UNIQUE (token));