import streamlit as st
import fitz  # PyMuPDF
from io import BytesIO

def load_pdf(file):
    return fitz.open(stream=file.read(), filetype="pdf")

def save_pdf(doc):
    pdf_bytes = BytesIO()
    doc.save(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes

def add_freetext_annotation(doc, page_number, x, y, new_text):
    doc = fitz.open("pdf", save_pdf(doc).getvalue())
    page = doc[page_number]
    page.insert_textbox(
        rect=(x, y, x + 100, y + 20),
        buffer=new_text,
        fontsize=12,
        color=(0, 0, 0),
        fill=(1, 1, 1)
    )
    return doc

def add_redaction(doc, page_number, x, y, width, height):
    doc = fitz.open("pdf", save_pdf(doc).getvalue())
    page = doc[page_number]
    rect = fitz.Rect(x, y, x + width, y + height)
    page.add_redact_annot(rect, fill=(0, 0, 0))
    page.apply_redactions()
    return doc

def main():
    if "doc" not in st.session_state:
        st.session_state["doc"] = None
    st.title("PDF Editor con PyMuPDF")
    uploaded_file = st.file_uploader("Carica un PDF", type="pdf")

    if uploaded_file:
        if st.session_state["doc"] is None:
            st.session_state["doc"] = load_pdf(uploaded_file)
        page_number = st.number_input("Numero pagina", min_value=0, max_value=len(doc)-1, value=0)

        option = st.radio("Azione da eseguire", ("Modifica Testo", "Oscura Testo"))

        x = st.number_input("Posizione X", min_value=0)
        y = st.number_input("Posizione Y", min_value=0)

        if option == "Modifica Testo":
            new_text = st.text_input("Testo da inserire")
            if st.button("Modifica testo"):
                st.session_state["doc"] = add_freetext_annotation(st.session_state["doc"], page_number, x, y, new_text)
                st.rerun()

        elif option == "Oscura Testo":
            width = st.number_input("Larghezza", min_value=1)
            height = st.number_input("Altezza", min_value=1)
            if st.button("Oscura area selezionata"):
                st.session_state["doc"] = add_redaction(st.session_state["doc"], page_number, x, y, width, height)
                st.rerun()

        st.write("Anteprima della pagina:")
        page = st.session_state["doc"][page_number]
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")
        st.image(img_bytes, caption=f"Pagina {page_number}", use_column_width=True)

        st.write("### Scarica il PDF modificato")
        modified_pdf = save_pdf(st.session_state["doc"])
        st.download_button("Scarica PDF", modified_pdf, "pdf_modificato.pdf", "application/pdf")

if __name__ == "__main__":
    main()
