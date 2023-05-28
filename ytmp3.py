from pytube import YouTube
import ffmpeg
import os
import sys
import time
import multiprocessing

DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'Music/ytmp3/')

def download_audio_from_video(url, song_name=""):
    # Download high quality audio of video from YouTube to MP4
    yt = YouTube(str(url))
    print(f"Downloading {yt.title}")
    mp4_file_path = yt.streams.filter(only_audio=True).first().download(output_path=DOWNLOAD_DIR)
    print("Downloaded m4a, converting to mp3 with ffmpeg-python")
    # Convert to MP3
    base, ext = os.path.splitext(mp4_file_path)
    mp3_file_path = base + '.mp3'
    with open(os.devnull, "w") as devnull:
        ffmpeg.input(mp4_file_path).output(mp3_file_path).overwrite_output().run(quiet=True)
    with open(mp3_file_path) as mp3_file:
        print("Successfully downloaded {yt.title}")
    os.remove(mp4_file_path)

if __name__ == "__main__":
    url = sys.argv[1]
    download_thread = multiprocessing.Process(target=download_audio_from_video, args=(url, ""))
    download_thread.start()
    while download_thread.is_alive():
        print(".", end="")
        sys.stdout.flush()
        time.sleep(0.1)
        
