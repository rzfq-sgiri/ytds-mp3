import streamlit as st
import yt_dlp
import os
import imageio_ffmpeg as ffmpeg  # Untuk muat turun automatik


# Set page title and icon
st.set_page_config(
    page_title="YouTube MP3 Downloader",  # Ganti dengan nama aplikasi anda
    page_icon="🎥",  # Ganti dengan emoji atau ikon unicode lain
)

def download_with_ytdlp(url):
    try:
        ffmpeg_path = ffmpeg.get_ffmpeg_exe()  # Muat turun FFmpeg jika tidak ada
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'ffmpeg_location': ffmpeg_path,  # Gunakan FFmpeg yang dimuat turun
        }
        st.write("Downloading ...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = os.path.splitext(ydl.prepare_filename(info))[0] + ".mp3"
            st.success("Download complete!")
            return filename
    except Exception as e:
        st.error(f"Download Failed : {e}")
        st.write(f"Details: {e.__class__.__name__} - {str(e)}")
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
        ver:0.3
        """
    )

def show_error_menu():
    st.warning("It seems there was an error. Here are some alternative options:")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Try Again")
    with col2:
        if st.button("Open Alternative URL (Video Downloader)"):
            js = "window.open('https://5g2rzdeptz6wrltb2fgeul.streamlit.app/')"
            st.write(f'<script>{js}</script>', unsafe_allow_html=True)
            
def main():
    st.title("YouTube MP3 Downloader with Error Handling")
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
            else:
                show_error_menu()

if __name__ == "__main__":
    main()
    display_disclaimer()
