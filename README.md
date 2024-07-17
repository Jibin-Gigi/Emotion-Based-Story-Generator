# Emotion-Based Story Generator

The **Emotion-Based Story Generator** is a Python application that detects emotions from uploaded images and generates personalized stories based on the detected emotion. Whether you're curious about your own emotions or want to explore creative storytelling, this app has you covered!

## Features

- **Emotion Detection:** Upload an image of your face, and the app will analyze it to determine the dominant emotion (e.g., happy, sad, surprised).
- **Story Generation:** Based on the detected emotion, the app generates a short story, based on opposite emotion of the detected one, with you as the main character.

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Jibin-Gigi/Emotion-Based-Story-Generator.git
   cd Emotion-Based-Story-Generator
   ```

2. **Install Dependencies:**
   Make sure you have Python and pip installed. Then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Get Your OpenAI API Key:**
   Sign up for an API key from [OpenAI](https://beta.openai.com/signup/). Copy the API key

4. **Run the App:**
   Execute the following command in your terminal:
   ```bash
   streamlit run app.py
   ```

5. **Use the App:**
   - Enter your OpenAI API key.
   - Provide your name.
   - Upload an image (JPEG or PNG) of your face.
   - The app will detect your emotion and display it along with the opposite emotion.
   - Finally, it will generate a short story for you.

## Contributing

Want to contribute? We welcome pull requests! Here's how you can get involved:
- Fork the repository.
- Create a new branch.
- Make your changes.
- Submit a pull request.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for creating interactive web apps.
- [DeepFace](https://github.com/serengil/deepface) for emotion detection.
- [OpenAI](https://beta.openai.com/) for the powerful GPT-3.5-turbo engine.

## License

This project is licensed under the MIT License.

