# not exactly my original code

import json
import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ulaaka_1223",
    database="playback"
)
cursor = conn.cursor()

def truncate_string(value, max_length):
    if value is None:
        return None
    return value[:max_length] if len(value) > max_length else value

def convert_to_mysql_datetime(iso_datetime):
    try:
        dt = datetime.strptime(iso_datetime, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return None

def get_reason_flags(reason_value):
    """Convert reason string to multiple binary flags"""
    reason = str(reason_value).lower() if reason_value else ""
    return {
        'trackdone': 1 if reason == 'trackdone' else 0,
        'fwdbtn': 1 if reason == 'fwdbtn' else 0,
        'backbtn': 1 if reason == 'backbtn' else 0,
        'remote': 1 if reason == 'remote' else 0,
        'clickrow': 1 if reason == 'clickrow' else 0,
        'endplay': 1 if reason == 'endplay' else 0
    }

def get_time_period(timestamp_str):
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
        hour = dt.hour
        if 6 <= hour < 12: return 'morning'
        elif 12 <= hour < 18: return 'afternoon'
        elif 18 <= hour < 24: return 'evening'
        else: return 'night'
    except:
        return None

user_query = """
INSERT INTO Users (username, timeListened, numberOfStreams, morning, afternoon, evening, night)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE 
    timeListened = timeListened + VALUES(timeListened), 
    numberOfStreams = numberOfStreams + 1,
    morning = morning + VALUES(morning),
    afternoon = afternoon + VALUES(afternoon),
    evening = evening + VALUES(evening),
    night = night + VALUES(night);
"""

with open('dataFiles/Streaming_History_Audio_2021-2025.json') as f:
    data = json.load(f)

for item in data:
    username = "default_user"
    iso_timestamp = item.get("ts")
    mysql_timestamp = convert_to_mysql_datetime(iso_timestamp)
    time_period = get_time_period(iso_timestamp)
    
    ms_played = item.get("ms_played", 0)
    minutes_played = ms_played / 60000
    
    is_song = item.get("spotify_track_uri") is not None
    is_episode = item.get("spotify_episode_uri") is not None
    
    morning = 1 if time_period == 'morning' else 0
    afternoon = 1 if time_period == 'afternoon' else 0
    evening = 1 if time_period == 'evening' else 0
    night = 1 if time_period == 'night' else 0
    
    user_values = (
        username,
        minutes_played,
        1,
        morning,
        afternoon,
        evening,
        night
    )
    
    if is_song:
        start_reasons = get_reason_flags(item.get("reason_start"))
        end_reasons = get_reason_flags(item.get("reason_end"))
        
        song_query = """
        INSERT INTO Songs (songURI, username, songName, artist, album, timeListened, numberOfStreams, 
                          start_trackdone, start_fwdbtn, start_backbtn, start_remote, start_clickrow, 
                          end_trackdone, end_fwdbtn, end_backbtn, end_remote, end_endplay, countriesListened)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            timeListened = timeListened + VALUES(timeListened), 
            numberOfStreams = numberOfStreams + 1,
            start_trackdone = start_trackdone + VALUES(start_trackdone),
            start_fwdbtn = start_fwdbtn + VALUES(start_fwdbtn),
            start_backbtn = start_backbtn + VALUES(start_backbtn),
            start_remote = start_remote + VALUES(start_remote),
            start_clickrow = start_clickrow + VALUES(start_clickrow),
            end_trackdone = end_trackdone + VALUES(end_trackdone),
            end_fwdbtn = end_fwdbtn + VALUES(end_fwdbtn),
            end_backbtn = end_backbtn + VALUES(end_backbtn),
            end_remote = end_remote + VALUES(end_remote),
            end_endplay = end_endplay + VALUES(end_endplay);
        """
        
        song_values = (
            item.get("spotify_track_uri"),
            username,
            truncate_string(item.get("master_metadata_track_name"), 255),
            truncate_string(item.get("master_metadata_album_artist_name"), 255),
            truncate_string(item.get("master_metadata_album_album_name"), 255),
            minutes_played,
            1,
            start_reasons['trackdone'],
            start_reasons['fwdbtn'],
            start_reasons['backbtn'],
            start_reasons['remote'],
            start_reasons['clickrow'],
            end_reasons['trackdone'],
            end_reasons['fwdbtn'],
            end_reasons['backbtn'],
            end_reasons['remote'],
            end_reasons['endplay'],
            truncate_string(item.get("conn_country"), 255)
        )
        
        cursor.execute(song_query, song_values)
        
        album_query = """
        INSERT INTO Albums (album, username, timeListened, numberOfStreams)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            timeListened = timeListened + VALUES(timeListened), 
            numberOfStreams = numberOfStreams + 1;
        """
        
        cursor.execute(album_query, (
            truncate_string(item.get("master_metadata_album_album_name"), 255),
            username,
            minutes_played,
            1
        ))
        
        artist_query = """
        INSERT INTO Artists (artist, username, timeListened, numberOfStreams)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            timeListened = timeListened + VALUES(timeListened), 
            numberOfStreams = numberOfStreams + 1;
        """
        
        cursor.execute(artist_query, (
            truncate_string(item.get("master_metadata_album_artist_name"), 255),
            username,
            minutes_played,
            1
        ))
        
        cursor.execute(user_query, user_values)
        
        timestamp_query = """
        INSERT INTO Timestamps (username, songURI, timestamp)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            timestamp = VALUES(timestamp)
        """
        
        cursor.execute(timestamp_query, (
            username,
            item.get("spotify_track_uri"),
            mysql_timestamp
        ))
        
        country_query = """
        INSERT INTO Countries (username, songURI, country, streams, minutesListened)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            streams = streams + 1,
            minutesListened = minutesListened + VALUES(minutesListened);
        """
        
        cursor.execute(country_query, (
            username,
            item.get("spotify_track_uri"),
            truncate_string(item.get("conn_country"), 255),
            1,
            minutes_played
        ))
        
    elif is_episode:
        start_reasons = get_reason_flags(item.get("reason_start"))
        end_reasons = get_reason_flags(item.get("reason_end"))
        
        episode_query = """
        INSERT INTO Episodes (episodeURI, username, episodeName, showName, timeListened, 
                            numberOfStreams, start_trackdone, start_fwdbtn, start_backbtn, 
                            start_remote, start_clickrow, end_trackdone, end_fwdbtn, 
                            end_backbtn, end_remote, end_endplay, countriesListened)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            timeListened = timeListened + VALUES(timeListened),
            numberOfStreams = numberOfStreams + 1;
        """
        
        episode_values = (
            truncate_string(item.get("spotify_episode_uri"), 255),
            username,
            truncate_string(item.get("episode_name"), 255),
            truncate_string(item.get("episode_show_name"), 255),
            minutes_played,
            1,
            start_reasons['trackdone'],
            start_reasons['fwdbtn'],
            start_reasons['backbtn'],
            start_reasons['remote'],
            start_reasons['clickrow'],
            end_reasons['trackdone'],
            end_reasons['fwdbtn'],
            end_reasons['backbtn'],
            end_reasons['remote'],
            end_reasons['endplay'],
            truncate_string(item.get("conn_country"), 255)
        )
        
        cursor.execute(episode_query, episode_values)
        
        show_query = """
        INSERT INTO Shows (showName, username, timeListened, numberOfStreams)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            timeListened = timeListened + VALUES(timeListened), 
            numberOfStreams = numberOfStreams + 1;
        """
        
        cursor.execute(show_query, (
            truncate_string(item.get("episode_show_name"), 255),
            username,
            minutes_played,
            1
        ))
        
        cursor.execute(user_query, user_values)

    if len(data) > 100 and (data.index(item) + 1) % 100 == 0:
        conn.commit()

conn.commit()
cursor.close()
conn.close()

print("Data insertion completed successfully!")