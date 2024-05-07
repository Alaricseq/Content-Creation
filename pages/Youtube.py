import streamlit as st
from Homepage import analyze_image_and_generate_suggestions, get_report_from_gemini
from PIL import Image

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit app layout
def main():
    st.title("YouTube Content Creation")
  
    # Specify creator domain
    domain = st.text_area("Please specify your creator domain:", height=150)
    
    # File uploader for the user to upload an image (optional)
    uploaded_image = st.file_uploader("Upload an image (optional):", type=["jpg", "jpeg", "png"])
    
    # Generate suggestions based on the user's input
    if st.button("Generate Suggestions"):
        if domain:
            suggestion = None
            if uploaded_image:
                image = Image.open(uploaded_image)
                st.image(image, caption="Uploaded Image")
                suggestion = analyze_image_and_generate_suggestions("YouTube", image)
            else:
                suggestion = get_report_from_gemini("YouTube", domain)
                
            if suggestion:
                st.subheader("Suggestions:")
                st.write(suggestion)
                # Append the model's suggestion to chat history
                st.session_state.chat_history.append(suggestion)
            else:
                st.warning("No suggestions available.")
        else:
            st.warning("Please specify your creator domain.")
    
    # Add an input box for the user to type additional prompts
    st.subheader("Ask more questions:")
    additional_prompt = st.text_area("Enter your additional prompt:")

    if st.button("Get Response"):
        if additional_prompt:
            # Concatenate chat history and additional prompt to form a contextual prompt
            contextual_prompt = "\n".join(st.session_state.chat_history + [additional_prompt])

            # Generate response using the AI model with the contextual prompt
            response = get_report_from_gemini("YouTube", contextual_prompt)

            # Display the response
            st.write(f"Response: {response}")

            # Append the model's response to chat history
            st.session_state.chat_history.append(response)

        else:
            st.warning("Please enter a prompt to receive a response.")

if __name__ == "__main__":
    main()
