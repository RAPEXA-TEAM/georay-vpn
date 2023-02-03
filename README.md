# georay-vpn

Pro v2ray vpn with user management and resseler management

## Todo

- [ ] code front of add sell from seller panel
- [ ] code front of edit sell from seller panel
- [ ] document all code and write new documentation for apis for other developers

- [ ] git pull latest project on server
- [ ] config domain for server
- [ ] config Mysql
- [ ] config site to run always on background (supervisor)

## Mysql

1. CREATE DATABASE sells; USE sells;
2. CREATE USER 'selleruser'@'localhost' IDENTIFIED BY 'sellerpass';
3. GRANT ALL PRIVILEGES ON sells.* TO 'selleruser'@'localhost';
4. DROP TABLE users;
5. CREATE TABLE users (user VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, phone VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, days VARCHAR(255) NOT NULL, token VARCHAR(255) NOT NULL, verified VARCHAR(10) NOT NULL, PRIMARY KEY (token), UNIQUE (token));
6. DROP TABLE dates;
7. CREATE TABLE dates (date VARCHAR(255) NOT NULL, UNIQUE (date));
8. DROP TABLE txids;
9. CREATE TABLE txids (txid VARCHAR(255) NOT NULL, days VARCHAR(255) NOT NULL, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,UNIQUE (txid));