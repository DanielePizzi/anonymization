import streamlit.components.v1 as components
import os

# Load built React app
def my_react_component():
    build_dir = os.path.join(os.path.dirname(__file__), "frontend/build")
    index_file = os.path.join(build_dir, "index.html")

    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        return components.html(html_content, height=600)  # Adjust height as needed
    else:
        return "React app not found. Please check the path."