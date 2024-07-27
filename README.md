# Emotion-Based Story Generator

This Streamlit application is designed to detect the user's emotion from an uploaded image and generate a story based on the opposite emotion using Google's Generative AI API (Gemini). It's a fun way to turn your frown upside down or explore the other side of your current mood!

## Features

- **Emotion Detection**: Upload an image, and the app uses the FER (Facial Emotion Recognition) library to detect your emotion. It's like a mood mirror!
- **Opposite Emotion**: The app identifies the opposite emotion to the detected one—because sometimes it's good to see things from a different perspective.
- **Story Generation**: Based on the opposite emotion, the app crafts a unique story just for you, with a customizable maximum word count. Perfect for a quick read!
- **User Input**: You can input your name, and the app makes you the star of the story. It also requires your API key for generating the story.

## Requirements

- Python 3.x
- streamlit
- opencv-python
- numpy
- fer
- google.generativeai

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Jibin-Gigi/Emotion-Based-Story-Generator.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd Emotion-Based-Story-Generator
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to the URL provided by Streamlit (typically http://localhost:8501).

3. **Enter your Gemini API key** in the provided input field.

4. **Enter your name** in the provided input field.

5. **Upload an image** of your face. A smile is optional, but clarity is important!

6. **Enter the maximum number of words** for the generated story. Keep it short and sweet or go for something epic—it's up to you!

7. **Click "Generate Story"** to receive a story inspired by the opposite of your detected emotion.

## Important Notes

- Make sure your face is clearly visible in the uploaded image for accurate emotion detection. The app isn't great with blurry selfies!
- The `google.generativeai` package requires a valid API key from Google Generative AI (Gemini).
- The FER library is good, but it's not perfect. Sometimes emotions can be a bit tricky to pin down.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://www.streamlit.io/) for the user-friendly interface.
- [FER](https://github.com/justinshenk/fer) for the emotion detection.
- [OpenCV](https://opencv.org/) for image processing.
- [NumPy](https://numpy.org/) for making math a bit more approachable.
- [Google Generative AI](https://cloud.google.com/gen-ai/) for the creative story generation.

## Contributing

Got a fun idea or a clever tweak? Feel free to fork this project and make it even better. Pull requests are always welcome!
