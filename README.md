# georay-vpn

Pro v2ray vpn with user management and resseler management

## Mysql

1. CREATE DATABASE sells; USE sells;
2. CREATE USER 'selleruserr'@'localhost' IDENTIFIED BY 'Sellerpass1!';
3. GRANT ALL PRIVILEGES ON sells.* TO 'selleruserr'@'localhost';
4. DROP TABLE users;
5. CREATE TABLE users (user VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, phone VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, token VARCHAR(255) NOT NULL, verified VARCHAR(10) NOT NULL, Device VARCHAR(255), OS VARCHAR(255), CreatedDate VARCHAR(255) NOT NULL, ExpiredDate varchar(255) NOT NULL, FreeTimeExpired VARCHAR(255) NOT NULL, usagee varchar(255), PRIMARY KEY (token), UNIQUE (token));
6. DROP TABLE sellers;
7. CREATE TABLE sellers (selleruser VARCHAR(255) NOT NULL, sellerpassword VARCHAR(255) NOT NULL, sellertoken VARCHAR(255) NOT NULL, CreatedDate VARCHAR(255) NOT NULL, Paidusers VARCHAR(255) NOT NULL, Sellusers VARCHAR(255) NOT NULL, Reseller VARCHAR(255), PRIMARY KEY (sellertoken), UNIQUE (sellertoken));
8. DROP TABLE txids;
9. CREATE TABLE txids (txid VARCHAR(255) NOT NULL, days VARCHAR(255) NOT NULL, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,UNIQUE (txid));
