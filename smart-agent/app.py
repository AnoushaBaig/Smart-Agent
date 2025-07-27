# import os
# import streamlit as st
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load .env
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Streamlit Config
# st.set_page_config(page_title="🤖 Semi-Hands-Off Agent", layout="centered")
# st.title("🧠 Smart Gemini Agent (Auto Mode)")
# st.markdown("`No need to set roles — just type, and AI adapts!`")

# # Memory
# if "history" not in st.session_state:
#     st.session_state.history = []

# # Tool: Simple calculator
# def calculator_tool(expression):
#     try:
#         result = eval(expression)
#         return f"🔢 Jawab: {result}"
#     except:
#         return "❌ Mujhe yeh calculation samajh nahi aayi."

# # Classify prompt type
# def detect_personality(prompt):
#     prompt = prompt.lower()
#     if any(word in prompt for word in ["solve", "calculate", "add", "subtract", "+", "-", "*", "/"]):
#         return "calculator"
#     elif any(word in prompt for word in ["kya hai", "explain", "samjhao"]):
#         return "teacher"
#     elif any(word in prompt for word in ["likho", "shayari", "nazm", "ghazal"]):
#         return "poet"
#     else:
#         return "assistant"

# # User input
# prompt = st.text_input("👤 Tumhara sawaal likho:", "")

# if st.button("📨 Send") and prompt:
#     mode = detect_personality(prompt)

#     # Handle calculator tool directly
#     if mode == "calculator":
#         response = calculator_tool(prompt)
#         st.session_state.history.append({"role": "user", "parts": [prompt]})
#         st.session_state.history.append({"role": "tool", "parts": [response]})

#     else:
#         # Set system instruction based on mode
#         if mode == "teacher":
#             instruction = "Tum aik Urdu teacher ho jo asaan zabaan mein samjhaata hai."
#         elif mode == "poet":
#             instruction = "Tum aik Urdu shayar ho jo har baat mein sher-o-shayari karta hai."
#         else:
#             instruction = "Tum aik smart AI assistant ho jo madad karta hai."

#         model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)
#         st.session_state.history.append({"role": "user", "parts": [prompt]})

#         with st.spinner("AI soch raha hai..."):
#             response = model.generate_content(st.session_state.history)
#             reply = response.text

#         st.session_state.history.append({"role": "model", "parts": [reply]})

# # Display chat
# for msg in st.session_state.history:
#     role = msg["role"]
#     if role == "user":
#         st.markdown(f"**🧍 You:** {msg['parts'][0]}")
#     elif role == "tool":
#         st.markdown(f"**🛠️ Tool:** {msg['parts'][0]}")
#     else:
#         st.markdown(f"**🤖 Gemini:** {msg['parts'][0]}")
