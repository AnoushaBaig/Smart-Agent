import streamlit as st
import base64

# ------------ Set Page Config ------------
st.set_page_config(page_title="Login | Anoushaa AI", layout="centered")

# ------------ Optional: Use Your Own Background Image (encoded) ------------
def set_bg_from_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ✅ Set image as background (replace with your actual image path if needed)
set_bg_from_image("bg.jpeg")  # Your uploaded image

# ------------ Glassmorphic Style ------------
st.markdown("""
    <style>
    .login-title {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 30px;
    }
    input, .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid #ffffff50;
        border-radius: 8px;
    }
    .login-btn button {
        background-color: #ec38bc !important;
        border: none;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
    }
    .forgot {
        font-size: 12px;
        margin-top: 10px;
    }
    .forgot a {
        color: #fff;
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# ------------ Session State Init ------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ------------ Redirect If Logged In ------------
if st.session_state.logged_in:
    st.switch_page("pages/chatbot.py")

# ------------ Login Form ------------
with st.container():
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">LOGIN</div>', unsafe_allow_html=True)

    username = st.text_input("Username", key="user")
    password = st.text_input("Password", type="password", key="pass")

    login = st.button("SIGN IN", use_container_width=True)
    if login:
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"✅ Logged in as {username}")
            st.switch_page("pages/chatbot.py")
        else:
            st.error("❌ Please enter both username and password.")

    st.markdown('<div class="forgot">Forgot password? <a href="#">Click here</a></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
