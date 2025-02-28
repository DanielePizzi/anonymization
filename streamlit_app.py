import streamlit as st
import io
import tempfile
from PyPDF2 import PdfReader, PdfWriter
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(page_title="Document Comparator", layout="wide")

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# Pagina di caricamento file
if st.session_state.uploaded_file is None:
    st.title("Carica un documento PDF")
    uploaded_file = st.file_uploader("Carica un file PDF", type=["pdf"])
    
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.rerun()
else:
    # Creare un file temporaneo per il PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        tmpfile.write(st.session_state.uploaded_file.read())
        pdf_path = tmpfile.name

    # Pagina di confronto
    st.title("Confronto documenti")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Documento Originale")
        pdf_viewer(pdf_path, key="original_pdf")
    
    with col2:
        st.subheader("Documento Modificato")
        pdf_viewer(pdf_path, key="modified_pdf")
    
    if st.button("Carica un nuovo documento"):
        st.session_state.uploaded_file = None
        st.rerun()
