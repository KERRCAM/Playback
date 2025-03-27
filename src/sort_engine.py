
from collections import Counter, defaultdict
from datetime import datetime

def sort_entries(data, sort_by):
    if sort_by == "most_played":
        count = Counter([entry.get("master_metadata_track_name") for entry in data])
        return count.most_common(100)

    elif sort_by == "total_listening_time":
        song_time = defaultdict(int)
        for entry in data:
            song = entry.get("master_metadata_track_name")
            song_time[song] += entry.get("ms_played", 0)
        return sorted(song_time.items(), key=lambda x: x[1], reverse=True)

    elif sort_by == "most_played_artist":
        count = Counter([entry.get("master_metadata_album_artist_name") for entry in data])
        return count.most_common()

    elif sort_by == "most_skipped":
        count = Counter()
        for entry in data:
            if entry.get("reason_end") == "forward_button":
                count[entry.get("master_metadata_track_name")] += 1
        return count.most_common()

    elif sort_by == "time_of_day":
        time_slots = defaultdict(int)
        for entry in data:
            hour = datetime.strptime(entry['ts'], "%Y-%m-%dT%H:%M:%SZ").hour
            time_slots[hour] += 1
        return sorted(time_slots.items())

    elif sort_by == "first_song_of_year":
        years = {}
        for entry in sorted(data, key=lambda x: x['ts']):
            year = datetime.strptime(entry['ts'], "%Y-%m-%dT%H:%M:%SZ").year
            if year not in years:
                years[year] = entry.get("master_metadata_track_name")
        return years

    elif sort_by == "top_artist_by_year":
        yearly_artists = defaultdict(list)
        for entry in data:
            year = datetime.strptime(entry['ts'], "%Y-%m-%dT%H:%M:%SZ").year
            artist = entry.get("master_metadata_album_artist_name")
            yearly_artists[year].append(artist)
        top_artists = {year: Counter(artists).most_common(1)[0] for year, artists in yearly_artists.items()}
        return top_artists

    elif sort_by == "listening_by_country":
        country_time = defaultdict(int)
        total_time = 0
        for entry in data:
            country = entry.get("conn_country")
            time = entry.get("ms_played", 0)
            total_time += time
            country_time[country] += time
        percentages = {k: (v / total_time) * 100 for k, v in country_time.items()}
        return percentages

    elif sort_by == "most_common_end_reason":
        reason_counts = Counter([entry.get("reason_end") for entry in data])
        return reason_counts.most_common()

    else:
        raise ValueError("Unsupported sort_by parameter")
