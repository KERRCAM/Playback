-- may be an issue, as would need some way to create the database instance on a users local machine

create database playback;

use playback;



-- All table creations

CREATE TABLE Songs (
    songURI VARCHAR(37),
    username VARCHAR(20),
    songName VARCHAR(30),
    artist VARCHAR(30),
    album VARCHAR(30),
    timeListened INT,
    numberOfStreams INT,
    start_trackdone INT,
    start_fwdbtn INT,
    start_backbtn INT,
    start_remote INT,
    start_clickrow INT,
    end_trackdone INT,
    end_fwdbtn INT,
    end_backbtn INT,
    end_remote INT,
    end_endplay INT,
    PRIMARY KEY (songURI, username)
);

CREATE TABLE Albums (
    albumID INT NOT NULL AUTO_INCREMENT,
    album VARCHAR(30),
    username VARCHAR(20),
    timeListened INT,
    numberOfStreams INT,
    PRIMARY KEY (album, username)
);

CREATE TABLE Artists (
    artistID INT NOT NULL AUTO_INCREMENT,
    artist VARCHAR(30),
    username VARCHAR(20),
    timeListened INT,
    numberOfStreams INT,
    PRIMARY KEY (artist, username)
);

CREATE TABLE Episodes (
    episodeURI VARCHAR(37),
    username VARCHAR(20),
    episodeName VARCHAR(30),
    showName VARCHAR(30),
    timeListened INT,
    numberOfStreams INT,
    reasonStart INT,
    reasonEnd INT,
    countriesListened VARCHAR(30),
    PRIMARY KEY (episodeURI, username)
);

CREATE TABLE Shows (
    showID INT NOT NULL AUTO_INCREMENT,
    showName VARCHAR(30),
    username VARCHAR(20),
    timeListened INT,
    numberOfStreams INT,
    PRIMARY KEY (showName, username)
);

CREATE TABLE Users (
    username VARCHAR(20) PRIMARY KEY,
    timeListened INT,
    numberOfStreams INT,
    morning INT,
    afternoon INT,
    evening INT,
    night INT
);

CREATE TABLE Timestamps (
    username VARCHAR(20),
    songURI VARCHAR(37),
    albumID INT,
    artistID INT,
    timestamp DATETIME,
    PRIMARY KEY (username, songURI)
);

CREATE TABLE Countries (
    username VARCHAR (20),
    songURI VARCHAR (37),
    albumID INT,
    artistID INT,
    showID INT,
    country VARCHAR (20),
    streams INT,
    minutesListened INT
);

delete from albums;
