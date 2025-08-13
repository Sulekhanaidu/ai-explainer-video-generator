import streamlit as st
import bcrypt
import json
import os
from pipeline import run_pipeline
from utils import sanitize_topic

# File to store user credentials
CREDENTIALS_FILE = "users.json"

# Load credentials
def load_users():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as f:
            return json.load(f)
    return {}

# Save credentials
def save_users(users):
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(users, f)

# Register new user
def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[username] = hashed_pw
    save_users(users)
    return True

# Authenticate user
def authenticate_user(username, password):
    users = load_users()
    if username in users:
        return bcrypt.checkpw(password.encode(), users[username].encode())
    return False

# -----------------
# Streamlit App UI
# -----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = "login"
if "username" not in st.session_state:
    st.session_state.username = None

# -----------------
# Main App Logic
# -----------------
st.title("🧠 AI Explainer Video Generator")

if st.session_state.authenticated:
    # MAIN PAGE
    st.sidebar.button(
        "🔒 Logout",
        on_click=lambda: st.session_state.update(
            {"authenticated": False, "page": "login", "username": None}
        )
    )
    st.success(f"Welcome, {st.session_state.username} 👋")
    st.markdown('<div class="main-title">🧠 AI Explainer Video Generator</div>', unsafe_allow_html=True)

    # -- rest of the explainer video generator UI follows here -
    # 🎨 CSS Styling
    st.markdown("""
        <style>
        .main-title {
            font-size: 32px;
            color: #2A7AE2;
            font-weight: bold;
            margin-bottom: 20px;
        }
        textarea {
            font-size: 16px !important;
            font-family: "Segoe UI", sans-serif !important;
        }
        label[data-testid="stCheckbox"] {
            font-weight: bold;
            font-size: 16px;
            color: #444;
        }
        button[kind="primary"] {
            background-color: #2A7AE2;
            color: white;
            border-radius: 8px;
            font-size: 16px;
        }
        </style>
    """, unsafe_allow_html=True)

    topic = st.text_input("Enter your topic here:")
    add_subtitles = st.checkbox("Include subtitles in the video", value=True)
    use_ai_images = st.checkbox("Use AI-generated images", value=True)
    num_slides = st.slider("Select number of slides", 1, 20, 15)
    use_cache = st.checkbox("Use Cached Script if Available", value=False)

    if st.button("Generate Video"):
        if topic.strip():
            safe_topic = sanitize_topic(topic)
            with st.spinner("Generating video..."):
                run_pipeline(safe_topic, add_subtitles, use_ai_images, num_slides, use_cache)
            st.success("✅ Video generated successfully!")
            video_path = f"output/{safe_topic}/final_video_with_subs.mp4" if add_subtitles else f"output/{safe_topic}/final_video.mp4"
            if os.path.exists(video_path):
                st.video(video_path)
                with open(video_path, "rb") as f:
                    st.download_button("📥 Download Final Video", f, "ai_explainer_video.mp4", "video/mp4")
            else:
                st.error("⚠️ Video file not found.")
        else:
            st.warning("Please enter a topic.")

else:
    # LOGIN / REGISTER PAGE
    page = st.sidebar.radio("Select", ["Login", "Register"])

    if page == "Register":
        st.subheader("Create a New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        if st.button("Register"):
            if register_user(new_user, new_password):
                st.success("✅ Registered! You can now log in.")
            else:
                st.error("🚫 Username already exists.")

    elif page == "Login":
        st.subheader("Login to Continue")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.page = "main"
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
