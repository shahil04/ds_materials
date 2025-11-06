import requests
import streamlit as st

# --- Streamlit page setup ---
st.set_page_config(page_title="YouTube Playlist Viewer", layout="wide")

# --- YouTube API credentials ---
API_KEY = "AIzaSyAw4FGWu6rZK515FA_5ID1UkMKOG8heDxs"
PLAYLIST_ID = "PLbdsuU_MGf0cshTlm6fADLaGco4jF5V9N"

# --- Fetch playlist data ---
@st.cache_data
def get_playlist_videos(api_key, playlist_id):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={playlist_id}&key={api_key}"
    response = requests.get(url).json()
    videos = []
    for item in response.get("items", []):
        snippet = item["snippet"]
        video_id = snippet["resourceId"]["videoId"]
        title = snippet["title"]
        description = snippet.get("description", "")
        thumbnails = snippet.get("thumbnails", {})
        thumbnail_url = (
            thumbnails.get("medium", {}).get("url")
            or thumbnails.get("high", {}).get("url")
            or thumbnails.get("default", {}).get("url")
            or "https://via.placeholder.com/320x180?text=No+Thumbnail"
        )
        videos.append({
            "id": video_id,
            "title": title,
            "desc": description,
            "thumb": thumbnail_url,
        })
    return videos

videos = get_playlist_videos(API_KEY, PLAYLIST_ID)

# --- Sidebar content ---
st.sidebar.title("🎥 Full Stack Data Science Playlist")
st.sidebar.markdown("Select a lecture to play:")

if not videos:
    st.sidebar.error("No videos found. Check your API key or playlist ID.")
else:
    # Create a list of video titles in the sidebar
    video_titles = [v["title"] for v in videos]
    selected_title = st.sidebar.radio("Lecture Videos", video_titles)

    # Find the selected video details
    selected_video = next((v for v in videos if v["title"] == selected_title), videos[0])

    # --- Main content area ---
    st.title("📘 Full Stack Data Science Pro")
    st.subheader(selected_video["title"])

    # Display video using YouTube embed
    video_url = f"https://www.youtube.com/watch?v={selected_video['id']}"
    st.video(video_url)

    # Show title and description below video
    with st.expander("📄 Video Description", expanded=True):
        st.write(selected_video["desc"])
