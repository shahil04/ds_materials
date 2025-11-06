import streamlit as st
import requests
from database import fetch_playlists, fetch_courses



import streamlit as st
import requests
from database import init_db, insert_playlist, insert_course, fetch_playlists, fetch_courses

# Initialize DB
init_db()

# Streamlit Page
st.set_page_config(page_title="YouTube LMS", layout="wide")
API_KEY = st.secrets["YOUTUBE_API_KEY"]

# --- Sidebar for Admin / Frontend ---
mode = st.sidebar.selectbox("Mode", ["Frontend", "Admin Panel"])

# ---------------- Admin Panel ----------------
if mode == "Admin Panel":
    st.title("🔧 Admin Panel")

    admin_tab = st.sidebar.radio("Admin Options", ["Add Playlist", "Add Course", "View Data"])

    if admin_tab == "Add Playlist":
        st.header("➕ Add Playlist")
        playlist_id = st.text_input("Playlist ID")
        playlist_name = st.text_input("Playlist Name")
        youtube_link = st.text_input("YouTube Link")
        extract_link = st.text_input("Extract Link (optional)")
        batch = st.text_input("Batch")

        if st.button("Add Playlist"):
            if playlist_id and playlist_name:
                insert_playlist(playlist_id, playlist_name, youtube_link, extract_link, batch)
                st.success("Playlist added successfully!")
            else:
                st.error("Playlist ID and Name are required.")

    elif admin_tab == "Add Course":
        st.header("➕ Add Course")
        course_name = st.text_input("Course Name")
        youtube_link = st.text_input("YouTube Video or Playlist Link")

        if st.button("Add Course"):
            if course_name and youtube_link:
                insert_course(course_name, youtube_link)
                st.success("Course added successfully!")
            else:
                st.error("All fields are required.")

    elif admin_tab == "View Data":
        st.header("📋 Playlists")
        playlists = fetch_playlists()
        st.dataframe(playlists)

        st.header("📋 Courses")
        courses = fetch_courses()
        st.dataframe(courses)

# ---------------- Frontend ----------------
else:
    st.title("📘 YouTube LMS Player")

    # Fetch courses
    courses = fetch_courses()
    if not courses:
        st.warning("No courses available. Ask admin to add courses.")
    else:
        course_names = [c[1] for c in courses]
        selected_course = st.selectbox("Select Course", course_names)

        if selected_course:
            course = next(c for c in courses if c[1] == selected_course)
            youtube_link = course[2]

            # Check if it's a playlist or single video
            if "playlist?list=" in youtube_link:
                playlist_id = youtube_link.split("list=")[1].split("&")[0]

                # Fetch playlist videos
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
                        videos.append({"id": video_id, "title": title})
                    return videos

                videos = get_playlist_videos(API_KEY, playlist_id)

                selected_video_title = st.selectbox("Select Video", [v["title"] for v in videos])
                selected_video = next(v for v in videos if v["title"] == selected_video_title)
                st.video(f"https://www.youtube.com/watch?v={selected_video['id']}")

            else:
                # Single video
                st.video(youtube_link)







# --- Batch filter ---
playlists = fetch_playlists()
if not playlists:
    st.warning("No playlists available. Ask admin to add playlists.")
else:
    # Extract unique batches
    batches = list(set([p[5] for p in playlists if p[5]]))
    batches.insert(0, "All")  # Add 'All' option
    selected_batch = st.selectbox("Filter by Batch", batches)

    # Filter playlists by batch
    if selected_batch != "All":
        playlists = [p for p in playlists if p[5] == selected_batch]

    st.subheader("🎬 Playlists")
    # Display playlists as cards
    for p in playlists:
        playlist_id, playlist_name, youtube_link, extract_link, batch = p[1], p[2], p[3], p[4], p[5]
        col1, col2 = st.columns([1, 3])
        with col1:
            # Fetch playlist thumbnail
            try:
                url = f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&id={playlist_id}&key={API_KEY}"
                res = requests.get(url).json()
                thumb_url = res["items"][0]["snippet"]["thumbnails"]["medium"]["url"]
            except:
                thumb_url = "https://via.placeholder.com/320x180?text=No+Thumbnail"
            st.image(thumb_url, use_column_width=True)

        with col2:
            st.markdown(f"### {playlist_name}")
            st.markdown(f"**Batch:** {batch}")
            if st.button(f"Open Playlist: {playlist_name}", key=playlist_id):
                st.session_state["selected_playlist"] = playlist_id

# --- Show selected playlist videos ---
if "selected_playlist" in st.session_state:
    playlist_id = st.session_state["selected_playlist"]

    # Fetch playlist videos
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
            videos.append({"id": video_id, "title": title})
        return videos

    videos = get_playlist_videos(API_KEY, playlist_id)
    st.subheader("📌 Videos in Playlist")
    selected_video_title = st.selectbox("Select Video", [v["title"] for v in videos])
    selected_video = next(v for v in videos if v["title"] == selected_video_title)
    st.video(f"https://www.youtube.com/watch?v={selected_video['id']}")


# =====
