import pandas as pd
import numpy as np
import json
import requests
from musicAPI import get_artist_tags

# Load environment variables and get access token from Spotify API

# Load the JSON file
with open('StreamingHistory_music_0.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# Convert 'msPlayed' to minutes
df['minutesPlayed'] = df['msPlayed'] / (1000 * 60)

# Add new columns for date, day of the week, month, and hour
df['endTime'] = pd.to_datetime(df['endTime'])
df['date'] = df['endTime'].dt.date
df['day-of-week'] = df['endTime'].dt.day_name()
df['month'] = df['endTime'].dt.month
df['hour'] = df['endTime'].dt.hour


# Create a new Dataframe that holds every song with total minutes played (sort minutes played in descending order)
song_summary = df.groupby(['artistName', 'trackName']).agg({'minutesPlayed': 'sum'}).sort_values('minutesPlayed', ascending=False).reset_index()

# Limit the song summary to the top 100 songs
song_summary = song_summary.head(100)

# Create a new DataFrame that holds all the artists with their genres (use the get_artist_tags function from musicAPI.py to get the tags and then the genres for each artist)
artist_genres = []
for artist in song_summary['artistName'].unique():
    tags = get_artist_tags(artist)
    if tags:
        artist_genres.append({'artistName': artist, 'genre': tags[0]['name'] if len(tags) > 0 else None, })
    else:
        artist_genres.append({'artistName': artist, 'genre':'Indie'})

artist_genres_df = pd.DataFrame(artist_genres)


# Create a new DataFrame that only has Joji songs
joji_songs = df[df['artistName'] == 'Joji']



# Check what you've got
print(df.to_string())
print(song_summary.to_string())
print(joji_songs.to_string())
df.to_csv('spotify_streaming_history.csv', index=False)
song_summary.to_csv('song_summary.csv', index=False)
joji_songs.to_csv('joji_songs.csv', index=False)
artist_genres_df.to_csv('artist_genres.csv', index=False)
