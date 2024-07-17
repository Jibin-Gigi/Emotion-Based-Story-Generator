import streamlit as st
import os
import cv2
import numpy as np
from deepface import DeepFace
import openai

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

# Function to generate story using OpenAI's GPT-3.5-turbo engine
def generate_story(opposite_emotion, api_key, user_name):
    openai.api_key = api_key
    prompt = f"Write a story that evokes {opposite_emotion} in which the main character's name is {user_name}."
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=200
    )
    story = response['choices'][0]['text'].strip()
    return story

# Main function for Streamlit app
def main():
    st.title("Emotion-Based Story Generator")

    api_key = st.text_input("Enter your OpenAI API key", type="password")
    
    if not api_key:
        st.warning("Please enter your OpenAI API key.")
        return
    
    user_name = st.text_input("Enter your name:")

    if user_name:
        st.write('Upload the image of your face, and the app will detect your emotion:')
        
        image_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

        if image_file is not None:
            primary_emotion = emotion_detector(image_file)
            opposite_emotion = get_opposite_emotion(primary_emotion)
            
            st.write(f"Detected Emotion: {primary_emotion}")
            st.write(f"Opposite Emotion: {opposite_emotion}")
            
            story = generate_story(opposite_emotion, api_key, user_name)
            st.write("Here's a story for you:")
            st.write(story)

if __name__ == "__main__":
    main()
