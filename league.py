import time
import requests
import warnings
from spotify import play_current_song, pause_current_song, play_playlist_for_user

def get_death(access_token, playlist_name):
    url = "https://127.0.0.1:2999/liveclientdata/allgamedata"
    is_dead = False  # Track death status
    playlist_started = False  # Track if playlist started
    check_interval = 1  # Time interval between checks

    while True:
        warnings.simplefilter("ignore") 
        try:
            response = requests.get(url, verify=False)
            data = response.json()
            currentPlayer = data['activePlayer']['summonerName']
            dead = data['allPlayers']
            
            # Find the current player’s "dead" status
            for player in dead:
                if player['riotId'] == currentPlayer:
                    is_currently_dead = player['isDead']
                    break

            # Only act if the death status has changed
            if is_currently_dead and not is_dead:
                print(f"{currentPlayer} is dead!")
                if not playlist_started:
                    play_playlist_for_user(access_token, playlist_name)
                    playlist_started = True
                else:
                    play_current_song(access_token)
                is_dead = True  # Update the state

            elif not is_currently_dead and is_dead:
                print(f"{currentPlayer} is not dead!")
                pause_current_song(access_token)
                is_dead = False  # Update the state

        except requests.exceptions.ConnectionError as e:
            print("Connection error:", e)

        except requests.exceptions.RequestException as e:
            print("Error making request:", e)

        except KeyError:
            print("Unable to retrieve death status..")

        time.sleep(check_interval)
