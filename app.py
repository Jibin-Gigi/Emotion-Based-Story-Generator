import streamlit as st
import os
import cv2
import numpy as np
from deepface import DeepFace
from langchain.llms import OpenAI

def emotion_detector(image_file):
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    st.image(image, channels="BGR")

    # Save the uploaded image to a temporary file
    temp_file = "temp_image.jpg"
    cv2.imwrite(temp_file, image)

    # Analyze the image using DeepFace
    result = DeepFace.analyze(img_path=temp_file, actions=['emotion'])
    emotion = result[0]['dominant_emotion']

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
        'neutral': 'emotional'
    }
    return opposite_emotions.get(emotion, 'neutral')

# Function to generate story using Langchain
def generate_story(opposite_emotion, api_key, user_name):
    os.environ["OPENAI_API_KEY"] = api_key
    llm = OpenAI(model_name="gpt-3.5-turbo-instruct")
    our_query = f"Write a story that evokes {opposite_emotion} in which the main character's name is {user_name}."
    story = llm(our_query)
    return story

# Main function for Streamlit app
def main():
    st.title("Emotion-Based Story Generator")

    api_key = st.text_input("Enter your OpenAI API key", type="password")
    
    if not api_key:
        st.warning("Please enter your OpenAI API key.")
        return
    
    user_name = st.text_input("Enter your name:")

    st.write('Upload the image of your face, and the app will detect your emotion:')

    image_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if user_name and image_file:
        primary_emotion = emotion_detector(image_file)
        opposite_emotion = get_opposite_emotion(primary_emotion)
        
        st.write(f"Detected Emotion: {primary_emotion}")
        st.write(f"Opposite Emotion: {opposite_emotion}")
        
        story = generate_story(opposite_emotion, api_key, user_name)
        st.write("Here's a story for you:")
        st.write(story)

if __name__ == "__main__":
    main()
