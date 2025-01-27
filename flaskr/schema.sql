DROP TABLE IF EXISTS user;
 
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    gender TEXT NOT NULL,
    dob TEXT NOT NULL,
    email TEXT NOT NULL,
    address1 TEXT NOT NULL,
    address2 TEXT NOT NULL,
    postcode TEXT NOT NULL,
    area TEXT NOT NULL,
    state TEXT NOT NULL,
    productNAME TEXT NOT NULL,
    productID TEXT NOT NULL,
    productID1_account INTEGER NOT NULL,
    ic INTEGER NOT NULL
);
