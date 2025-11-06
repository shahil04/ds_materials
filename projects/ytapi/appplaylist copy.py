import requests
import streamlit as st

# --- Streamlit setup ---
st.set_page_config(page_title="Courses Dashboard", layout="wide")

# --- Page Title ---
st.title("Welcome to **CSwithShahil** - Free Online Courses Platform")

# --- YouTube Subscribe Button ---
channel_id = "UCM1Ge17WU-d2QwIvFVDlNSA"
subscribe_url = f"https://www.youtube.com/channel/{channel_id}?sub_confirmation=1"

st.sidebar.markdown(
    f"""
    <style>
        .sidebar-subscribe {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .subscribe-button {{
            background: linear-gradient(135deg, #ff0000, #cc0000);
            color: #ffffff !important;
            padding: 12px 26px;
            border: none;
            border-radius: 50px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none !important;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            box-shadow: 0 6px 20px rgba(255, 0, 0, 0.4);
            transition: all 0.3s ease;
            animation: pulse 2s infinite;
        }}
        .subscribe-button:hover {{
            background: linear-gradient(135deg, #e60000, #ff3333);
            transform: scale(1.07);
            box-shadow: 0 8px 25px rgba(255, 0, 0, 0.6);
        }}
        .subscribe-button:visited,
        .subscribe-button:active {{
            color: #ffffff !important;
            text-decoration: none !important;
        }}
        .subscribe-icon {{
            background-color: white;
            color: #ff0000;
            font-weight: bold;
            border-radius: 50%;
            width: 22px;
            height: 22px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
        }}
        @keyframes pulse {{
            0% {{ box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.6); }}
            70% {{ box-shadow: 0 0 0 10px rgba(255, 0, 0, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }}
        }}
    </style>

    <div class="sidebar-subscribe">
        <a href="{subscribe_url}" target="_blank" class="subscribe-button">
            <div class="subscribe-icon">▶</div>
            Subscribe on YouTube
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# --- YouTube API Key ---
API_KEY = st.secrets["YOUTUBE_API_KEY"]

# --- Load playlists data from secrets ---
playlists_data = st.secrets["playlists"]["data"]
PLAYLISTS = [{"id": p["id"], "name": p["name"]} for p in playlists_data]

# =========================
# --- NAVIGATION LOGIC ---
# =========================
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Home"


def set_nav_page(page):
    st.session_state.nav_page = page


# --- Navbar (Streamlit buttons) ---
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    if st.button("🏠 Home"):
        set_nav_page("Home")
with col2:
    if st.button("ℹ️ About Us"):
        set_nav_page("About")
with col3:
    if st.button("📞 Contact"):
        set_nav_page("Contact")
with col4:
    if st.button("💬 Support"):
        set_nav_page("Support")

st.markdown("<hr style='border:1px solid #00b4d8'>", unsafe_allow_html=True)

# --- Sidebar: Course categories ---
st.sidebar.title("📂 Course Categories")
categories = ["Forms", "Course Materials", "Feedback", "Review", "No Selected"]
selected_category = st.sidebar.selectbox("Select Category", categories, index=4)
st.sidebar.markdown("---")
st.sidebar.info(f"Showing content for **{selected_category}**")

# --- Sidebar Dynamic Content ---
if selected_category == "Forms":
    st.sidebar.markdown("### 📝 Available Forms")
    st.sidebar.markdown("- [Registration Form](https://forms.gle/example1)")
    st.sidebar.markdown("- [Feedback Form](https://forms.gle/example2)")
    st.sidebar.markdown("- [Course Enrollment](https://forms.gle/example3)")

elif selected_category == "Course Materials":
    st.sidebar.markdown("### 📚 Course Resources")
    st.sidebar.markdown("- [Python Basics PDF](https://example.com/python.pdf)")
    st.sidebar.markdown("- [Machine Learning Notes](https://example.com/ml.pdf)")
    st.sidebar.markdown("- [Data Science Book](https://example.com/ds.pdf)")

elif selected_category == "Feedback":
    st.sidebar.markdown("### 💬 Submit Feedback")
    st.sidebar.markdown("- [Feedback Form](https://forms.gle/xyz123)")
    st.sidebar.markdown("- [Rate Instructor](https://forms.gle/abc456)")

elif selected_category == "Review":
    st.sidebar.markdown("### ⭐ Course Reviews")
    st.sidebar.markdown("- [Python Course Reviews](https://example.com/review/python)")
    st.sidebar.markdown("- [Data Science Reviews](https://example.com/review/ds)")
    st.sidebar.markdown("- [AI Course Reviews](https://example.com/review/ai)")

else:
    st.sidebar.markdown("ℹ️ Select a category from the dropdown to view content.")


# --- Cache helpers ---
@st.cache_data
def get_playlist_details(api_key, playlist_id):
    url = "https://www.googleapis.com/youtube/v3/playlists"
    params = {"part": "snippet", "id": playlist_id, "key": api_key}
    response = requests.get(url, params=params).json()
    items = response.get("items", [])
    if not items:
        return None
    snippet = items[0]["snippet"]
    return {"title": snippet["title"], "thumbnail": snippet["thumbnails"]["medium"]["url"]}


@st.cache_data
def get_playlist_videos(api_key, playlist_id):
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {"part": "snippet", "maxResults": 50, "playlistId": playlist_id, "key": api_key}
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


def get_video_description(api_key, video_id):
    url = "https://www.googleapis.com/youtube/v3/videos"
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
        comments.append({"author": snippet["authorDisplayName"], "text": snippet["textDisplay"]})
    return comments


# =========================
# --- PAGE CONTENT ---
# =========================

if st.session_state.nav_page == "Home":
    st.title("📚 Courses Playlist")

    if "selected_playlist" not in st.session_state:
        st.session_state.selected_playlist = None

    if st.session_state.selected_playlist is None:
        cols = st.columns(3)
        for idx, pl in enumerate(PLAYLISTS):
            details = get_playlist_details(API_KEY, pl["id"])
            if details:
                col = cols[idx % 3]
                with col:
                    st.image(details["thumbnail"], use_container_width=True)
                    if st.button(details["title"], key=pl["id"]):
                        st.session_state.selected_playlist = pl["id"]

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

            description = get_video_description(API_KEY, selected_video["id"])
            with st.expander("📝 Video Description", expanded=True):
                st.write(description)

            with st.expander("💬 Top Comments", expanded=False):
                comments = get_video_comments(API_KEY, selected_video["id"])
                if not comments:
                    st.info("No comments found or comments are disabled for this video.")
                else:
                    for c in comments:
                        st.markdown(f"**{c['author']}**: {c['text']}")
                        st.markdown("---")


elif st.session_state.nav_page == "About":
    st.title("ℹ️ About Us")
    st.info("""
Welcome to our YouTube Learning Platform!  
We curate high-quality playlists and tutorials from experts to help you learn programming, AI, and professional skills effectively.
""")


elif st.session_state.nav_page == "Contact":
    st.title("📞 Contact Us")
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        if st.form_submit_button("Send Message"):
            st.success(f"Thank you {name}, your message has been received!")


elif st.session_state.nav_page == "Support":
    st.title("💬 Support Us")
    st.markdown("""
If you enjoy our free courses, you can support our work:
- ⭐ Star our GitHub repo  
- ☕ [Buy Me a Coffee](https://www.buymeacoffee.com)  
- 📢 Share this app with friends!
""", unsafe_allow_html=True)
