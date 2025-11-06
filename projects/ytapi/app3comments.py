import requests
import streamlit as st

# --- Streamlit setup ---
st.set_page_config(page_title="YouTube Playlist Viewer", layout="wide")

# --- YouTube API credentials ---
API_KEY = "AIzaSyAw4FGWu6rZK515FA_5ID1UkMKOG8heDxs"

# PLAYLIST_ID = "PLbdsuU_MGf0cshTlm6fADLaGco4jF5V9N"
PLAYLIST_ID = "PLbdsuU_MGf0cJolt7k6EKdSxa9JSUEqex"
# https://www.youtube.com/playlist?list=PLbdsuU_MGf0cJolt7k6EKdSxa9JSUEqex
# --- Helper function: get playlist videos ---
@st.cache_data
def get_playlist_videos(api_key, playlist_id):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        "part": "snippet",
        "maxResults": 50,
        "playlistId": playlist_id,
        "key": api_key
    }
    response = requests.get(url, params=params).json()

    videos = []
    for item in response.get("items", []):
        snippet = item["snippet"]
        video_id = snippet["resourceId"]["videoId"]
        title = snippet["title"]
        description = snippet.get("description", "")
        thumbnails = snippet.get("thumbnails", {})
        thumb_url = (
            thumbnails.get("medium", {}).get("url") or
            thumbnails.get("high", {}).get("url") or
            thumbnails.get("default", {}).get("url") or
            "https://via.placeholder.com/320x180?text=No+Thumbnail"
        )
        videos.append({
            "id": video_id,
            "title": title,
            "description": description,
            "thumbnail": thumb_url
        })
    return videos

# --- Helper function: get video description (for freshness) ---
def get_video_description(api_key, video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet",
        "id": video_id,
        "key": api_key
    }
    response = requests.get(url, params=params).json()
    items = response.get("items", [])
    if items:
        return items[0]["snippet"].get("description", "No description available.")
    return "No description found."

# --- Helper function: get top 5 comments ---
def get_video_comments(api_key, video_id, max_results=5):
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": max_results,
        "key": api_key
    }
    response = requests.get(url, params=params).json()
    comments = []
    for item in response.get("items", []):
        snippet = item["snippet"]["topLevelComment"]["snippet"]
        comments.append({
            "author": snippet["authorDisplayName"],
            "text": snippet["textDisplay"]
        })
    return comments

# --- Load playlist ---
videos = get_playlist_videos(API_KEY, PLAYLIST_ID)

st.sidebar.title("🎥 Playlist Videos")

if not videos:
    st.sidebar.error("No videos found. Check your API key or playlist ID.")
else:
    video_titles = [v["title"] for v in videos]
    selected_title = st.sidebar.radio("Select a video:", video_titles)
    selected_video = next((v for v in videos if v["title"] == selected_title), videos[0])

    # --- Main content ---
    st.title("📘 YouTube Playlist Viewer")
    st.subheader(selected_video["title"])

    video_url = f"https://www.youtube.com/watch?v={selected_video['id']}"
    st.video(video_url)

    # --- Video description ---
    description = get_video_description(API_KEY, selected_video["id"])
    with st.expander("📝 Video Description", expanded=True):
        st.write(description)

    # --- Comments ---
    with st.expander("💬 Top Comments", expanded=False):
        comments = get_video_comments(API_KEY, selected_video["id"])
        if not comments:
            st.info("No comments found or comments are disabled for this video.")
        else:
            for c in comments:
                st.markdown(f"**{c['author']}**: {c['text']}")
                st.markdown("---")
