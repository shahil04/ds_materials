import requests
import streamlit as st

st.set_page_config(page_title="YouTube Playlist Viewer", layout="wide")

API_KEY = "AIzaSyAw4FGWu6rZK515FA_5ID1UkMKOG8heDxs"
PLAYLIST_ID = "PLbdsuU_MGf0cshTlm6fADLaGco4jF5V9N"

st.title("🎥 YouTube Playlist Viewer")
st.write("Fetching playlist videos...")

url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={PLAYLIST_ID}&key={API_KEY}"
response = requests.get(url).json()

if "items" not in response:
    st.error("Failed to fetch data. Check your API key or playlist ID.")
else:
    for item in response["items"]:
        snippet = item["snippet"]
        title = snippet["title"]
        video_id = snippet["resourceId"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # ✅ Safely handle missing thumbnails
        thumbnails = snippet.get("thumbnails", {})
        thumbnail_url = (
            thumbnails.get("medium", {})
            .get("url")
            or thumbnails.get("high", {})
            .get("url")
            or thumbnails.get("default", {})
            .get("url")
            or "https://via.placeholder.com/320x180?text=No+Thumbnail"
        )

        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(thumbnail_url, use_container_width=True)
        with col2:
            st.markdown(f"### [{title}]({video_url})")
            st.write(f"**Channel:** {snippet.get('channelTitle', 'Unknown')}")
            st.write(f"📅 Published on: {snippet.get('publishedAt', 'N/A')[:10]}")
        st.divider()












# import requests
# import streamlit as st

# st.set_page_config(page_title="YouTube Playlist Viewer", layout="wide")

# API_KEY = "AIzaSyAw4FGWu6rZK515FA_5ID1UkMKOG8heDxs"
# PLAYLIST_ID = "PLbdsuU_MGf0cshTlm6fADLaGco4jF5V9N"

# st.title("🎥 YouTube Playlist Viewer")
# st.write("Fetching playlist videos...")

# url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={PLAYLIST_ID}&key={API_KEY}"
# response = requests.get(url).json()

# if "items" not in response:
#     st.error("Failed to fetch data. Check your API key or playlist ID.")
# else:
#     for item in response["items"]:
#         snippet = item["snippet"]
#         title = snippet["title"]
#         thumbnail = snippet["thumbnails"]["medium"]["url"]
#         video_id = snippet["resourceId"]["videoId"]
#         video_url = f"https://www.youtube.com/watch?v={video_id}"

#         col1, col2 = st.columns([1, 3])
#         with col1:
#             st.image(thumbnail, use_container_width=True)
#         with col2:
#             st.markdown(f"### [{title}]({video_url})")
#             st.write(f"**Channel:** {snippet['channelTitle']}")
#             st.write(f"📅 Published on: {snippet['publishedAt'][:10]}")
#         st.divider()
