import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from streamlit import rerun

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Streamlit Config
st.set_page_config(page_title="💬 Anoushaa AI", layout="wide")

# Session Check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠ Please login first from the **Login Page**.")
    st.stop()

# Initialize Session State
if "personalities" not in st.session_state:
    st.session_state.personalities = {
        "Teacher 👩‍🏫": "You are a helpful and patient teacher who explains things clearly.",
        "Friend 😄": "You are a supportive, fun, and casual friend who talks in a friendly tone.",
        "Poet ✨": "You are a poetic soul who answers everything in beautiful poetic style.",
        "Assistant 💼": "You are a professional assistant. Be precise and to the point."
    }

if "history" not in st.session_state:
    st.session_state.history = []

if "current_personality" not in st.session_state:
    st.session_state.current_personality = list(st.session_state.personalities.values())[0]

if "current_personality_name" not in st.session_state:
    st.session_state.current_personality_name = list(st.session_state.personalities.keys())[0]

if "show_custom_form" not in st.session_state:
    st.session_state.show_custom_form = False

# ✅ CSS (Do not change)
st.markdown("""<style>
    html, body, [data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #FBEAFF, #E0F7FF); font-family: 'Segoe UI', sans-serif; color: #333; }
    [data-testid="stSidebar"] { background: #f3e8ff; padding: 20px; }
    .sidebar-title { font-size: 26px; font-weight: 900; text-align: center; background: linear-gradient(to right, #A78BFA, #EC4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 25px; }
    div[role="radiogroup"] > label { background-color:#c3b1ac; border-radius: 10px; font-size: 18px; font-weight: 700; color: #000000 !important; padding: 12px; margin-bottom: 8px; border: 1px solid #c084fc; display: flex; align-items: center; gap: 10px; transition: all 0.3s ease; }
    div[role="radiogroup"] > label:hover { background-color: #ddd6fe; }
    div[role="radiogroup"] > label[data-selected="true"] { background: linear-gradient(to right, #A78BFA, #EC4899); color: #fff !important; font-weight: 800; }
    .main-title { font-size: 46px; font-weight: 900; text-align: center; margin-top: 20px; background: linear-gradient(270deg, #A78BFA, #EC4899, #A78BFA); background-size: 300% 300%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: gradientMove 5s ease infinite; }
    @keyframes gradientMove { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .subtitle { text-align: center; font-size: 20px; color: #666; margin-bottom: 20px; }
    .chat-container { display: flex; flex-direction: column; gap: 12px; margin: auto; width: 60%; margin-top: 20px; }
    .user-bubble, .bot-bubble { padding: 14px 18px; border-radius: 18px; font-size: 16px; box-shadow: 0px 3px 6px rgba(0,0,0,0.1); line-height: 1.5; }
    .user-bubble { background: #E0F2FE; align-self: flex-end; }
    .bot-bubble { background: #F3E8FF; align-self: flex-start; }
    .input-container { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); width: 60%; display: flex; gap: 10px; background: #fff; padding: 10px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .custom-form { margin: 20px auto; width: 60%; background: #fff; padding: 15px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .custom-form h3 { color: #7C3AED; margin-bottom: 10px; }
    .stTextInput > div > div > input, .stTextArea textarea { padding: 14px; font-size: 16px; border-radius: 8px; border: 1px solid #a78bfa; background: white; color: black !important; }
    button:has(span:contains("📨 Send")) { background: linear-gradient(90deg, #A78BFA, #EC4899); color: white !important; font-weight: bold; border-radius: 8px; padding: 10px 16px; border: none; box-shadow: 0 4px 10px rgba(236, 72, 153, 0.3); transition: 0.3s; }
    button:has(span:contains("📨 Send")):hover { background: linear-gradient(90deg, #8B5CF6, #DB2777); }
    button:has(span:contains("🎭 Custom Personality")) { background: #f3f4f6; color: #4B5563; border: 1px solid #d1d5db; font-weight: 600; border-radius: 8px; padding: 10px 16px; transition: 0.3s; }
    button:has(span:contains("🎭 Custom Personality")):hover { background: white; }
    .footer { text-align: center; color: gray; margin-top: 40px; }
</style>""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("<div class='sidebar-title'>🚀 Menu</div>", unsafe_allow_html=True)
if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    rerun()

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.history = []
    st.rerun()

nav_option = st.sidebar.radio("Navigation", ["Home", "Chat", "History", "Settings"])

# Pages
if nav_option == "Home":
    username = st.session_state.get("username", "Guest")
    st.markdown(f"<div class='main-title'>Welcome, {username}!</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Your Smart AI Assistant is ready to help!</div>", unsafe_allow_html=True)

elif nav_option == "Chat":
    st.markdown("<div class='main-title'>💬 Chat with Neura</div>", unsafe_allow_html=True)

    # Show Current Personality
    st.markdown(f"""
    <div style="text-align:center; font-size:18px; color:gray; margin-bottom:10px;">
        Current Personality: <b>{st.session_state.current_personality_name}</b><br>
        <i>{st.session_state.current_personality}</i>
    </div>
    """, unsafe_allow_html=True)

    # Personality Selector
    selected_role = st.sidebar.selectbox("Choose Role:", list(st.session_state.personalities.keys()),
                                         index=list(st.session_state.personalities.keys()).index(st.session_state.current_personality_name))
    if not st.session_state.show_custom_form:
        st.session_state.current_personality = st.session_state.personalities[selected_role]
        st.session_state.current_personality_name = selected_role

    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=st.session_state.current_personality)

    # Chat Display
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for i, msg in enumerate(st.session_state.history):
        role = msg["role"]
        content = msg["parts"][0]
        bubble_class = "user-bubble" if role == "user" else "bot-bubble"
        label = "🧐 You:" if role == "user" else f"🤖 {st.session_state.current_personality_name}:"
        st.markdown(f"<div class='{bubble_class}'>{label} {content}</div>", unsafe_allow_html=True)

    #     # ✅ Quick Replies after last bot response
    #     if role == "model" and i == len(st.session_state.history) - 1:
    #         st.write("**Quick Replies:**")
    #         cols = st.columns(3)
    #         suggestions = ["👍 Great!", "Tell me more", "Can you simplify it?"]
    #         for idx, suggestion in enumerate(suggestions):
    #             if cols[idx].button(suggestion):
    #                 st.session_state.history.append({"role": "user", "parts": [suggestion]})
    #                 st.rerun()

    # st.markdown("</div>", unsafe_allow_html=True)

    # Input Section
    with st.form(key="chat_form", clear_on_submit=True):
        st.markdown("<div class='input-container'>", unsafe_allow_html=True)
        col1, col2 = st.columns([4, 1])
        prompt = col1.text_input("Type your message...", key="chat_input", label_visibility="collapsed")
        send_btn = col2.form_submit_button("📨 Send")
        custom_btn = st.form_submit_button("🎭 Custom Personality", type="secondary")
        st.markdown("</div>", unsafe_allow_html=True)

        if send_btn and prompt.strip():
            st.session_state.history.append({"role": "user", "parts": [prompt]})
            with st.spinner("Thinking..."):
                response = model.generate_content(st.session_state.history)
                reply = response.text
            st.session_state.history.append({"role": "model", "parts": [reply]})
            st.rerun()

        if custom_btn:
            st.session_state.show_custom_form = not st.session_state.show_custom_form

    # Custom Personality Form
    if st.session_state.show_custom_form:
        st.markdown("<div class='custom-form'>", unsafe_allow_html=True)
        st.markdown("<h3>🎭 Create Custom Personality</h3>", unsafe_allow_html=True)
        custom_name = st.text_input("Personality Name:")
        custom_instr = st.text_area("Personality Instructions:")
        save = st.button("✅ Save Personality")
        cancel = st.button("❌ Cancel")

        if save:
            if custom_instr.strip():
                custom_key = custom_name.strip() if custom_name.strip() else f"Custom {len(st.session_state.personalities)+1}"
                st.session_state.personalities[custom_key] = custom_instr
                st.session_state.current_personality = custom_instr
                st.session_state.current_personality_name = custom_key
                st.session_state.show_custom_form = False
                st.success(f"✅ '{custom_key}' added and applied!")
                st.rerun()
            else:
                st.warning("⚠ Please provide instructions.")
        if cancel:
            st.session_state.show_custom_form = False
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

elif nav_option == "History":
    st.markdown("<h2 style='color:#7C3AED;'>🕘 Chat History</h2>", unsafe_allow_html=True)
    if st.session_state.history:
        for msg in st.session_state.history:
            st.write(f"**{msg['role'].capitalize()}:** {msg['parts'][0]}")
        history_text = "\n\n".join(f"{msg['role'].capitalize()}: {msg['parts'][0]}" for msg in st.session_state.history)
        st.download_button("📥 Download Chat", history_text, file_name="anoushaa_chat.txt")
    else:
        st.markdown("<p style='color:black; font-size:18px;'>No chat history yet.</p>", unsafe_allow_html=True)

elif nav_option == "Settings":
    st.markdown("<h2 style='color:#7C3AED;'>⚙️ Settings (Coming Soon)</h2>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>Made with ❤️ by <b>Anoushaa Baig</b></div>", unsafe_allow_html=True)
