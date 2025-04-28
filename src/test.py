# Test Script
from queries import Queries

# Initialize the Queries class
queries = Queries()

# Test most_listened method
print("Testing most listened songs:")
# most_listened_result = queries.most_listened(10)
# print(most_listened_result)

# Test most_streamed method
print("Testing most streamed songs:")
most_streamed_result = queries.most_streamed(10)
print(most_streamed_result)

# Test most_played_artists method
print("Testing most played artists:")

# most_played_artists_result = queries.most_played_artists(10)
# print(most_played_artists_result)

# Test top_artist_year method (replace 0 with a valid number of results, e.g., 5)
print("Testing top artist by year:")
# top_artist_year_result = queries.top_artist_year(5)
# print(top_artist_year_result)

# Test first_songs_year_time method
print("Testing first songs played each year:")
# first_songs_year_result = queries.first_songs_year_time()
# print(first_songs_year_result)

# Test total_listening_time_country method
print("Testing total listening time by country:")
# total_listening_time_country_result = queries.total_listening_time_country()
# print(total_listening_time_country_result)
