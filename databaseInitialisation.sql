-- may be an issue, as would need some way to create the database instance on a users local machine

drop database playback;
drop table Episodes;
drop table Songs;

create database playback;

use playback;



-- All table creations

CREATE TABLE Songs (
    songURI VARCHAR(37),
    username VARCHAR(20),
    songName VARCHAR(200),
    artist VARCHAR(200),
    album VARCHAR(200),
    timeListened INT,
    numberOfStreams INT,
    start_trackdone INT,
    start_fwdbtn INT,
    start_backbtn INT,
    start_remote INT,
    start_clickrow INT,
    start_trackerror INT,
    start_playbtn INT,
    start_appload INT,
    end_trackdone INT,
    end_fwdbtn INT,
    end_backbtn INT,
    end_remote INT,
    end_endplay INT,
    end_logout INT,
    end_unexpected_exit INT,
    end_unexpected_exit_while_paused INT,
    PRIMARY KEY (songURI, username)
);

CREATE TABLE Albums (
    albumID INT NOT NULL AUTO_INCREMENT,
    album VARCHAR(200),
    username VARCHAR(20),
    timeListened INT,
    numberOfStreams INT,
    PRIMARY KEY (albumID, username)
);

CREATE TABLE Artists (
    artistID INT NOT NULL AUTO_INCREMENT,
    artist VARCHAR(200),
    username VARCHAR(20),
    timeListened INT,
    numberOfStreams INT,
    PRIMARY KEY (artistID, username)
);

CREATE TABLE Episodes (
    episodeURI VARCHAR(37),
    username VARCHAR(20),
    episodeName VARCHAR(200),
    showName VARCHAR(200),
    timeListened INT,
    numberOfStreams INT,
    start_trackdone INT,
    start_fwdbtn INT,
    start_backbtn INT,
    start_remote INT,
    start_clickrow INT,
    start_trackerror INT,
    start_playbtn INT,
    start_appload INT,
    end_trackdone INT,
    end_fwdbtn INT,
    end_backbtn INT,
    end_remote INT,
    end_endplay INT,
    end_logout INT,
    end_unexpected_exit INT,
    end_unexpected_exit_while_paused INT,
    PRIMARY KEY (episodeURI, username)
);

CREATE TABLE Shows (
    showID INT NOT NULL AUTO_INCREMENT,
    showName VARCHAR(200),
    username VARCHAR(20),
    timeListened INT,
    numberOfStreams INT,
    PRIMARY KEY (showID, username)
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
	tsID INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(20),
    songURI VARCHAR(37),
    episodeURI VARCHAR (37),
    albumID INT,
    artistID INT,
    timestamp DATETIME,
    PRIMARY KEY (tsID, username, timestamp)
);

CREATE TABLE Countries (
    username VARCHAR (20),
    songURI VARCHAR (37),
    episodeURI varchar(37),
    albumID INT,
    artistID INT,
    showID INT,
    countryCode VARCHAR (5),
    numberOfStreams INT,
    timeListened INT
);



DELETE FROM Songs;
DELETE FROM Albums;
DELETE FROM Artists;
DELETE FROM Episodes;
DELETE FROM Shows;
DELETE FROM Timestamps;
DELETE FROM Countries;
DELETE FROM Users;
