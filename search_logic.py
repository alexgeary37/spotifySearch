import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials using environment variables
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SEC')

# Authenticate with Spotify
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def search_for_artists_by_popularity(keyword, min_popularity, max_popularity):
    offset = 0
    limit = 50
    max_iterations = 40  # Limit the number of iterations to prevent long searches
    current_iteration = 0
    total_artists_processed = 0
    max_total_artists = 1000  # Total number of artists to process to prevent overly long searches

    results = []

    while True:
        if current_iteration >= max_iterations or total_artists_processed >= max_total_artists:
            break

        # Search for artists with pagination
        search_results = sp.search(q=keyword, type='artist', limit=limit, offset=offset)
        artists = search_results['artists']['items']

        for artist in artists:
            popularity = artist['popularity']
            if min_popularity <= popularity <= max_popularity:
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

    return results
