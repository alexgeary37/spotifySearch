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

# Convert command-line arguments to integers
min_followers = int(sys.argv[1])  # sys.argv[0] is the script name, so start with sys.argv[1]
max_followers = int(sys.argv[2])

def search_for_artists(keyword, min_followers, max_followers):
    results = sp.search(q=keyword, type='artist', limit=50)
    artists = results['artists']['items']
    
    found_artist = False
    for artist in artists:
        followers = artist['followers']['total']
        if min_followers < followers < max_followers:
            print(f"Artist: {artist['name']}, Followers: {followers}, URL: {artist['external_urls']['spotify']}")
            found_artist = True
    
    if not found_artist:
        print("No artists found within the specified follower range.")

# main program
search_for_artists(keyword='indie', min_followers=min_followers, max_followers=max_followers)
