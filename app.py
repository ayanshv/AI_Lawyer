import streamlit as st
import pypdf
from pdf_reader import extract_pdf
from analyze import analyze_document
from text_extract import extract_text_from_image

st.set_page_config(
   page_title = "Rights AI",
   layout = "wide"
)


if "show_camera" not in st.session_state:
   st.session_state.show_camera = False
if "saved_question" not in st.session_state:
   st.session_state.saved_question = ""
if "analysis_result" not in st.session_state:
   st.session_state.analysis_result = None




st.title("_Rights AI_. Your companion in the :yellow[legal] world.")


user_question = st.chat_input("What is your inquiry?")
if user_question:
   st.session_state.saved_question = user_question


uploaded_pdf = st.file_uploader("Upload your legal document", type = "pdf")
if uploaded_pdf is not None:
   with st.spinner("Extracting text..."):
       document_info = extract_pdf(uploaded_pdf)


   if document_info.strip():
       with st.spinner("Analyzing the document..."):
           document_analysis = analyze_document(document_info, user_question)
           st.markdown(document_analysis)
   else:
       st.error("No readable text found in this PDF.")


def open_camera():
   st.session_state.show_camera = True


st.button("Take a picture of your legal document", on_click=open_camera)


if st.session_state.show_camera:


   uploaded_camera_image = st.camera_input("Take a picture of your legal document")
   if uploaded_camera_image is not None:
       with st.spinner("Extracting text..."):
           document_info = extract_text_from_image(uploaded_camera_image)


   if document_info.strip():
       with st.spinner("Analyzing the document..."):
               image_analysis = analyze_document(document_info, user_question)
               st.markdown(image_analysis)
   else:
       st.error("No readable text found in this Image")

      