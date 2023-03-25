import streamlit as st
from llama_index import GPTSimpleVectorIndex, Document, SimpleDirectoryReader, QuestionAnswerPrompt
import os
import PyPDF2

# Set page title and favicon
favicon = "favicon.ac8d93a.69085235180674d80d902fdc4b848d0b.png"
st.set_page_config(page_title="PDF Indexer", page_icon=favicon)

# Define function to extract text from PDF
def extract_text(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    return text

# Define function to create and save the index
def create_index(index_file):
    # Load the index file
    index = GPTSimpleVectorIndex.load_from_disk(index_file)

    return index

# Create the app layout
st.title("PDF Indexer")

pdf_file = st.file_uploader("Upload a PDF file")

# If a PDF file is uploaded, create and save the index
if pdf_file:
    filename = create_index(pdf_file)
    st.write(filename)
    st.success(f"Index saved to {filename}")


# List all json files in the directory
files = os.listdir('.')
json_files = [f for f in files if f.endswith('.json')]

# Create a dropdown to select the index file
index_file = st.selectbox("Select an index file:", json_files)

# If an index file is selected, create the index
if index_file:
    index = create_index(index_file)
    st.success(f"Index loaded from {index_file}")
else:
    st.warning("No index file selected.")
