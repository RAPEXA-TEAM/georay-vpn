# georay-vpn
v2ray vpn

## Todo

[+] git pull latest project on rapexa.ir server
[+] buying domain for site and connect to rapexa.ir:5550
[ ] run v2ray on iran and thefarameta.com site
[ ] run openconnect on iran and thefarameta.com site
[ ] v2ray ui on server for creating accounts
[ ] config rapexa.ir for an other vpn selling site
[ ] config Mysql
[ ] config site to run always on background (supervisor and port forwarding on 5550)
[ ] config Expiration.py to run daily once (https://www.geeksforgeeks.org/scheduling-python-scripts-on-linux/)
[ ] buying iran vps for v2ray vpn and run boilshit site

## Mysql 

1. CREATE DATABASE sells;
2. CREATE USER 'selleruser'@'localhost' IDENTIFIED BY 'sellerpass';
3. GRANT ALL PRIVILEGES ON sells.* TO 'selleruser'@'localhost';
4. CREATE TABLE users (user VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, phone VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, days VARCHAR(255) NOT NULL, token VARCHAR(255) NOT NULL, PRIMARY KEY (token), UNIQUE (token));
5. DROP TABLE dates;
6. CREATE TABLE dates (date VARCHAR(255) NOT NULL, UNIQUE (date));
7. DROP TABLE txids;
8. CREATE TABLE txids (txid VARCHAR(255) NOT NULL, days VARCHAR(255) NOT NULL, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,UNIQUE (txid));