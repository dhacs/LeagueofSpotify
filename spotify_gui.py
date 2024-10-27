import tkinter as tk
from tkinter import messagebox, Listbox
import threading
import webbrowser
import requests
from flask import Flask, request
from spotify import get_authorization, get_access_token, get_user_playlists
from league import get_death
import os
import signal


class SpotifyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spotify Playlist Selector")
        self.access_token = None
        self.flask_thread = None

        # Authenticate Button
        self.auth_button = tk.Button(root, text="Authenticate Spotify", command=self.authenticate)
        self.auth_button.pack(pady=10)

        # Playlist Selection
        self.playlist_listbox = Listbox(root, width=50)
        self.playlist_listbox.pack(pady=10)
        self.playlist_listbox.bind("<<ListboxSelect>>", self.select_playlist)

        # Status Label
        self.status_label = tk.Label(root, text="Status: Waiting for authentication")
        self.status_label.pack(pady=10)

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def authenticate(self):
        auth_url = get_authorization()
        self.status_label.config(text="Opening Spotify login in browser...")
        webbrowser.open(auth_url)

        # Start Flask server in a separate thread for callback handling
        self.flask_thread = threading.Thread(target=self.start_callback_server)
        self.flask_thread.start()

    def start_callback_server(self):
        # Define Flask app within this method so we can stop it later
        app = Flask(__name__)

        @app.route('/callback')
        def callback():
            code = request.args.get('code')
            if code:
                token_data = get_access_token(code)
                self.access_token = token_data['access_token']
                self.status_label.config(text="Authenticated! Fetching playlists...")
                self.fetch_playlists()
            else:
                messagebox.showerror("Error", "Authorization failed.")
            return "Authorization complete. You can close this tab."

        # Run Flask app
        app.run(port=5000)

    def fetch_playlists(self):
        try:
            playlists = get_user_playlists(self.access_token)
            self.playlist_listbox.delete(0, tk.END)
            for playlist in playlists:
                self.playlist_listbox.insert(tk.END, playlist['name'])
            self.status_label.config(text="Select a playlist to monitor")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch playlists: {e}")

    def select_playlist(self, event):
        selected_index = self.playlist_listbox.curselection()
        if selected_index:
            playlist_name = self.playlist_listbox.get(selected_index)
            self.status_label.config(text=f"Monitoring playlist '{playlist_name}'")
            # Run get_death in a separate thread with the selected playlist
            threading.Thread(target=self.run_get_death, args=(playlist_name,)).start()

    def run_get_death(self, playlist_name):
        try:
            get_death(self.access_token, playlist_name)  # Assumes get_death will use the playlist in the intended way
        except Exception as e:
            messagebox.showerror("Error", f"Error running get_death: {e}")

    def on_close(self):
        """Cleanup resources before closing the app"""
        if self.flask_thread is not None:
            # Terminate Flask server
            os.kill(os.getpid(), signal.SIGTERM)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SpotifyApp(root)
    root.mainloop()
