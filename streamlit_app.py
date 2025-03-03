import streamlit as st
import io
from docx import Document

st.set_page_config(page_title="Editor & Comparator DOCX", layout="wide")

if "selected_words" not in st.session_state:
    st.session_state.selected_words = []
if "annotations" not in st.session_state:
    st.session_state.annotations = []
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

st.title("Modifica, Annota e Confronta Documenti Word")
st.markdown("Carica un documento Word, seleziona testo, evidenzia, aggiungi annotazioni e confronta i documenti.")

# **Caricamento del file**
uploaded_file = st.file_uploader("Carica un file Word (DOCX)", type=["docx"])

if uploaded_file:
    st.session_state.uploaded_file = uploaded_file

if st.session_state.uploaded_file:
    file_name = st.session_state.uploaded_file.name

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Documento Originale")
        doc = Document(st.session_state.uploaded_file)
        original_text = "\n".join([p.text for p in doc.paragraphs])
        st.text_area("Testo originale", original_text, height=500, disabled=True)
    
    with col2:
        st.subheader("Modifica il Documento")
        modified_text = st.text_area("Modifica il testo", original_text, height=500)

        # **Evidenziazione del testo**
        highlight_word = st.text_input("Inserisci una parola da evidenziare")
        if st.button("Evidenzia Parola"):
            if highlight_word and highlight_word in modified_text:
                st.session_state.selected_words.append(highlight_word)

        st.write("### Parole evidenziate:")
        for word in st.session_state.selected_words:
            st.markdown(f"- 🟡 {word}")

        # **Aggiunta di annotazioni personalizzate**
        annotation_text = st.text_area("Scrivi un'annotazione")
        if st.button("Aggiungi Annotazione"):
            st.session_state.annotations.append(annotation_text)

        st.write("### Annotazioni salvate:")
        for ann in st.session_state.annotations:
            st.markdown(f"- 📌 {ann}")

        # **Salvataggio DOCX modificato**
        if st.button("Esporta documento modificato (Word)"):
            modified_doc = Document()
            for line in modified_text.split("\n"):
                modified_doc.add_paragraph(line)

            doc_buffer = io.BytesIO()
            modified_doc.save(doc_buffer)
            doc_buffer.seek(0)

            st.download_button(
                label="Scarica Documento Word",
                data=doc_buffer,
                file_name="documento_modificato.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

    if st.button("Carica un nuovo documento"):
        st.session_state.uploaded_file = None
        st.session_state.selected_words = []
        st.session_state.annotations = []
        st.experimental_rerun()
