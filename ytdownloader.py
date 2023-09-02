
# NOTE: If you encounter the "HTTP Error 403: Forbidden" error, it might be due to the following reasons:
# - IP or User-Agent Restrictions: YouTube might restrict access to its videos based on IP addresses or User-Agent headers.
#   Make sure you're not using a VPN or proxy that might have an IP address that's blocked by YouTube.
#   Additionally, some download tools allow you to set a custom User-Agent header, so you could try changing it to mimic a web browser.

import youtube_dl
import os
import googleapiclient.discovery
from spotify_playlist import get_playlist_songs

# Replace with your own youtube API credentials
api_key = ''
download_directory = r""


def get_mix_details(youtube_mix_link):
    ydl_opts = {
        'quiet': True, 
        'extract_flat': True, 
    }
    try:
        with youtube_dl.YoutubeDL({**ydl_opts, 'outtmpl': os.path.join(download_directory, '%(title)s.%(ext)s')}) as ydl:
            info = ydl.extract_info(youtube_mix_link, download=False)
            if 'entries' in info:
                songs = [entry['title'] for entry in info['entries']]
            else:
                songs = []

            return songs

    except Exception as e:
        return "Error:", str(e)

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

def get_user_choice_and_songs():
    while True:
        print("Choose an option:")
        print("1. Download from Spotify")
        print("2. Download from YouTube")
        user_choice = input("Enter the number of your choice (1 or 2): ")
        print("************ user choice : ", user_choice)

        if user_choice == '1':
            playlist_link = input("Insert Spotify playlist link: ")
            songs = get_playlist_songs(playlist_link)
            return songs 
        elif user_choice == '2':
            playlist_link = input("Insert YouTube Mix link: ")
            songs = get_mix_details(playlist_link)
            return songs
        else:
            print("Invalid choice. Please enter '1' for Spotify or '2' for YouTube.")

#search for a song on YouTube and get its URL
def search_song(song_name):
    try:
        search_response = youtube.search().list(
            q=song_name,
            type="video",
            part="id",
            maxResults=1
        ).execute()
        video = search_response.get("items")[0]
        video_id = video["id"]["videoId"]

        youtube_url = f"https://www.youtube.com/watch?v={video_id}"

        return youtube_url

    except Exception as e:
        return str(e)

#download a song given its YouTube URL
def song_downloader(video_url, song_name):
    video_info = youtube_dl.YoutubeDL().extract_info(
        url=video_url,
        download=False
    )
    # Define the filename for the downloaded audio file (with the specified download directory)
    filename = os.path.join(download_directory, f"{video_info['title']}.mp3")
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print(f"Download of '{song_name}' complete. Saved to {filename}")

if __name__ == '__main__':
    songs = []
    
    songs = get_user_choice_and_songs()
    print("************ songs : " , songs )
    for song_name in songs:
        try:
            # Search for the song on YouTube
            youtube_url = search_song(song_name)
            if youtube_url:
                print(f"Downloading '{song_name}'...")
                song_downloader(youtube_url, song_name)
            else:
                print(f"Song '{song_name}' not found on YouTube.")

        except Exception as e:
            print(f"Error downloading '{song_name}': {str(e)}")


