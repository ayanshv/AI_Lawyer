import streamlit as st
import pypdf
from pdf_reader import extract_pdf
from analyze import analyze_document
from text_extract import extract_text_from_image


logo_path = "RightsAI.png"

st.set_page_config(
  page_title="Rights AI",
  page_icon=logo_path,
  layout="centered",
  initial_sidebar_state="collapsed"
)


if "show_camera" not in st.session_state:
  st.session_state.show_camera = False
if "saved_question" not in st.session_state:
  st.session_state.saved_question = ""
if "analysis_result" not in st.session_state:
  st.session_state.analysis_result = None


st.markdown(
   """
   <style>
  
   @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;600&display=swap');
   @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');


  
   h1, h2, h3 {
       font-family: 'Playfair Display', serif !important;
       color: #1E3A8A;
       margin-bottom: 0.5rem;
   }


  
   [data-testid="stAppViewContainer"] {
       background-color: #FFFFFF !important;
       background-image:
           radial-gradient(circle at 5% 15%, rgba(30, 58, 138, 0.20) 0%, transparent 50%),
           radial-gradient(circle at 95% 75%, rgba(30, 58, 138, 0.15) 0%, transparent 60%) !important;
       background-attachment: fixed !important;
   }


  
   [data-testid="stHeader"] {
       background-color: transparent !important;
   }


  
   .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
       font-family: 'Playfair Display', serif !important;
       font-size: 1.2rem;
       font-weight: 600;
   }


   [data-testid="stFileUploadDropzone"] {
       border-radius: 12px;
       border: 2px dashed #94A3B8;
       background-color: #F8FAFC;
       padding: 2rem;
   }
  
   .stButton > button {
       border-radius: 8px;
   }

   [data-testid="stBottom"] {
       background-color: transparent !important;
   }

   
   [data-testid="stBottom"] > div {
       background: rgba(255, 255, 390, 0.6) !important;
       backdrop-filter: blur(12px) !important;
       -webkit-backdrop-filter: blur(12px) !important;
       border-top: 1px solid rgba(30, 58, 138, 0.1) !important;
   }

   .stTabs [data-baseweb="tab-list"] {
       gap: 8px;
       background-color: #F1F5F9 !important; /* Soft slate gray */
       border-radius: 12px;
       padding: 6px;
       border: none !important;
       display: inline-flex; /* Prevents it from stretching the full width if you don't want it to */
   }

   .stTabs [data-baseweb="tab"] {
       border-radius: 8px !important;
       padding: 10px 24px !important;
       height: auto !important;
       border: none !important;
       background-color: transparent !important;
       color: #64748B !important; /* Muted gray for inactive tabs */
       font-family: 'Inter', sans-serif !important;
       font-weight: 600 !important;
       font-size: 1rem !important;
       transition: all 0.2s ease-in-out !important;
   }

   .stTabs [data-baseweb="tab"]:hover {
       color: #0F172A !important;
       background-color: rgba(0, 0, 0, 0.04) !important;
   }

   .stTabs [aria-selected="true"] {
       background-color: #FFFFFF !important;
       color: #1E3A8A !important; /* Your navy brand color */
       box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
   }
   
   .stTabs [data-baseweb="tab-highlight"] {
       display: none !important;
   }

   @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;600&display=swap');
   @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

   .block-container {
       padding-top: 3rem !important;
       padding-bottom: 6rem !important;
       max-width: 850px !important;
   }

   h1, h2, h3 {
       font-family: 'Playfair Display', serif !important;
       color: #1E3A8A;
       margin-bottom: 0.5rem;
   }

   [data-testid="stAppViewContainer"] {
       background-color: #FFFFFF !important;
       background-image:
           radial-gradient(circle at 5% 15%, rgba(30, 58, 138, 0.20) 0%, transparent 50%),
           radial-gradient(circle at 95% 75%, rgba(30, 58, 138, 0.15) 0%, transparent 60%) !important;
       background-attachment: fixed !important;
   }

   [data-testid="stHeader"] {
       background-color: transparent !important;
   }

   [data-testid="stFileUploadDropzone"] {
       border-radius: 12px;
       border: 2px dashed #94A3B8;
       background-color: #F8FAFC;
       padding: 2rem;
   }
  
   .stButton > button {
       border-radius: 8px;
   }

   [data-testid="stBottom"] {
       background-color: transparent !important;
   }

   [data-testid="stBottom"] > div {
       background: rgba(255, 255, 255, 0.6) !important;
       backdrop-filter: blur(12px) !important;
       -webkit-backdrop-filter: blur(12px) !important;
       border-top: 1px solid rgba(30, 58, 138, 0.1) !important;
   }

   .stTabs [data-baseweb="tab-list"] {
       gap: 8px;
       background-color: #F1F5F9 !important;
       border-radius: 12px;
       padding: 6px;
       border: none !important;
       display: inline-flex;
   }

   .stTabs [data-baseweb="tab"] {
       border-radius: 8px !important;
       padding: 10px 24px !important;
       height: auto !important;
       border: none !important;
       background-color: transparent !important;
       color: #64748B !important;
       font-family: 'Inter', sans-serif !important;
       font-weight: 600 !important;
       font-size: 1rem !important;
       transition: all 0.2s ease-in-out !important;
   }

   .stTabs [data-baseweb="tab"]:hover {
       color: #0F172A !important;
       background-color: rgba(0, 0, 0, 0.04) !important;
   }

   .stTabs [aria-selected="true"] {
       background-color: #FFFFFF !important;
       color: #1E3A8A !important;
       box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
   }
   
   .stTabs [data-baseweb="tab-highlight"] {
       display: none !important;
   }

}
   </style>
   """,
   unsafe_allow_html=True
)

user_question = st.chat_input("What is your inquiry?")
if user_question:
   st.session_state.saved_question = user_question

tab1, tab2 = st.tabs(["Rights", "Why?"])

with tab1:
  
  st.title("_Rights AI_. Your companion in the :yellow[legal] world.")
  st.markdown("Empowering you to understand your documents, one upload at a time.")
 
  st.divider()
  user_language = st.selectbox(
        "What is your preferred language?",
        ("English", "Spanish (Español)", "French (Français)", "Chinese (中文)", "Arabic (العربية)", "Russian (Русский)", "Portuguese (Português)", "Hindi (हिन्दी)", "Bengali (বাংলা)", "Japanese (日本語)", "German (Deutsch)", "Korean (한국어)", "Italian (Italiano)", "Dutch (Nederlands)", "Turkish (Türkçe)", "Vietnamese (Tiếng Việt)", "Polish (Polski)", "Ukrainian (Українська)", "Persian (فارسی)", "Romanian (Română)", "Greek (Ελληνικά)", "Czech (Čeština)", "Swedish (Svenska)", "Hungarian (Magyar)", "Finnish (Suomi)", "Danish (Dansk)", "Norwegian (Norsk)")
        )
  st.divider()
  if user_language:
        st.session_state.saved_question = user_language

  with st.container():
      st.header("Analyze a :yellow[Document]")
      uploaded_pdf = st.file_uploader("Upload your legal document (PDF)", type="pdf")
     
      if uploaded_pdf is not None:
         with st.spinner("Extracting text..."):
            document_info = extract_pdf(uploaded_pdf)   
         if document_info.strip():
            with st.spinner("Analyzing the document..."):
               document_analysis = analyze_document(document_info, user_question, user_language)
               st.success("Analysis Complete")
               st.markdown(document_analysis)
         else:
            st.error("No readable text found in this PDF.")


  st.subheader("OR")
  def open_camera():
     st.session_state.show_camera = True


  st.button("Take a picture of your legal document", on_click=open_camera, type="primary")


  if st.session_state.show_camera:
     uploaded_camera_image = st.camera_input("Capture your document")
     if uploaded_camera_image is not None:
        with st.spinner("Extracting text..."):
           document_info = extract_text_from_image(uploaded_camera_image)
        if document_info.strip():
           with st.spinner("Analyzing the document..."):
              image_analysis = analyze_document(document_info, user_question, user_language)
              st.success("Analysis Complete")
              st.markdown(image_analysis)
        else:
           st.error("No readable text found in this Image")

st.write("---") # Adds a visual divider
  
st.markdown(
      """
      <div style='text-align: center; color: #64748B; margin-bottom: 2rem;'>
          <i class="fa-solid fa-shield-halved"></i> <b>Bank-Grade Security:</b> Your documents are processed securely and are never stored or shared.
      </div>
      """, 
      unsafe_allow_html=True
  )

st.subheader("Not sure where to start?")
st.markdown("Try uploading or snapping a picture of:")
  
colA, colB, colC = st.columns(3)
with colA:
      st.info("**Lease Agreements**\n\nUnderstand your renting rights, deposit terms, and hidden fees.")
with colB:
      st.info("**Employment Contracts**\n\nDecode non-competes, termination clauses, and benefits.")
with colC:
      st.info("**Immigration Forms**\n\nClarify confusing government jargon and next steps.")

st.write("---")


st.subheader("Frequently Asked Questions")
  
with st.expander("How accurate is the AI analysis?"):
   st.write("Our AI is trained on vast amounts of legal data to provide accurate summaries. However, it is an informational companion, not a replacement for a certified lawyer.")
      
with st.expander("Do you save my legal documents?"):
   st.write("No. Your privacy is our top priority. Documents are analyzed in real-time and immediately deleted from our servers once the analysis is complete.")
      
with st.expander("What languages are supported?"):
   st.write("We currently support over 25 languages! Just select your preferred language from the dropdown at the top of the page.")

st.markdown(
      """
      <div style='text-align: center; color: #94A3B8; font-size: 0.8rem; margin-top: 4rem; margin-bottom: 2rem;'>
          © 2026 Rights AI. All rights reserved. <br>
          <i>Disclaimer: Rights AI provides informational insights and does not constitute official legal advice.</i>
      </div>
      """, 
      unsafe_allow_html=True
  )
 
with tab2:
  st.header("About Us")
  st.divider()
 
  col1, col2 = st.columns([1, 1.2], gap="large")
 
  with col1:
      st.image("https://cis.org/sites/default/files/2024-05/Foreign-born-number-percent-social.png", use_container_width=True)
     
  with col2:
      st.markdown("""
      **Navigating the American legal system can be overwhelming**, especially when language barriers stand in the way of justice.
     
      For over 25 million U.S. residents with Limited English Proficiency, a simple misunderstanding of legal documents or complex political jargon can lead to unintended legal trouble and compromised due process.
     
      Our platform bridges this critical gap by empowering you to:
      * **Fully understand** your rights.
      * **Easily decode** complicated legal language.
      * **Confidently plan** your next steps.
     
      No matter your background, we are here to ensure that language is never a barrier to your safety, protection, and peace of mind.
      """)

