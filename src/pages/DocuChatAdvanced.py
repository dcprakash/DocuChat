import os
import sys
import platform

# Adjust import for pysqlite3
if platform.system() != 'Darwin':  # 'Darwin' is the system name for macOS
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import glob
import sqlite3
from tempfile import NamedTemporaryFile

import streamlit as st
from streamlit import logger

from src.modules.Layout import Layout
from modules.MultiModalRetriever import MultiModalRetrieverAgent
from src.modules.Sidebar import Sidebar
from src.utils.frontend import display, chat_history
from src.utils.openai_models import load_api_key
from langchain_community.callbacks import get_openai_callback


app_logger = logger.get_logger('myapp')
app_logger.info(f"SQLite version: {sqlite3.sqlite_version}")
app_logger.info(f"Python version: {sys.version}")

st.set_page_config(page_title="Advanced Chat")
layout = Layout()
layout.show_header("pdf")
st.info('Multimodal Retrieval Augmented Generation (RAG) with GPT-4o. It can answer questions on tables or images in pdf')


class SimpleBot:
    def __init__(self):
        self.llm, self.embeddings = None, None
        app_logger.info("Advanced Bot class initialized")

    @st.spinner('Setting up conversational chain..')
    def setup_qa_chain_simple(self, file_content):
        if 'processed_data' not in st.session_state:
            agent = MultiModalRetrieverAgent()
            retriever_multi_vector_img, chain_multimodal_rag = agent.process_pdf_advanced(file_content)
            st.session_state['processed_data'] = (retriever_multi_vector_img, chain_multimodal_rag)
            app_logger.info("Processed data stored in session state")
        else:
            retriever_multi_vector_img, chain_multimodal_rag = st.session_state['processed_data']
            app_logger.info("Processed data retrieved from session state")
        return retriever_multi_vector_img, chain_multimodal_rag

    @st.spinner('Finding answers..')
    def get_answers(self, chain, user_query):
        with get_openai_callback() as cb:
            result = chain.invoke(user_query)
            app_logger.info(f"Answer found for query: {user_query}")
            app_logger.info(f"Total Tokens: {cb.total_tokens}")
            app_logger.info(f"Prompt Tokens: {cb.prompt_tokens}")
            app_logger.info(f"Completion Tokens: {cb.completion_tokens}")
            app_logger.info(f"Total Cost (USD): ${cb.total_cost}")
            return result

    @chat_history
    def main(self):
        sidebar = Sidebar()
        user_api_key = load_api_key()
        if not user_api_key:
            layout.show_api_key_missing()
        else:
            os.environ["OPENAI_API_KEY"] = user_api_key

        sidebar.show_options()
        sidebar.about()

        if user_api_key:
            uploaded_file = st.sidebar.file_uploader(label='Upload PDF files', type=['pdf'], accept_multiple_files=False)
            images_dir = 'src/modules/images'

            if os.path.exists(images_dir):
                files = glob.glob(os.path.join(images_dir, '*'))
                for file in files:
                    if os.path.isfile(file):
                        os.remove(file)
                app_logger.info("All files in the images/ directory have been deleted.")
            else:
                app_logger.info(f"The {images_dir} directory does not exist.")

            if not uploaded_file:
                st.error("Please upload PDF documents to proceed.")
                st.stop()

            with NamedTemporaryFile(suffix=".pdf") as temp:
                temp.write(uploaded_file.getvalue())
                retriever, qa_chain = self.setup_qa_chain_simple(temp.name)
                    
                user_query = st.chat_input(placeholder="Ask questions on your document!")

                if uploaded_file and user_query:
                    display(user_query, 'user')
                    
                    docs = retriever.invoke(user_query, k=10)
                    for doc in docs:
                        app_logger.info(f"Documents: {doc}.")

                    with st.chat_message("assistant"):
                        result = self.get_answers(qa_chain, user_query)
                        st.write(result)
                        st.session_state.messages.append({"role": "assistant", "content": result})


if __name__ == "__main__":
    obj = SimpleBot()
    obj.main()
