DROP TABLE IF EXISTS cif, comments, product, "productID(1)-transactions", "productID(2)-transactions", scammer ;
 
CREATE TABLE "cif" (
	"id"	INTEGER UNIQUE,
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT,
	"firstname"	TEXT,
	"lastname"	TEXT,
	"gender"	TEXT,
	"dob"	TEXT,
	"ic"	INTEGER UNIQUE,
	"phone"	INTEGER,
	"email"	TEXT UNIQUE,
	"address1"	NUMERIC,
	"address2"	TEXT,
	"postcode"	TEXT,
	"area"	TEXT,
	"state"	TEXT,
	"country"	TEXT,
	"productID"	INTEGER,
	"productNAME"	TEXT,
	"accountID"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "comments" (
	"id"	INTEGER,
	"comment"	TEXT NOT NULL,
	"scammer_id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"created_at"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY("scammer_id") REFERENCES "scammer"("scammerID"),
	FOREIGN KEY("user_id") REFERENCES "cif"("username"),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "product" (
	"productID"	INTEGER UNIQUE,
	"productNAME"	TEXT NOT NULL,
	PRIMARY KEY("productID" AUTOINCREMENT)
);

CREATE TABLE "productID(1)-transactions" (
	"accountID"	TEXT,
	"date"	TEXT,
	"transactionTYPE"	TEXT,
	"description"	TEXT,
	"Amount"	REAL,
	"accountBAL"	REAL,
	"category"	TEXT,
	"status"	TEXT
);

CREATE TABLE "productID(2)-transactions" (
	"accountID"	TEXT,
	"transactionDATE"	TEXT,
	"transactionTYPE"	TEXT,
	"description"	TEXT,
	"amount"	REAL
);

CREATE TABLE "scammer" (
	"scammerID"	INTEGER NOT NULL,
	"scammerName"	TEXT,
	"contact"	TEXT,
	"platform"	TEXT,
	"reportedDate"	TEXT,
	"recordedDate"	TEXT,
	"bankAccount"	TEXT,
	"bankName"	TEXT,
	"bankAccountName"	TEXT,
	"sourceReport1"	TEXT,
	"sourceReport2"	TEXT,
	"sourceReport3"	TEXT,
	"tiktokID"	TEXT,
	"facebookID"	TEXT,
	"twitterID"	TEXT,
	"instagramID"	TEXT,
	"telegramID"	TEXT,
	"reporterID"	INTEGER,
	PRIMARY KEY("scammerID" AUTOINCREMENT)
);

--UPDATE 'productID(1)-transactions'
--SET status = (SELECT COALESCE(status, 'Completed')
  --                 FROM 'productID(1)-transactions'
    --               WHERE status IS NULL);
