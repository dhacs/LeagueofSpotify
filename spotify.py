import requests
import base64

# Spotify API credentials here
CLIENT_ID = '00000000000000000000000000000000'
CLIENT_SECRET = '00000000000000000000000000000000' #replace with user Client ID and Secret
REDIRECT_URI = 'http://localhost:5000/callback'  # Local redirect URI
SCOPE = 'user-read-private user-read-email user-modify-playback-state user-read-playback-state user-read-currently-playing playlist-read-private'

# Spotify authorization endpoints
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
PROFILE_URL = 'https://api.spotify.com/v1/me'
SEARCH_URL = 'https://api.spotify.com/v1/search'
DEVICES_URL = 'https://api.spotify.com/v1/me/player/devices'
PLAY_URL = 'https://api.spotify.com/v1/me/player/play'
PAUSE_URL = 'https://api.spotify.com/v1/me/player/pause'

access_token = None

def get_authorization():
    """Step 1: Get authorization code by directing user to Spotify"""
    auth_query_params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "show_dialog": "true"
    }
    auth_url = f"{AUTH_URL}?{'&'.join([f'{key}={value}' for key, value in auth_query_params.items()])}"
    return auth_url

def get_access_token(code):
    """Step 2: Exchange the authorization code for an access token"""
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    token_headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(TOKEN_URL, data=token_data, headers=token_headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get access token: {response.text}")

def get_devices(access_token):
    """Fetch the list of available devices on which we can play music"""
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(DEVICES_URL, headers=headers)
    
    if response.status_code == 200:
        devices = response.json()['devices']
        return devices
    else:
        raise Exception(f"Failed to retrieve devices: {response.text}")

def get_user_playlists(access_token):
    """Fetch the current user's playlists."""
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers)

    if response.status_code == 200:
        return response.json()['items']
    else:
        raise Exception(f"Failed to retrieve playlists: {response.text}")

def search_playlist(access_token, playlist_name):
    """Search for a user's playlist by name."""
    playlists = get_user_playlists(access_token)  # Get user's playlists
    
    # Filter playlists by name
    for playlist in playlists:
        if playlist_name.lower() in playlist['name'].lower():
            return playlist['uri']  # Return the URI of the first matching playlist
    
    print("No playlists found with that name.")
    return None

def play_playlist(access_token, device_id, playlist_uri):
    """Play a specific playlist on the selected device"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "context_uri": playlist_uri
    }

    play_url = f"{PLAY_URL}?device_id={device_id}"
    response = requests.put(play_url, headers=headers, json=body)
    
    if response.status_code == 204:
        print("Playback started successfully!")
    else:
        print(f"Error: {response.status_code} - {response.json()}")

def play_playlist_for_user(access_token, playlist_name):
    """Search for a playlist and play it"""
    devices = get_devices(access_token)
    
    if devices:
        selected_device_id = devices[0]['id']  # Choose the first available device
        playlist_uri = search_playlist(access_token, playlist_name)
        
        if playlist_uri:
            play_playlist(access_token, selected_device_id, playlist_uri)

def get_current_playback_state(access_token):
    """Get the current playback state of the user"""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://api.spotify.com/v1/me/player', headers=headers)
    if response.status_code == 200:
        print(response)
        return response.json()
    else:
        print(f"Failed to get current playback state: {response.status_code} - {response.text}")
        return None

def pause_current_song(access_token):
    """Pause the currently playing song on Spotify"""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Check if a device is active and playback is ongoing
    playback_state = get_current_playback_state(access_token)
    if playback_state and playback_state['is_playing']:
        response = requests.put('https://api.spotify.com/v1/me/player/pause', headers=headers)

        if response.status_code == 200 or response.status_code == 204:
            print("Playback paused successfully!")
        else:
            try:
                error_response = response.json()
                print(f"Failed to pause playback: {response.status_code} - {error_response}")
            except ValueError:
                print(f"Failed to pause playback: {response.status_code} - No response content")
    else:
        print("No active device or nothing is currently playing.")

def play_current_song(access_token):
    """Resume playing the current song on Spotify."""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Check if a device is active and playback is paused
    playback_state = get_current_playback_state(access_token)
    if playback_state and not playback_state['is_playing']:  # Check if playback is paused
        response = requests.put('https://api.spotify.com/v1/me/player/play', headers=headers)

        if response.status_code == 200 or response.status_code == 204:
            print("Playback resumed successfully!")
        else:
            try:
                error_response = response.json()
                print(f"Failed to resume playback: {response.status_code} - {error_response}")
            except ValueError:
                print(f"Failed to resume playback: {response.status_code} - No response content")
    else:
        print("No active device or playback is already playing.")