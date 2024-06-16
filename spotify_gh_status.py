#!/usr/bin/env python3
import os
import time
import requests
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')

# authentication 
scope = "user-read-playback-state user-read-currently-playing"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

def get_current_song():
    current = sp.current_playback()
    if current is None or current['item'] is None:
        return None
    item = current['item']
    artist_names = ', '.join([artist['name'] for artist in item['artists']])
    song_name = item['name']
    return f"{song_name} by {artist_names}"

def update_github_status(status):
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json",
    }
    query = """
    mutation ($input: ChangeUserStatusInput!) {
      changeUserStatus(input: $input) {
        status {
          message
        }
      }
    }
    """
    variables = {
        "input": {
            "message": status,
            "emoji": ":musical_note:",  
            "limitedAvailability": False  
        }
    }
    data = {
        "query": query,
        "variables": variables
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("GitHub status updated successfully")
    else:
        print(f"Failed to update GitHub status: {response.status_code}, {response.json()}")

def main():
    while True:
        current_song = get_current_song()
        if current_song:
            update_github_status(current_song)
        else:
            print("No song currently playing")
        time.sleep(20) 

if __name__ == "__main__":
    main()
