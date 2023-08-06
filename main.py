from pytube import YouTube
import requests
from tqdm import tqdm

def download_youtube_video(url, output_path='.', resolution='1080p'):
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the best quality progressive stream available
        stream = yt.streams.filter(progressive=True).get_highest_resolution()
        #stream = yt.streams.filter(file_extension='mp4', resolution=resolution).first()

        # Get the video title for progress bar display
        video_title = yt.title

        # Get the video stream URL
        video_url = stream.url

        # Set up the progress bar
        response = requests.get(video_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size, unit='bytes', unit_scale=True, desc=video_title, ascii=True)

        # Download the video with progress bar
        with open(f"{output_path}/{video_title}.mp4", "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    progress_bar.update(len(chunk))

        progress_bar.close()
        print("\nVideo downloaded successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_youtube_video(video_url)
