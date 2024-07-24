FROM python:3.11

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app
WORKDIR /app

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]
