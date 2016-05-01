# User table
CREATE TABLE User(
	username VARCHAR(20) PRIMARY KEY,
	firstname VARCHAR(20),
	lastname VARCHAR(20),
	password VARCHAR(256),
	email VARCHAR(40)
);

# Friends table 
CREATE TABLE Friends(
	friendid INTEGER PRIMARY KEY AUTO_INCREMENT,
	username VARCHAR(20),
	name VARCHAR(30),
	picture_url VARCHAR(40),
	access ENUM('always allow', 'ask for approval', 'timed', 'block') DEFAULT 'ask for approval',
	time INTEGER DEFAULT NULL,
	FOREIGN KEY(username) REFERENCES User(username)
);

CREATE TABLE Picture(
	username VARCHAR(20) PRIMARY KEY,
	current_picture VARCHAR(50),
	FOREIGN KEY(username) REFERENCES User(username)
);