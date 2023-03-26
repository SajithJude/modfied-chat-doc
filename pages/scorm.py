import streamlit as st
import zipfile
import os






# import streamlit as st
import openai 
from llama_index import GPTSimpleVectorIndex, Document, SimpleDirectoryReader,PromptHelper,QuestionAnswerPrompt
import os 
from streamlit_chat import message as st_message

# favicon = "favicon.ac8d93a.69085235180674d80d902fdc4b848d0b.png"
# st.set_page_config(page_title="Flipick Chat", page_icon=favicon)

openai.api_key = os.getenv("API_KEY")


# Define the function to extract the zip file and save the contents to a directory
def extract_zipfile(zip_file, save_directory):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(save_directory)

# Create a file uploader component for the zip file
zip_file = st.file_uploader('Upload a zip file', type='zip')

# If the user uploads a file, extract its contents and save them to a directory
if zip_file is not None:
    # Create a directory for the extracted files
    save_directory = 'scorm'
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Call the extract_zipfile function to extract the zip file and save the contents to the directory
    extract_zipfile(zip_file, save_directory)
    
    # Display a success message
    st.success('Zip file extracted and saved to directory: {}'.format(save_directory))


try:
    index = GPTSimpleVectorIndex.load_from_disk('indx.json')
except FileNotFoundError:
    # Loading from a directory
    documents = SimpleDirectoryReader('scorm').load_data()
    index = GPTSimpleVectorIndex(documents)
    index.save_to_disk('indx.json')

if "history" not in st.session_state:
    st.session_state.history = []

def generate_answer():
    user_message = st.session_state.input_text
    
    if any(op in user_message for op in ['+', '-', '*', '/', '%']):
        st.session_state.history.append({"message": user_message, "is_user": True})
        st.session_state.history.append({"message": "I'm sorry, I'm not allowed to perform calculations.", "is_user": False})
    else:
        query_str = str(user_message)
        context_str = "Generate answers for the questions that are relevant only to the documents context, throw a default answer saying I dont know for unrelevant questions."
        QA_PROMPT_TMPL = (
            "We have provided context information below. \n"
            "---------------------\n"
            "{context_str}"
            "\n---------------------\n"
            "Given this information, please answer the question: {query_str}\n"
        )
        QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)
        message_bot = index.query(query_str, text_qa_template=QA_PROMPT, response_mode="compact", mode="embedding")
        # source = message_bot.get_formatted_sources()
        # st.sidebar.write("Answer Source :",source)  # added line to display source on sidebar
        st.session_state.history.append({"message": user_message, "is_user": True})
        st.session_state.history.append({"message": str(message_bot), "is_user": False})

# col1, col2 = st.columns([1.4, 1])
# col2.image("Flipick_Logo-1.jpg", width=210)
st.write("")
st.write("")

input_text = st.text_input("Ask Chatbot a question", key="input_text", on_change=generate_answer)
# st.caption("Disclaimer : This ChatBOT is a pilot built solely for the purpose of a demo to Indian Institute of Banking and Finance (IIBF). The BOT has been trained based on the book Treasury Management published by IIBF. All content rights vest with IIBF")

# Display the conversation history
for chat in st.session_state.history:
    st_message(**chat)



# # Set up the Streamlit app
# st.title('Zip File Uploader')

