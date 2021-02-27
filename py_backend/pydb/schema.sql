-- database table schema
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS club;

CREATE TABLE user (
	email VARCHAR 50 PRIMARY KEY,
	password VARCHAR 50 NOT NULL,
	fname VARCHAR 50 NOT NULL,
	lname VARCHAR 50 NOT NULL
);

CREATE TABLE admin (
	admin_email VARCHAR(50),
	FOREIGN KEY (admin_email) REFERENCES user (email)
);


-- intro: introduction/description about what the club is about
-- details: club meeting times and recruitment details
CREATE TABLE club (
	name VARCHAR(50) PRIMARY KEY,
	intro VARCHAR(280) NOT NULL,
	details VARCHAR(280) NOT NULL
);