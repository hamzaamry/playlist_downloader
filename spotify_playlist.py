import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Replace with your own Spotify API credentials
client_id = ''
client_secret = ''

# Initialize the Spotify API client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlist_songs(playlist_link):
    # Extract playlist URI from the link
    playlist_URI = playlist_link.split('/')[-1].split("?")[0]
    songs = []

    for track in sp.playlist_tracks(playlist_URI)["items"]:
        track_name = track["track"]["name"]
        songs.append(track_name)

    return songs

if __name__ == '__main__':
    playlist_link = input("Insert Spotify playlist link: ")
    spotify_songs = get_playlist_songs(playlist_link)
    print('Spotify playlist songs:', spotify_songs)
