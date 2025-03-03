import streamlit as st
from my_component.component import my_react_component
import streamlit.components.v1 as components


st.title("Streamlit with React")
my_react_component()
components.html("<h1>Hello from basic HTML</h1>", height=100)
