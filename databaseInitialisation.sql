-- may be an issue, as would need some way to create the database instance on a users local machine



create database playback;

use playback;

-- All table creations

CREATE TABLE Songs (
    songURI VARCHAR(50),
    username VARCHAR(20),
    songName VARCHAR(400),
    artist VARCHAR(400),
    album VARCHAR(400),
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
    start_unknown INT,
    start_switched_to_audio INT,
    start_switched_to_video INT,
    end_trackdone INT,
    end_fwdbtn INT,
    end_backbtn INT,
    end_remote INT,
    end_endplay INT,
    end_logout INT,
    end_unexpected_exit INT,
    end_unexpected_exit_while_paused INT,
    end_trackerror INT,
    end_unknown INT,
    end_switched_to_audio INT,
    end_switched_to_video int,
    PRIMARY KEY (songURI, username)
);

CREATE TABLE Albums (
    albumID INT NOT NULL AUTO_INCREMENT,
    album VARCHAR(400),
    username VARCHAR(20),
    timeListened INT,
    numberOfStreams INT,
    PRIMARY KEY (albumID, username)
);

CREATE TABLE Artists (
    artistID INT NOT NULL AUTO_INCREMENT,
    artist VARCHAR(400),
    username VARCHAR(20),
    timeListened INT,
    numberOfStreams INT,
    PRIMARY KEY (artistID, username)
);

CREATE TABLE Episodes (
    episodeURI VARCHAR(50),
    username VARCHAR(20),
    episodeName VARCHAR(400),
    showName VARCHAR(400),
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
    start_unknown INT,
    start_switched_to_audio INT,
    start_switched_to_video INT,
    end_trackdone INT,
    end_fwdbtn INT,
    end_backbtn INT,
    end_remote INT,
    end_endplay INT,
    end_logout INT,
    end_unexpected_exit INT,
    end_unexpected_exit_while_paused INT,
    end_trackerror INT,
    end_unknown INT,
    end_switched_to_audio INT,
    end_switched_to_video INT,
    PRIMARY KEY (episodeURI, username)
);

CREATE TABLE Shows (
    showID INT NOT NULL AUTO_INCREMENT,
    showName VARCHAR(400),
    username VARCHAR(20),
    timeListened INT,
    numberOfStreams INT,
    PRIMARY KEY (showID, username)
);

CREATE TABLE Users (
    username VARCHAR(20) PRIMARY KEY,
    password VARCHAR(20),
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
    songURI VARCHAR(50),
    episodeURI VARCHAR (50),
    album varchar(400),
    artist varchar(400),
    timestamp DATETIME,
    PRIMARY KEY (tsID, username, timestamp)
);

CREATE TABLE Countries (
    username VARCHAR (20),
    songURI VARCHAR (50),
    episodeURI varchar(50),
    album varchar(400),
    artist varchar(400),
    showName varchar(400),
    countryCode VARCHAR (5),
    numberOfStreams INT,
    timeListened INT,
    PRIMARY KEY(username, countryCode)
);

select * from Users;

commit;

select * from Songs ORDER BY timeListened DESC;

select * from Timestamps;

SELECT * FROM Albums ORDER BY timeListened DESC;

SELECT A.artist, SUM(S.timeListened) AS total_time, COUNT(*) AS total_stream
                    FROM Songs S 
                    JOIN Timestamps T ON S.songURI = T.songURI AND S.username = T.username
                    JOIN Artists A ON S.artist = A.artist AND S.username = A.username
                    WHERE YEAR(T.timestamp) = '2024' and S.artist != 'null' and S.username = 'test'
                    GROUP BY A.artist
                    ORDER BY total_time DESC
                    LIMIT 100;


drop database playback;
drop table Episodes;
drop table Songs;
drop table TimeStamps;
drop table Countries;

DELETE FROM Songs;
DELETE FROM Albums;
DELETE FROM Artists;
DELETE FROM Episodes;
DELETE FROM Shows;
DELETE FROM Timestamps;
DELETE FROM Countries;
DELETE FROM Users;
