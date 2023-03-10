# georay-vpn

Pro v2ray vpn with user management and resseler management

## Todo

## Mysql

1. CREATE DATABASE sells; USE sells;
2. CREATE USER 'selleruserr'@'localhost' IDENTIFIED BY 'Sellerpass1!';
3. GRANT ALL PRIVILEGES ON sells.* TO 'selleruserr'@'localhost';
4. DROP TABLE users;
5. CREATE TABLE users (user VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, phone VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, days VARCHAR(255) NOT NULL, token VARCHAR(255) NOT NULL, verified VARCHAR(10) NOT NULL, PRIMARY KEY (token), UNIQUE (token));
6. DROP TABLE dates;
7. CREATE TABLE dates (date VARCHAR(255) NOT NULL, UNIQUE (date));
8. DROP TABLE txids;
9. CREATE TABLE txids (txid VARCHAR(255) NOT NULL, days VARCHAR(255) NOT NULL, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,UNIQUE (txid));

## Changes

1. ALTER TABLE users ADD Device varchar(255);
2. ALTER TABLE users ADD OS varchar(255);

## Sellers

mohsen,javaheri1989,59
amirferdows,0850200628,12
mojtabaferdows,7936122,12
erfan1381,1296354870,2
amirtala,Amir81@#,9
sase315,sas2043,4
avatar2003d,21101381mrdMRD,7
sajjad.asgharnia,9576842310sa,1
hosseinkhojani,#khojani,0
uploadpic01@gmail.com,20082008@#,0
1983masoud@gmail.com,20082008@#,0
rasoolkarimi635@gmail.com,20082008@#,3
Mehdisoleimani7675@gmail.com,20082008@#,0
rezaabbasabad@gmail.com,20082008@#,10
habibbabakhan7749@gmail.com,20082008@#,0
Mohsen1982ziaei@gmail.com,20082008@#,0
Alirezahaghighat@gmail.com,20082008@#,10
clupparsa,Mm123456a!,0
alireza1368,6518alireza,1
brooz,0850056314,0