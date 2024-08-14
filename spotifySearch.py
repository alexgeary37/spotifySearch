import os
import sys
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

# Error handling for command-line arguments
if len(sys.argv) < 4:
    print("Usage: python3 myscript.py <keyword> <min_popularity> <max_popularity>")
    sys.exit(1)

# Command-line arguments
keyword = sys.argv[1]
min_popularity = int(sys.argv[2])
max_popularity = int(sys.argv[3])

def search_for_artists_by_popularity(keyword, min_popularity, max_popularity):
    offset = 0
    limit = 50
    found_artist = False

    while True:
        # Search for artists with pagination
        results = sp.search(q=keyword, type='artist', limit=limit, offset=offset)
        artists = results['artists']['items']

        for artist in artists:
            popularity = artist['popularity']
            if min_popularity <= popularity <= max_popularity:
                print(f"Artist: {artist['name']}, Popularity: {popularity}, URL: {artist['external_urls']['spotify']}")
                found_artist = True

        # Break the loop if no more artists are found
        if len(artists) < limit:
            break
        
        offset += limit  # Move to the next page of results

    if not found_artist:
        print("No artists found within the specified popularity range.")

# Main program
search_for_artists_by_popularity(keyword=keyword, min_popularity=min_popularity, max_popularity=max_popularity)
