#!/usr/bin/env python3
"""
Obtain or refresh SoundCloud access token using PKCE.

# !GETTING THE AUTH_CODE! (for ~5 minutes):
# curl -X POST https://secure.soundcloud.com/authorize?client_id={CLIENT_ID}\
# &redirect_uri={REDIRECT_URI}\
# &response_type=code\
# &code_challenge=base64urlencode(sha256({CODE_VERIFIER}))\
# &code_challenge_method=S256\
# &state={CSRF_STATE}

"""

import requests
import os

# === CONFIGURATION ===
TOKEN_URL = "https://secure.soundcloud.com/oauth/token"
ACCESS_TOKEN_FILE = 'soundcloud_token.txt'
REFRESH_TOKEN_FILE = 'refresh_token.txt'

def read_value(filename):
    """Read and strip a value from a text file."""
    with open(filename, "r") as f:
        return f.read().strip()

# Read configuration values from files
CLIENT_ID = read_value("client_id.txt")
CLIENT_SECRET = read_value("client_secret.txt")
REDIRECT_URI = read_value("redirect_uri.txt")
CODE_VERIFIER = read_value("code_verifier.txt")
AUTH_CODE = read_value("auth_code.txt")

# === TOKEN REQUEST (initial authorization) ===
def request_access_token():
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": CODE_VERIFIER,
        "code": AUTH_CODE,
    }

    headers = {
        "accept": "application/json; charset=utf-8",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    print("Requesting access token from SoundCloud...")

    resp = requests.post(TOKEN_URL, data=data, headers=headers)
    if resp.status_code == 200:
        token_info = resp.json()
        print("\n✅ Access token obtained successfully!\n")
        print("Access token:", token_info.get("access_token"))
        print("Refresh token:", token_info.get("refresh_token"))
        print("Expires in:", token_info.get("expires_in", "0"))

        # Save tokens
        if "access_token" in token_info:
            with open(ACCESS_TOKEN_FILE, "w") as f:
                f.write(token_info["access_token"])
        if "refresh_token" in token_info:
            with open(REFRESH_TOKEN_FILE, "w") as f:
                f.write(token_info["refresh_token"])
        print("\n💾 Tokens saved.")
    else:
        print(f"\n❌ Failed ({resp.status_code}):\n{resp.text}")

# === REFRESH FUNCTION ===
def refresh_access_token():
    refresh_token = read_value(REFRESH_TOKEN_FILE)
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token,
    }
    headers = {
        "accept": "application/json; charset=utf-8",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    print("Refreshing access token...")

    resp = requests.post(TOKEN_URL, data=data, headers=headers)
    if resp.status_code == 200:
        token_info = resp.json()
        print("\n✅ Access token refreshed!\n")
        print("New access token:", token_info.get("access_token"))
        print("Expires in:", token_info.get("expires_in", "0"))

        # Store new access token
        if "access_token" in token_info:
            with open(ACCESS_TOKEN_FILE, "w") as f:
                f.write(token_info["access_token"])
            print(f"💾 New access token saved to '{ACCESS_TOKEN_FILE}'")
    else:
        print(f"\n❌ Refresh failed ({resp.status_code}):\n{resp.text}")

# === MAIN ===
if __name__ == "__main__":
    if os.path.exists(REFRESH_TOKEN_FILE):
        refresh_access_token()
    else:
        request_access_token()
