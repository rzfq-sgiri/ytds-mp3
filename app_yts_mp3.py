import streamlit as st
import yt_dlp
import os

def download_with_ytdlp(url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',  # Pilih format audio terbaik
            'postprocessors': [{
                'key': 'FFmpegAudioConvertor',  # Menggunakan FFmpeg untuk menukar format
                'preferredcodec': 'mp3',  # Tukar ke MP3
                'preferredquality': '192',  # Kualiti MP3
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Simpan dalam folder "downloads"
        }
        st.write("Downloading with yt-dlp...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            st.success("Download complete with yt-dlp!")
            return filename
    except Exception as e:
        st.error(f"yt-dlp failed: {e}")
        return None

def main():
    st.title("YouTube Audio Downloader (MP3)")
    url = st.text_input("Enter the YouTube video URL:")
    if st.button("Download"):
        if url:
            filename = download_with_ytdlp(url)
            if filename:
                with open(filename, "rb") as file:
                    st.download_button(
                        label="Click here to download the MP3 file",
                        data=file,
                        file_name=os.path.basename(filename),
                        mime="audio/mp3"
                    )

if __name__ == "__main__":
    main()
