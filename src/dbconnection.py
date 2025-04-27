
# Library imports
import mysql.connector

# Local imports

class DatabaseConnection:
    def __init__(self):
        """Initialize the database connection."""
            # Connect to the database
        connection = self.connection_database()
        self.connection = connection
        # Create tables
        self.create_tables()

    def connection_database(self):
        """Connect to the MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",       
                user="root",            
                password="Uchku2003!",    
                database="playback"     
            )
            print("Database connection established.")
            return self.connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise

    def create_tables(self):
        """Create tables in the database."""
        try:
            if not self.connection:
                raise ValueError("No database connection. Call connection_database() first.")

            cursor = self.connection.cursor()

            """Create tables in the database."""

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Songs (
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
                    PRIMARY KEY (songURI, username)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Albums (
                        albumID INT NOT NULL AUTO_INCREMENT,
                        album VARCHAR(400),
                        username VARCHAR(20),
                        timeListened INT,
                        numberOfStreams INT,
                        PRIMARY KEY (albumID, username),
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Artists (
                    artistID INT NOT NULL AUTO_INCREMENT,
                    artist VARCHAR(400),
                    username VARCHAR(20),
                    numberOfStreams INT,
                    PRIMARY KEY (artistID, username)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Episodes (
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
                    PRIMARY KEY (episodeURI, username)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Shows (
                    showID INT NOT NULL AUTO_INCREMENT,
                    showName VARCHAR(400),
                    username VARCHAR(20),
                    timeListened INT,
                    numberOfStreams INT,
                    PRIMARY KEY (showID, username)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users  (
                    username VARCHAR(20) PRIMARY KEY,
                    password VARCHAR(20),
                    timeListened INT,
                    numberOfStreams INT,
                    morning INT,
                    afternoon INT,
                    evening INT,
                    night INT
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Timestamps(
                    tsID INT NOT NULL AUTO_INCREMENT,
                    username VARCHAR(20),
                    songURI VARCHAR(50),
                    episodeURI VARCHAR (50),
                    album varchar(400),
                    artist varchar(400),
                    timestamp DATETIME,
                    PRIMARY KEY (tsID, username, timestamp),
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Countries (
                    username VARCHAR (20),
                    songURI VARCHAR (50),
                    episodeURI varchar(50),
                    album varchar(400),
                    artist varchar(400),
                    showName varchar(400),
                    countryCode VARCHAR (5),
                    numberOfStreams INT,
                    timeListened INT,
                    PRIMARY KEY(username, countryCode),
                );
            """)
            self.connection.commit()
            print("Tables created successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise
        finally:
            if cursor:
                cursor.close()

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Connection closed.")