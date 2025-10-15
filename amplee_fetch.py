#!/usr/bin/env python3
"""
Fetch most recent liked tracks from your SoundCloud account.
"""

import requests
import sys

# === CONFIGURATION ===
ACCESS_TOKEN = ""
# Read token from file
token_file = 'soundcloud_token.txt'
try:
    with open(token_file, "r") as f:
        ACCESS_TOKEN = f.read().strip()
except FileNotFoundError:
    raise RuntimeError(f"Token file '{token_file}' not found!")

LIMIT = 30
BASE_URL = "https://api.soundcloud.com"
HEADERS = {"Authorization": f"OAuth {ACCESS_TOKEN}"}

def fetch_likes(limit=30):
    URL = f"{BASE_URL}/me/likes/tracks?limit={limit}"
    response = requests.get(URL, headers=HEADERS)

    if response.status_code == 200:
        tracks = response.json()
        for i, track in enumerate(tracks, start=1):
            title = track.get("title")
            artist = track.get("user", {}).get("username")
            url = track.get("permalink_url")
            genre = track.get("genre")
            tag_list = track.get("tag_list")
            print(f"{i}. {artist} – {title}")
            print(f"Genre: {genre}; Tags: {tag_list}")
            print(f"   {url}\n")
    else:
        print(f"Error: {response.status_code} - {response.text}")


def main():
    if ACCESS_TOKEN != "":
        fetch_likes(LIMIT)
    else:
        raise RuntimeError(f"ACCESS_TOKEN is not set or failed to be read from '{token_file}'")

if __name__ == "__main__":
    main()
