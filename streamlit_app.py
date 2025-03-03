import streamlit as st
import tempfile
import os
from streamlit_pdf_viewer import pdf_viewer

# Streamlit app
st.title("PDF Viewer App")

st.write("Upload a PDF file to view it.")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Save uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name  # Get file path
    
    # Display the PDF
    pdf_viewer(temp_path)

    # Optionally, delete the temporary file after displaying
    os.remove(temp_path)
