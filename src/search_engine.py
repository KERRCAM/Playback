
import datetime

def parse_timestamp(ts):
    return datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")

def is_within_time_range(ts, start, end):
    return start <= ts.time() <= end

def is_binge_session(playback_data, max_gap_minutes=15):
    binge_sessions = []
    current_session = []
    for i, entry in enumerate(sorted(playback_data, key=lambda x: x['ts'])):
        entry_time = parse_timestamp(entry['ts'])
        if not current_session:
            current_session.append((entry, entry_time))
            continue
        last_entry_time = current_session[-1][1]
        gap = (entry_time - last_entry_time).total_seconds() / 60
        if gap <= max_gap_minutes:
            current_session.append((entry, entry_time))
        else:
            session_length = (current_session[-1][1] - current_session[0][1]).total_seconds() / 60
            if session_length >= 120:
                binge_sessions.append([x[0] for x in current_session])
            current_session = [(entry, entry_time)]
    if current_session:
        session_length = (current_session[-1][1] - current_session[0][1]).total_seconds() / 60
        if session_length >= 120:
            binge_sessions.append([x[0] for x in current_session])
    return binge_sessions

def search_entries(data, filters):
    results = []
    for entry in data:
        ts = parse_timestamp(entry['ts'])
        if filters.get("song_title") and filters["song_title"].lower() not in (entry.get("master_metadata_track_name") or "").lower():
            continue
        if filters.get("artist") and filters["artist"].lower() not in (entry.get("master_metadata_album_artist_name") or "").lower():
            continue
        if filters.get("album") and filters["album"].lower() not in (entry.get("master_metadata_album_album_name") or "").lower():
            continue
        if "offline" in filters and entry.get("offline", False) != filters["offline"]:
            continue
        if filters.get("device") and filters["device"].lower() not in (entry.get("device") or "").lower():
            continue
        if "shuffle" in filters and entry.get("shuffle", False) != filters["shuffle"]:
            continue
        if "podcast_only" in filters:
            is_podcast = entry.get("episode_name") is not None
            if is_podcast != filters["podcast_only"]:
                continue
        if "timestamp_range" in filters:
            start, end = filters["timestamp_range"]
            if not (start <= ts <= end):
                continue
        if "time_range" in filters:
            t_start, t_end = filters["time_range"]
            if not is_within_time_range(ts, t_start, t_end):
                continue
        if "day_of_week" in filters:
            if ts.strftime('%A').lower() != filters["day_of_week"].lower():
                continue
        if "genre" in filters and filters["genre"].lower() not in (entry.get("genre", "")).lower():
            continue
        results.append(entry)
    return results
