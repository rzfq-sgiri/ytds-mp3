import streamlit as st
import yt_dlp
import os


# Set page title and icon
st.set_page_config(
    page_title="YouTube MP3 Downloader",  # Ganti dengan nama aplikasi anda
    page_icon="🎥",  # Ganti dengan emoji atau ikon unicode lain
)

def download_with_ytdlp(url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            },
            # Uncomment if you want to use a proxy
            # 'proxy': 'http://your_proxy_ip:port',
        }
        st.write("Downloading...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = os.path.splitext(ydl.prepare_filename(info))[0] + ".mp3"
            st.success("Download complete!")
            return filename
    except Exception as e:
        st.error(f"yt-dlp failed: {e}")
        return None
    
# Disclaimer content
def display_disclaimer():
    st.markdown("---")  # Horizontal line
    st.markdown(
        """
        
        **Disclaimer**  
        This application is provided as is for educational and informational purposes only.  
        The author, Risz-Sgr, is not responsible for any misuse of this tool.  
        Please ensure compliance with YouTube's terms of service and copyright laws when using this application. 
        ver: 0.0
        """
    )


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
        # Call this function at the end of the app
    display_disclaimer()


