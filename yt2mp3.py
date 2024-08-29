import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp
from pydub import AudioSegment
import os

import tkinter as tk




def download_youtube_video_as_mp3(youtube_url, output_path='.'):
    try:
        # Download the video audio using yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        
        # Find the downloaded file
        info_dict = ydl.extract_info(youtube_url, download=False)
        title = info_dict.get('title', None)
        new_file = os.path.join(output_path, f"{title}.mp3")
        
        if os.path.isfile(new_file):
            return new_file
        else:
            raise Exception("Failed to find the downloaded MP3 file.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

def browse_output_directory():
    directory = filedialog.askdirectory()
    output_path_entry.delete(0, tk.END)
    output_path_entry.insert(0, directory)

def start_download():
    youtube_url = url_entry.get()
    output_path = output_path_entry.get()
    if not youtube_url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    if not output_path:
        output_path = '.'

    downloaded_file = download_youtube_video_as_mp3(youtube_url, output_path)
    if downloaded_file:
        messagebox.showinfo("Success", f"Downloaded and converted: {downloaded_file}")

# Set up the GUI
root = tk.Tk()
root.title("YouTube to MP3 Converter - APSoftech")

# YouTube URL input
tk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Output path input
tk.Label(root, text="Output Path:").grid(row=1, column=0, padx=10, pady=10)
output_path_entry = tk.Entry(root, width=50)
output_path_entry.grid(row=1, column=1, padx=10, pady=10)
browse_button = tk.Button(root, text="Browse", command=browse_output_directory)
browse_button.grid(row=1, column=2, padx=10, pady=10)

# Download button
download_button = tk.Button(root, text="Download", command=start_download)
download_button.grid(row=2, column=1, pady=20)




root.mainloop()
