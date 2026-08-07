from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from pdf_reader import extract_pdf
from text_extract import extract_text_from_image

def chunk_text():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
        length_function=len,
        seperator="\n\n"
    )
    chunks = text_splitter.split_text()
    print(f"Number of chunks: {len(chunks)}")