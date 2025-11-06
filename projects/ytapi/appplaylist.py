import requests
import streamlit as st

# --- Streamlit setup ---
st.set_page_config(page_title="Courses Dashboard", layout="wide")
# Page title
st.title("Welcome to **CSwithShahil** - Free Online Courses Platform")

API_KEY = st.secrets["YOUTUBE_API_KEY"]


# Load playlists data from secrets
playlists_data = st.secrets["playlists"]["data"]

# Extract only playlist IDs
PLAYLISTS = [{"id": p["id"]} for p in playlists_data]

# PLAYLISTS = [{"id": pid} for pid in st.secrets["playlists"]["ids"]]


# --- List of playlists ---
# PLAYLISTS = [
#     {"id": "PLbdsuU_MGf0cJolt7k6EKdSxa9JSUEqex"},
#     {"id": "PLbdsuU_MGf0cshTlm6fADLaGco4jF5V9N"},
#     {"id": "PLbdsuU_MGf0eq83haO7J1pOYdw07aSWJO"}
#     # Add more playlist IDs here
# ]

# --- Cache playlist details ---
@st.cache_data
def get_playlist_details(api_key, playlist_id):
    url = "https://www.googleapis.com/youtube/v3/playlists"
    params = {"part": "snippet", "id": playlist_id, "key": api_key}
    response = requests.get(url, params=params).json()
    items = response.get("items", [])
    if not items:
        return None
    snippet = items[0]["snippet"]
    return {
        "title": snippet["title"],
        "thumbnail": snippet["thumbnails"]["medium"]["url"]
    }

# --- Cache videos ---
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
        videos.append({
            "id": snippet["resourceId"]["videoId"],
            "title": snippet["title"],
            "description": snippet.get("description", "")
        })
    return videos

# --- Video description and comments ---
def get_video_description(api_key, video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos"
    params = {"part": "snippet", "id": video_id, "key": api_key}
    response = requests.get(url, params=params).json()
    items = response.get("items", [])
    if items:
        return items[0]["snippet"].get("description", "No description available.")
    return "No description found."

def get_video_comments(api_key, video_id, max_results=5):
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {"part": "snippet", "videoId": video_id, "maxResults": max_results, "key": api_key}
    response = requests.get(url, params=params).json()
    comments = []
    for item in response.get("items", []):
        snippet = item["snippet"]["topLevelComment"]["snippet"]
        comments.append({
            "author": snippet["authorDisplayName"],
            "text": snippet["textDisplay"]
        })
    return comments


# --- Session state for selected playlist ---
if "selected_playlist" not in st.session_state:
    st.session_state.selected_playlist = None

# --- Home page: show playlists ---
if st.session_state.selected_playlist is None:
    st.title("📚 Courses Playlist")
    cols = st.columns(3)
    for idx, pl in enumerate(PLAYLISTS):
        details = get_playlist_details(API_KEY, pl["id"])
        if details:
            col = cols[idx % 3]
            with col:
                st.image(details["thumbnail"], use_container_width=True)
                if st.button(details["title"], key=pl["id"]):
                    st.session_state.selected_playlist = pl["id"]


# --- Playlist page: show videos ---
else:
    playlist_id = st.session_state.selected_playlist
    st.button("⬅ Back to Playlists", on_click=lambda: st.session_state.update({"selected_playlist": None}))
    
    videos = get_playlist_videos(API_KEY, playlist_id)
    st.sidebar.title("🎥 Playlist Videos")
    if not videos:
        st.sidebar.error("No videos found. Check your API key or playlist ID.")
    else:
        video_titles = [v["title"] for v in videos]
        selected_title = st.sidebar.radio("Select a video:", video_titles)
        selected_video = next((v for v in videos if v["title"] == selected_title), videos[0])

        st.title("📘 YouTube Playlist Viewer")
        st.subheader(selected_video["title"])
        video_url = f"https://www.youtube.com/watch?v={selected_video['id']}"
        st.video(video_url)

        # Description
        description = get_video_description(API_KEY, selected_video["id"])
        with st.expander("📝 Video Description", expanded=True):
            st.write(description)

        # Comments
        with st.expander("💬 Top Comments", expanded=False):
            comments = get_video_comments(API_KEY, selected_video["id"])
            if not comments:
                st.info("No comments found or comments are disabled for this video.")
            else:
                for c in comments:
                    st.markdown(f"**{c['author']}**: {c['text']}")
                    st.markdown("---")























# import requests
# import streamlit as st

# # --- Streamlit page config ---
# st.set_page_config(page_title="YouTube Playlists Dashboard", layout="wide")

# # --- YouTube API credentials ---
# API_KEY = "AIzaSyAw4FGWu6rZK515FA_5ID1UkMKOG8heDxs"
# # PLAYLIST_ID = "PLbdsuU_MGf0cshTlm6fADLaGco4jF5V9N"

# # Example: your playlists (replace with real playlist IDs)
# PLAYLISTS = [
#     {"id": "PLbdsuU_MGf0cshTlm6fADLaGco4jF5V9N"},
#     {"id": "PLbdsuU_MGf0dx_pWVPrCSHFkDnKRg9BCB"},
# ]

# # --- Function to get playlist details ---
# @st.cache_data
# def get_playlist_details(api_key, playlist_id):
#     url = "https://www.googleapis.com/youtube/v3/playlists"
#     params = {"part": "snippet", "id": playlist_id, "key": api_key}
#     response = requests.get(url, params=params).json()
#     items = response.get("items", [])
#     if not items:
#         return None
#     snippet = items[0]["snippet"]
#     return {
#         "title": snippet["title"],
#         "thumbnail": snippet["thumbnails"]["medium"]["url"]
#     }

# # --- Function to get videos in a playlist ---
# @st.cache_data
# def get_playlist_videos(api_key, playlist_id):
#     url = "https://www.googleapis.com/youtube/v3/playlistItems"
#     params = {"part": "snippet", "playlistId": playlist_id, "maxResults": 50, "key": api_key}
#     response = requests.get(url, params=params).json()
#     videos = []
#     for item in response.get("items", []):
#         snippet = item["snippet"]
#         videos.append({
#             "id": snippet["resourceId"]["videoId"],
#             "title": snippet["title"],
#             "description": snippet.get("description", "")
#         })
#     return videos

# # --- Session state to track current playlist ---
# if "selected_playlist" not in st.session_state:
#     st.session_state.selected_playlist = None

# # --- Main Page ---
# if st.session_state.selected_playlist is None:
#     st.title("📚 My YouTube Playlists")

#     cols = st.columns(3)
#     for idx, pl in enumerate(PLAYLISTS):
#         details = get_playlist_details(API_KEY, pl["id"])
#         if details:
#             col = cols[idx % 3]
#             with col:
#                 st.image(details["thumbnail"], use_container_width=True)
#                 if st.button(details["title"], key=pl["id"]):
#                     st.session_state.selected_playlist = pl["id"]
# else:
#     playlist_id = st.session_state.selected_playlist
#     st.button("⬅ Back to Playlists", on_click=lambda: st.session_state.update({"selected_playlist": None}))

#     # Show videos for selected playlist
#     videos = get_playlist_videos(API_KEY, playlist_id)
#     st.subheader("Videos in this Playlist")

#     for video in videos:
#         video_url = f"https://www.youtube.com/watch?v={video['id']}"
#         st.markdown(f"### [{video['title']}]({video_url})")
#         st.video(video_url)
#         st.write(video["description"])
#         st.divider()


