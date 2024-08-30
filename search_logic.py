import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
import requests.exceptions
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials using environment variables
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SEC')

# Authenticate with Spotify
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def was_last_release_in_last_year(artist_id, last_year):
    try:
        albums = sp.artist_albums(artist_id, album_type='album,single', limit=1)
        if albums['items']:
            latest_release_date = albums['items'][0]['release_date']
            print(latest_release_date, " ", int(latest_release_date[:4]) >= last_year)
            return int(latest_release_date[:4]) >= last_year
    except (SpotifyException, requests.exceptions.ReadTimeout):
        # Skip this artist and move on to the next if there's a timeout or Spotify API error
        return False

def search_for_artists_by_popularity(keyword, popularity_setting, start_offset):
    last_year = datetime.now().year - 1 # Define the current year here
    offset = start_offset
    limit = 50
    current_iteration = 0
    max_iterations = 40  # Limit the number of iterations to prevent long searches
    total_artists_processed = 0
    max_total_artists = 1000  # Total number of artists to process to prevent overly long searches

    results = []
    results.append({
        'keyword': keyword,
        'popularity' : popularity_setting,
        'start_offset': start_offset,
    })

    while True:
        if current_iteration >= max_iterations or total_artists_processed >= max_total_artists:
            break

        # Search for artists with pagination
        search_results = sp.search(q=keyword, type='artist', limit=limit, offset=offset)
        artists = search_results['artists']['items']

        for artist in artists:
            popularity = artist['popularity']
            if popularity == popularity_setting and was_last_release_in_last_year(artist['id'], last_year):
                results.append({
                    'name': artist['name'],
                    'popularity': popularity,
                    'url': artist['external_urls']['spotify']
                })

        total_artists_processed += len(artists)
        current_iteration += 1

        if len(artists) < limit:
            break

        offset += limit
        if offset > 9999:
            break
        print("Offset:", offset)

    return results
