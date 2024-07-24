import streamlit as st
import cv2
import numpy as np
from fer import FER
import google.generativeai as genai

def emotion_detector(image_file):
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    st.image(image, channels="BGR")

    # Convert image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize the FER emotion detector
    detector = FER()

    # Detect emotions in the image
    emotions = detector.detect_emotions(rgb_image)

    if emotions:
        # Get the dominant emotion
        emotion, score = detector.top_emotion(rgb_image)
    else:
        emotion = 'No face detected'

    return emotion

# Function to get opposite emotion
def get_opposite_emotion(emotion):
    opposite_emotions = {
        'angry': 'calm',
        'happy': 'sad',
        'sad': 'happy',
        'fear': 'confident',
        'disgust': 'admiration',
        'surprise': 'boredom',
        'neutral': 'emotional',
        'contempt': 'respectful',
        'confused': 'clear-minded',
        'embarrassed': 'proud',
        'No face detected': 'Please provide a clear face image'
    }
    return opposite_emotions.get(emotion, 'neutral')

# Function to generate a story based on the opposite emotion
def generate_story(opposite_emotion, api_key, user_name, max_no_of_words):
    try:
        genai.configure(api_key=api_key)
        prompt = f"Write a simple story that evokes {opposite_emotion} in which the main character's name is {user_name}. The maximum number of words should be {max_no_of_words}."
        model = genai.GenerativeModel('gemini-1.0-pro-latest')
        response = model.generate_content(prompt)
        story = response.text
    except Exception as e:
        st.error(f"Error generating the story: {e}")
        story = None
    
    return story

# Main function for Streamlit app
def main():
    st.title("Emotion-Based Story Generator")

    api_key = st.text_input("Enter your Gemini API key", type="password")
    user_name = st.text_input("Enter your name:")

    if user_name:
        st.write('Upload the image of your face, and the app will detect your emotion:')

        image_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp", "tiff", "webp"])

        if image_file is not None:
            primary_emotion = emotion_detector(image_file)
            opposite_emotion = get_opposite_emotion(primary_emotion)

            st.write(f"Detected Emotion: {primary_emotion}")
            st.write(f"Opposite Emotion: {opposite_emotion}")

            max_no_of_words = st.text_input("Enter the maximum number of words for the story.")

            if st.button('Generate Story'):
                if max_no_of_words.isdigit():
                    story = generate_story(opposite_emotion, api_key, user_name, max_no_of_words)
                    st.write("Here's a story for you:")
                    st.write(story)
                else:
                    st.error("Please enter a valid number for the maximum number of words.")

if __name__ == "__main__":
    main()
