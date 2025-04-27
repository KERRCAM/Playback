# LIBRARY IMPORTS
import mysql.connector

# LOCAL IMPORTS


# ----------------------------------------------------------------------------------------------- #

class DatabaseConnection:

# ----------------------------------------------------------------------------------------------- #

    def __init__(self):
        """Initialize the database connection."""
        self.connection = None

    # ------------------------------------------------------------------------------------------- #

    def connection_database(self):
        """Connect to the MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Uchku2003!",
                database="Playback"
            )
            print("Database connection established.")
            return self.connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise

    # ------------------------------------------------------------------------------------------- #

    def test_connection(self):
        """Test the database connection."""
        try:
            if not self.connection:
                print("No connection to the database.")
                return

            cursor = self.connection.cursor()
            cursor.execute("SELECT DATABASE();")
            result = cursor.fetchone()
            print(f"Connected to database: {result[0]}")
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # ------------------------------------------------------------------------------------------- #

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Connection closed.")

    # ------------------------------------------------------------------------------------------- #

    def create_tables(self):
        """Create tables in the database."""
        try:
            if not self.connection:
                raise ValueError("No database connection. Call connection_database() first.")

            cursor = self.connection.cursor()

            # Create Songs table
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
            """)

            # Create Albums table
            cursor.execute("""
                CREATE TABLE Albums (
                    albumID INT NOT NULL AUTO_INCREMENT,
                    album VARCHAR(400),
                    username VARCHAR(20),
                    timeListened INT,
                    numberOfStreams INT,
                    PRIMARY KEY (albumID, username)
                );
            """)

            # Create Artists table
            cursor.execute("""
                CREATE TABLE Artists (
                    artistID INT NOT NULL AUTO_INCREMENT,
                    artist VARCHAR(400),
                    username VARCHAR(20),
                    timeListened INT,
                    numberOfStreams INT,
                    PRIMARY KEY (artistID, username)
                );
            """)

            # Create Episodes table
            cursor.execute("""
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
            """)

            # Create Users table
            cursor.execute("""            
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
            """)
            
            # Create Timestamps table
            cursor.execute("""
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
            """)

            # Create Countries table
            cursor.execute("""
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
            """)
            self.connection.commit()
            print("Tables created successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise
        finally:
            if cursor:
                cursor.close()

# ----------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    db = DatabaseConnection()
    db.connection_database()
    db.test_connection()
    db.create_tables()
    db.close()
