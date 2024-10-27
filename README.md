# LeagueOfSpotify: Playlist Integration with League of Legends

This project integrates Spotify playlists with the popular video game League of Legends by leveraging the League of Legends API and Spotify API to control the player's music in-game. The application continuously monitors the player's status using the Riot API, automatically playing your Spotify playlists when you die—eliminating the need to alt-tab—and pausing the music when you respawn.

To use this project, you will need approved Spotify API credentials, which are essential for authenticating and interacting with your Spotify account.

## Features
- **Spotify Authentication**: Authenticate with your Spotify account to access your playlists.
- **Playlist Selection**: Choose from your Spotify playlists to monitor during gameplay.
- **Real-time Monitoring**: The app checks the player's status at regular intervals and plays/pause music based on whether the player is dead or alive.

## Requirements

- Python 3.x
- Libraries:
  - `requests`
  - `tkinter` (included with Python)
  - `Flask`

You can install the required libraries using pip:

```bash
pip install requests Flask
```

# Usage

## Clone the Repository:

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

## Run the Application with:

```bash
py spotify_gui.py
```

## Authenticate with Spotify:

- Click the "Authenticate Spotify" button, which will open a browser window for Spotify login.
- Follow the prompts to authenticate and allow access.

## Select a Playlist:

Once authenticated, your playlists will be displayed. Select a playlist to monitor.

## Gameplay Monitoring:

The application will monitor the game for the player's death status. When the player dies, the selected playlist will start playing; if the player is alive, the music will pause.

# License

This project is licensed under the MIT License - see the LICENSE file for details.
