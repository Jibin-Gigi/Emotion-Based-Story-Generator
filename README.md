# Emotion-to-Character Roleplay Chatbot

This Streamlit app uses Google's Gemini models to create a unique and interactive chat experience. It captures a user's image, infers their emotion and gender, and then generates a chatbot with a persona of the opposite emotion and gender. The user can then engage in a real-time conversation with this AI-driven character.

## Features

  * **Image-based Analysis:** Uses the Gemini Vision model to analyze a user's photo and detect their dominant emotion and gender.
  * **Dynamic Character Creation:** Generates a new chatbot character with a specific backstory, profession, and personality based on the analysis of the user's photo. The character's persona is the opposite of the user's detected emotion and gender.
  * **Engaging Roleplay:** The chatbot is instructed to roleplay as the created character, adhering to specific rules for conversational style and behavior to provide a realistic chat experience.
  * **Secure API Handling:** Uses environment variables (`.env` file) to securely manage the Gemini API key.
  * **Privacy Notice:** The application provides a clear privacy warning, informing users that their image and chat data are sent to the Gemini API for processing and are not stored locally.

## How It Works

1.  **Capture Image:** The user takes a selfie using the built-in camera input.
2.  **Analysis:** The image is sent to the Gemini Vision API, which returns a JSON object containing the detected emotion and gender.
3.  **Character Generation:** The application uses these detections to create a prompt for the Gemini text model. This prompt instructs the model to generate a character with the opposite emotion and gender. The model creates a three-sentence character profile and a detailed set of instructions for the chatbot's persona.
4.  **Chat:** The user chats with the newly created character. The chatbot uses the provided persona instructions and conversation history to generate in-character responses.

## Installation and Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Jibin-Gigi/Emotion-Based-Story-Generator/
    cd Emotion-Based-Story-Generator
    ```
2.  **Create a Virtual Environment (Optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```
3.  **Install Dependencies:**
    The required packages are listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set Up API Key:**
      * Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/).
      * Create a file named `.env` in the root directory of the project.
      * Add your API key to the file in the following format:
        ```
        GEMINI_API_KEY="your_api_key_here"
        ```
5.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```

The application will open in your default web browser.

## Code Structure

  * `app.py`: The main Streamlit application file, containing all the logic for the UI, API calls, and character generation.
  * `.env`: A hidden file for storing the API key securely.
  * `requirements.txt`: A list of all Python libraries needed to run the application.
