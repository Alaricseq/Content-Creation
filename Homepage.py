import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Your Google API key
API_KEY = "Your API Key"

# Homepage
st.title("Content Creation Portal")

# Brief Explanation
st.header("How it Works:")
st.markdown("""
<span style='color:#afd1c4; font-size:18px;'>1. Enter your prompt to generate content ideas for YouTube or Instagram.</span><br>
<span style='color:#afd1c4; font-size:18px;'>2. Choose the platform you want to create the content for.</span><br>
<span style='color:#afd1c4; font-size:18px;'>3. Access the sidebar to continue exploring options and generating content.</span><br>
""", unsafe_allow_html=True)
# Configure the Gemini model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")


def load_prompt(platform):
    if platform == "YouTube":
        file_path = 'youtube_prompt.txt'
    elif platform == "Instagram":
        file_path = 'instagram_prompt.txt'
    else:
        raise ValueError("Unsupported platform.")

    with open(file_path, 'r') as f:
        prompt = f.read()
    return prompt

# Function to generate content based on domain and platform choice
def get_report_from_gemini(platform, domain):
    # Load the base prompt and append the user input (platform and domain)
    prompt = load_prompt(platform)
    user_prompt = f"{prompt}\n\nPlease provide content creation suggestions for the {platform} platform in the domain of {domain}."
    
    # Generate content using the Gemini model
    report = model.generate_content(user_prompt)
    
    # Extract and return the generated text from the response
    return report.text

# Function to upload an image to the File API
def upload_image_to_file_api(image):
    # Convert the image to bytes
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    # Save the image file as a temporary file
    temp_file_path = "temp_image.png"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(image_bytes.getbuffer())
    
    # Upload the file to the File API
    uploaded_file = genai.upload_file(path=temp_file_path, display_name="Uploaded Image")
    
    # Clean up the temporary file
    import os
    os.remove(temp_file_path)

    return uploaded_file

# Function to analyze an uploaded image and generate suggestions
def analyze_image_and_generate_suggestions(platform, uploaded_image):
    # Upload the image to the File API
    uploaded_file = upload_image_to_file_api(uploaded_image)
    
    prompt = load_prompt(platform)
    # Define the prompt for generating content
    
    # Generate content using the model and uploaded image
    response = model.generate_content([prompt, uploaded_file])

    # Extract and return the response text (content suggestion)
    return response.text
