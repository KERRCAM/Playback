import json
from datetime import datetime, time

from src.search_engine import search_entries
from src.sort_engine import sort_entries

# Load your JSON streaming data
with open('dataFiles/Streaming_History_Audio_2019-2020_0.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 🔍 Example Search: All Spotify streams by "Drake" on Fridays
search_filters = {
    "artist": "Drake",
    "day_of_week": "Friday"
}
filtered_data = search_entries(data, search_filters)
print(f"Found {len(filtered_data)} Drake songs on Fridays.")

# 🌀 Example Sort: Top 10 most played songs
top_songs = sort_entries(data, "most_played")
print("🎵 Top 10 Songs:")
for i, (song, count) in enumerate(top_songs[:10], start=1):
    print(f"{i}. {song} - {count} plays")

# 🧪 Another Example: Total listening time by country
country_stats = sort_entries(data, "listening_by_country")
print("🌍 Listening Time by Country (%):")
for country, percentage in country_stats.items():
    print(f"{country}: {percentage:.2f}%")
