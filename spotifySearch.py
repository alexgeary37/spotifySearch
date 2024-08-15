import os
import sys
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tkinter as tk
from tkinter import messagebox

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials using environment variables
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SEC')

# Authenticate with Spotify
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Function to search for artists by popularity
def search_for_artists_by_popularity(keyword, min_popularity, max_popularity):
    offset = 0
    limit = 50
    found_artist = False
    max_iterations = 20  # Limit the number of iterations to prevent long searches
    current_iteration = 0
    total_artists_processed = 0
    max_total_artists = 1000  # Total number of artists to process to prevent overly long searches

    results_text.delete(1.0, tk.END)  # Clear the text area before showing new results

    while True:
        if current_iteration >= max_iterations:
            results_text.insert(tk.END, "Reached maximum number of iterations.\n")
            break

        if total_artists_processed >= max_total_artists:
            results_text.insert(tk.END, "Reached maximum number of artists processed.\n")
            break

        # Search for artists with pagination
        results = sp.search(q=keyword, type='artist', limit=limit, offset=offset)
        artists = results['artists']['items']

        index = 1
        for artist in artists:
            popularity = artist['popularity']
            if min_popularity <= popularity <= max_popularity:
                results_text.insert(tk.END, f"{index}-Artist: {artist['name']}, Popularity: {popularity}, URL: {artist['external_urls']['spotify']}\n")
                found_artist = True
                index += 1

        total_artists_processed += len(artists)
        current_iteration += 1

        if len(artists) < limit:
            break

        offset += limit

        # Prompt the user if the search is taking too long
        if current_iteration % 10 == 0:
            continue_search = messagebox.askyesno("Continue Search", "The search is returning many results. Do you want to continue?")
            if not continue_search:
                break

    if not found_artist:
        results_text.insert(tk.END, "No artists found within the specified popularity range.\n")

# Function to handle the button click event
def on_search_click():
    try:
        keyword = keyword_entry.get()
        min_popularity = int(min_popularity_entry.get())
        max_popularity = int(max_popularity_entry.get())

        if keyword == "":
            messagebox.showerror("Input Error", "Please enter a keyword.")
            return

        search_for_artists_by_popularity(keyword, min_popularity, max_popularity)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for popularity.")

# Create the main window
root = tk.Tk()
root.title("Spotify Artist Search by Popularity")

# Configure grid to make widgets grow with the window
root.grid_rowconfigure(4, weight=1)  # Row for the results_text
root.grid_columnconfigure(1, weight=1)  # Column for the entry fields and text area

# Keyword input
tk.Label(root, text="Keyword:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
keyword_entry = tk.Entry(root)
keyword_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Minimum popularity input
tk.Label(root, text="Min Popularity:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
min_popularity_entry = tk.Entry(root)
min_popularity_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Maximum popularity input
tk.Label(root, text="Max Popularity:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
max_popularity_entry = tk.Entry(root)
max_popularity_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

# Search button
search_button = tk.Button(root, text="Search", command=on_search_click)
search_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Text area to display results
results_text = tk.Text(root, height=15, width=80)
results_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Run the application
root.mainloop()
