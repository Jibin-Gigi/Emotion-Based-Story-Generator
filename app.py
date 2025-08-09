# filename: app.py
import streamlit as st
import numpy as np
import google.generativeai as genai
import io
import os
import json
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from a .env file.
# The .env file should contain the line: GEMINI_API_KEY="your-api-key"
load_dotenv()

# -----------------------
# Utility: opposite mapping
# -----------------------
OPPOSITE_EMOTION = {
    'angry': 'calm',
    'happy': 'sad',
    'sad': 'happy',
    'fear': 'confident',
    'disgust': 'admiration',
    'surprise': 'boredom',
    'neutral': 'emotional',
    'contempt': 'respectful',
}
OPPOSITE_GENDER = {
    'Man': 'Woman',
    'Woman': 'Man',
    'Other': 'Other' 
}

# -----------------------
# Utility: short character blurb
# -----------------------
def build_brief(profile_text: str, max_len: int = 160) -> str:
    """
    Creates a brief, one-line summary from a multi-line profile text.
    """
    if not profile_text:
        return ""
    # Use the first non-empty line as the brief
    for line in profile_text.splitlines():
        candidate = line.strip()
        if candidate:
            brief = candidate
            break
    else:
        brief = profile_text.strip()
    brief = brief.replace("\n", " ")
    if len(brief) > max_len:
        brief = brief[: max_len - 1].rstrip() + "…"
    return brief


# -----------------------
# Utility: queue user message for processing and clear input on next run
# -----------------------
def queue_user_message():
    message_text = (st.session_state.get('user_input_chat') or '').strip()
    if message_text:
        st.session_state['pending_user_message'] = message_text
        st.session_state['should_clear_input'] = True


# Detection function using Gemini Vision
def analyze_image(img_pil):
    """
    Input: PIL Image (RGB)
    Output: dict with keys: dominant_emotion, gender
    Uses Gemini Vision to infer emotion and gender from the image.
    """
    try:
        buf = io.BytesIO()
        img_pil.save(buf, format="JPEG")
        img_bytes = buf.getvalue()

        prompt = (
            "Look at the person in the photo and infer two things: "
            "1) their dominant emotion as one of: angry, happy, sad, fear, disgust, surprise, neutral, contempt; "
            "2) perceived gender as one of: Man, Woman, Other. "
            "Respond ONLY as compact JSON like {\"emotion\":\"happy\",\"gender\":\"Man\"}."
        )
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        resp = model.generate_content([
            {"mime_type": "image/jpeg", "data": img_bytes},
            prompt,
        ])
        
        text = resp.text.strip()
        # Strip code fences if present
        if text.startswith("```json") and text.endswith("```"):
            text = text[len("```json"): -3].strip()
        
        # Parse JSON
        data = json.loads(text)
        emotion = str(data.get("emotion", "unknown")).lower()
        gender = str(data.get("gender", "unknown"))
        
        return {"dominant_emotion": emotion, "gender": gender, "age": None}
    except Exception as e:
        st.warning(f"Image analysis failed: {e}")
        return {"dominant_emotion": "unknown", "gender": "unknown", "age": None}

# -----------------------
# LLM wrappers (Gemini)
# -----------------------
def configure_genai():
    """Configures the Gemini API using an environment variable."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("Gemini API key not found. Please set it in the .env file.")
        st.stop()
    genai.configure(api_key=api_key)
    st.session_state['genai_configured'] = True

def create_character(person_name, target_gender, target_emotion):
    """
    Asks the LLM to create a character profile and a persona prompt.
    Returns a dict with 'profile_text' and 'persona_prompt'.
    """
    profile_prompt = (
        f"You are a character creator. Your task is to generate a concise character profile. "
        f"The character's name is {person_name}, they are a {target_gender} and should embody the primary emotion '{target_emotion}'. "
        f"The character should be South Indian and their profession should be relevant to their city/region. "
        f"The profile must be exactly **three sentences** long and written in a simple, third-person perspective. "
        f"Sentence 1: State their name, age-range, profession, and city/region. "
        f"Sentence 2: Describe a routine habit and one hobby. "
        f"Sentence 3: Mention their favorite food or music and a personal detail like an important life event or a secret."
    )
    
    try:
        # First call to generate the concise profile
        model = genai.GenerativeModel('gemini-2.5-flash')
        profile_resp = model.generate_content(profile_prompt)
        final_profile = profile_resp.text.strip()

        # Second, more detailed prompt for the chat persona
        persona_prompt_template = (
            f"You will now roleplay as the following character:\n\n{final_profile}\n\n"
            "Your persona is defined by the profile above. Follow these rules strictly for all your responses:\n"
            "1. **Converse Naturally:** Respond like a real person, not a chatbot. Use casual language and realistic sentence structures.\n"
            "2. **Stay In-Character:** Your responses must align with your character's emotion and personality. A sad character speaks less and more thoughtfully, while a happy one might be more talkative.\n"
            "3. **Be Vague with Secrets:** If asked about your secrets or sensitive life events, be evasive. Hint at them without giving direct details.\n"
            "4. **Keep it Concise:** Limit responses to 1-3 sentences to simulate a real conversation.\n"
            "5. **No Stage Directions:** Do not use parentheses, brackets, or any other meta-text to describe your actions or feelings.\n"
            "6. **Acknowledge User:** Respond directly to the user's question or statement without repeating it.\n"
            "7. **Know Your Profession:** You should be knowledgeable about your character's profession and surroundings (e.g., if you are a doctor in Chennai, you know about local hospitals).\n"
        )
        
        return {'profile_text': final_profile, 'persona_prompt': persona_prompt_template}
    except Exception as e:
        st.error(f"Failed to create character: {e}")
        return None

def chat_with_character(persona_prompt, conversation_history, user_message):
    """
    Feeds persona + conversation history + user message to LLM to get a response.
    """
    full_prompt = (
        f"{persona_prompt}\n\n"
        f"Conversation history:\n"
    )
    # Build a single prompt that includes persona + conversation history.
    for role, text in conversation_history[-6:]:  # Use the last few turns
        full_prompt += f"{role}: {text}\n"
    full_prompt += f"User: {user_message}\nCharacter:"
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        resp = model.generate_content(full_prompt)
        return resp.text
    except Exception as e:
        st.error(f"Chat failed: {e}")
        return "Sorry, I couldn't produce a response right now."

# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(page_title="Emotion+Gender → Roleplay Chatbot", layout="centered")
st.title("Emotion-to-Character Roleplay Chatbot")
st.markdown(
    "This app uses a photo to determine your emotion (or you can select it), then creates a chatbot character with the **opposite gender** and **opposite emotion** to roleplay with."
)
st.markdown("⚠️ **Privacy:** Your photo will be sent to the Gemini API for emotion and gender detection. Chat messages are also sent to Gemini. Nothing is saved on this device by the app.")

# Ensure Gemini is configured only once
if 'genai_configured' not in st.session_state:
    configure_genai()

# Camera input
img_file = st.camera_input("Take a selfie 📸")
if img_file is not None:
    # Convert to PIL Image for display and potential analysis
    img_pil = Image.open(io.BytesIO(img_file.getvalue())).convert("RGB")
    st.image(img_pil, caption="Captured image", use_container_width=True)

    # Run analysis (Gemini vision)
    analysis = analyze_image(img_pil)
    primary_emotion = analysis.get('dominant_emotion', 'unknown')
    detected_gender = analysis.get('gender', 'unknown')

    # Emotion result (or manual fallback)
    if primary_emotion == 'unknown':
        primary_emotion = st.selectbox(
            "Select your emotion",
            list(OPPOSITE_EMOTION.keys()),
            index=2, # Default to "sad"
            key='emotion_selectbox'
        )
    st.write(f"Your Emotion: **{primary_emotion}**")

    # Gender selection (manual)
    if detected_gender in ("unknown", None):
        selected_gender = st.selectbox(
            "Your gender (used to create an opposite-gender character)",
            list(OPPOSITE_GENDER.keys()),
            index=0,
            key='gender_selectbox'
        )
    else:
        selected_gender = detected_gender
        st.write(f"Detected Gender: **{selected_gender}**")

    # Determine opposites
    opposite_emotion = OPPOSITE_EMOTION.get(primary_emotion.lower(), 'neutral')
    opposite_gender = OPPOSITE_GENDER.get(selected_gender, 'Other')

    st.write(f"The chatbot character will be a **{opposite_gender}** with a **{opposite_emotion}** demeanor. 🎭")

    # Character name
    char_name = st.text_input("Choose a name for your character:", value="Alex", key='char_name_input')

    if st.button("Create character & start chat"):
        with st.spinner("Creating character..."):
            char_data = create_character(char_name, opposite_gender, opposite_emotion)
        if char_data is not None:
            st.session_state['persona_prompt'] = char_data['persona_prompt']
            st.session_state['char_profile'] = char_data['profile_text']
            st.session_state['char_brief'] = build_brief(char_data['profile_text'])
            st.session_state['conversation'] = [("System", "A new character has been created!")]
            st.session_state['char_name'] = char_name
            st.success("Character created. Start chatting below!")

# Chat interface
if 'persona_prompt' in st.session_state:
    st.subheader(f"Chat with {st.session_state.get('char_name', 'your character')}")
    
    # Display the character profile in a container
    if st.session_state.get('char_profile'):
        with st.container(border=True):
            st.markdown("**Character description:**")
            st.write(st.session_state.get('char_profile', ''))
    
    st.markdown("---")
    
    # Process any pending message and clear input flag BEFORE rendering widgets
    pending_msg = st.session_state.pop('pending_user_message', None)
    if pending_msg:
        st.session_state['conversation'].append(("User", pending_msg))
        response = chat_with_character(
            st.session_state['persona_prompt'],
            st.session_state['conversation'],
            pending_msg,
        )
        st.session_state['conversation'].append(("Character", response))
        # Clear the input value before rerun so the box is empty
        st.session_state['user_input_chat'] = ""
        st.rerun() # Re-run to display the new chat messages
    
    # Display conversation history
    for role, text in (st.session_state.get('conversation') or []):
        if role == "User":
            st.markdown(f"**You:** {text}")
        elif role == "Character":
            st.markdown(f"**{st.session_state.get('char_name', 'Character')}:** {text}")

    user_msg = st.text_input(
        "You:",
        key="user_input_chat",
        on_change=lambda: (
            st.session_state.setdefault('pending_user_message', st.session_state.get('user_input_chat', '').strip())
        ),
    )
    
    send_clicked = st.button("Send", key="send_button")
    if send_clicked and user_msg:
        st.session_state['pending_user_message'] = user_msg
        st.rerun()

# Clear button to remove session data
st.markdown("---")
if st.button("End session & clear data"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.success("Session ended. All data cleared.")
    st.rerun()