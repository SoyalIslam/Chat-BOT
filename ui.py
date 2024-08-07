from dotenv import load_dotenv
import streamlit as st
import time
import os 
import google.generativeai as genai 
from PIL import Image 
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

#Code Main Logic
def get_gemini_response(prompt, uploaded_image):
    model=genai.GenerativeModel('gemini-1.5-flash')
    model2=genai.GenerativeModel('gemini-pro')
    if prompt !="": 
        response=model.generate_content([prompt,uploaded_image])
    elif uploaded_image !="":
        response=model2.generate_content(prompt)
    else:
         response=model.generate_content(uploaded_image)
    return response.text

# Page Title
st.set_page_config(page_title="Chatbot with Login", page_icon=":robot:")

# Function for add chat history
def add_to_chat_history(sender, message):
    st.session_state.chat_history.append((sender, message))

# Function to generate bot response
def generate_bot_response(user_input):
    bot_response = get_gemini_response(prompt=input,uploaded_image=image)
    add_to_chat_history("Bot", bot_response)
    return bot_response

# Function to dynamically update bot response as if it's being typed out
def update_bot_response(response):
    full_response = "Bot: " + response  
    for char_index in full_response.split(" "):
      yield char_index + " "
      time.sleep(0.05)

# Main chat interface
st.title("Hi! Any querys Let me Know I will Solve For You😉")

#CSS
custom_css = """
<style>
.gradient-text {
  background-image: linear-gradient(to right, #73a0ff, #3d5af1);
  color: transparent;
  -webkit-background-clip: text;
  background-clip: text;
  text-fill-color: transparent;
}

.stButton {
  position: relative;
}

.stButton>button:hover {
  font-weight:bold;
  border:none;
  color: #000000;
  background: linear-gradient(to right, #00c6fb , #005bea , #00c6fb);
}

.stButton>button:after {
  content: "";
  position: absolute;
  insert: 0;
  border:none;
  border-radius: inherit;
  background: linear-gradient(to right, #00c6fb 0%, #005bea 0%, #00c6fb 90%);
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
}

.stButton>button:active,
.stButton>button:focus {
  outline: none;
}

.stButton>button:hover:after {
  color:#000000;
  opacity: 1;
}

.stTextArea:hover,
.stTextInput:hover,
.stSelectbox:hover {
  transform: translateY(-2px);
  transition: transform 0.2s ease-in-out;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

if not st.session_state["logged_in"]:
    # Interface image
    image = 'chatbot9103.jpg'
    st.image(image, caption='My Chat Bot', use_column_width=True)

    # Login 
    with st.sidebar:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        if login_button:
            # Authentication
            if username == "Google" and password == "369":
                st.session_state["logged_in"] = True
                st.success("Login successful!")
                st.empty()
            else:
                st.error("Invalid username or password")

if st.session_state["logged_in"]:
# Chat interface 
      user_input = st.text_input("You:", "", help="Type your message here...",key="user_input")
      uploaded_file = st.file_uploader("choose an image ...",type=['jpeg','jpg','png'])
      image=""
        
      if uploaded_file is not None:
        image=Image.open(uploaded_file)
        st.image(image,'Uploaded Image')
      submit_button = st.button(label='Send')
      if user_input.strip() !="" and submit_button:
         user_response=user_input
         add_to_chat_history("You",user_response)
         response=get_gemini_response(prompt=user_input,uploaded_image=image)
         st.write_stream(update_bot_response(response))
        
    # Display chat history 
      st.sidebar.title("Chat History")

    # Side Logo
      logo_image = 'pngtree.png'
      st.sidebar.image(logo_image, caption='''Hi! Am here to Save Records''', use_column_width=True)

      for index, (sender, message) in enumerate(st.session_state.chat_history, start=1):
        st.sidebar.text_area(f"{sender} ({index}):", message, height=len(message) // 2 + 1, max_chars=len(message), key=f"chat_history_{index}")

st.markdown("<h1 class='gradient-text'>Chatbot Interface</h1>", unsafe_allow_html=True)
