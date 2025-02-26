import streamlit as st
import pandas as pd
import io
from PyPDF2 import PdfReader, PdfWriter
from docx import Document
from streamlit_extras.stylable_container import stylable_container
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import streamlit.components.v1 as components


# Funzione per leggere un file PDF
def read_pdf(file):
    reader = PdfReader(file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

# Funzione per leggere un file Word
def read_docx(file):
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Funzione per generare PDF con formattazione

def create_pdf(text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    content = [Paragraph(text, styles['Normal'])]
    doc.build(content)
    buffer.seek(0)
    return buffer

st.set_page_config(page_title="Document Comparator", layout="wide")

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
    st.session_state.original_text = ""
    st.session_state.modified_text = ""

# Pagina di caricamento file
if st.session_state.uploaded_file is None:
    st.title("Carica un documento")
    uploaded_file = st.file_uploader("Carica un file (PDF o Word)", type=["pdf", "docx"])
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        file_type = uploaded_file.type
        if "pdf" in file_type:
            st.session_state.original_text = read_pdf(uploaded_file)
        else:
            st.session_state.original_text = read_docx(uploaded_file)
        st.session_state.modified_text = st.session_state.original_text
        st.rerun()
else:
    # Pagina di confronto
    st.title("Confronto documenti")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Documento Originale")
        st.text_area("Documento Originale", st.session_state.original_text, height=500, disabled=True, key="original_text_area")
    with col2:
        st.subheader("Modifica il Documento")
        st.session_state.modified_text = st.text_area("Modifica il Documento", st.session_state.modified_text, height=500, key="modified_text_area")
    
    if st.button("Esporta come PDF"):
        pdf_buffer = create_pdf(st.session_state.modified_text)
        st.download_button(
            label="Scarica PDF",
            data=pdf_buffer,
            file_name="documento_modificato.pdf",
            mime="application/pdf"
        )
    
    if st.button("Carica un nuovo documento"):
        st.session_state.uploaded_file = None
        st.session_state.original_text = ""
        st.session_state.modified_text = ""
        st.rerun()
