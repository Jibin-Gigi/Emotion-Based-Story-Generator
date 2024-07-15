import streamlit as st
from transformers import pipeline
import os
from langchain.llms import OpenAI

# Initialize emotion detection pipeline
emotion_detector = pipeline('sentiment-analysis', model='bhadresh-savani/distilbert-base-uncased-emotion')

# Function to get opposite emotion
def get_opposite_emotion(emotion):
    opposite_emotions = {
        'anger': 'calm',
        'joy': 'sadness',
        'sadness': 'joy',
        'fear': 'trust',
        'disgust': 'admiration',
        'surprise': 'anticipation'
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
    user_input = None
    
    if user_name:
        user_input = st.text_input(f"{user_name}, How are you feeling today?")
    
    if user_input:
        emotions = emotion_detector(user_input)
        primary_emotion = emotions[0]['label']
        opposite_emotion = get_opposite_emotion(primary_emotion)
        
        st.write(f"Detected Emotion: {primary_emotion}")
        st.write(f"Opposite Emotion: {opposite_emotion}")
        
        story = generate_story(opposite_emotion, api_key, user_name)
        st.write("Here's a story for you:")
        st.write(story)

if __name__ == "__main__":
    main()
