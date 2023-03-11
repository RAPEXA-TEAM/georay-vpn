CREATE TABLE users
(
    user     VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone    VARCHAR(255) NOT NULL,
    email    VARCHAR(255) NOT NULL,
    days     VARCHAR(255) NOT NULL,
    token    VARCHAR(255) NOT NULL,
    verified VARCHAR(10)  NOT NULL,
    PRIMARY KEY (token),
    UNIQUE (token)
);


CREATE TABLE adWatchs
(
    date VARCHAR(255) NOT NULL,
    UNIQUE (date)
);

CREATE TABLE txids
(
    txid VARCHAR(255) NOT NULL,
    days VARCHAR(255) NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (txid)
);