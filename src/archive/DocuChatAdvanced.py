import sys
import os

# Add the root directory to the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import streamlit as st
from tempfile import NamedTemporaryFile
from src.modules.Layout import Layout
from archive.MultiModalRetriever import MultiModalRetrieverAgent
from src.modules.Sidebar import Sidebar
from src.utils.frontend import display, chat_history
from src.utils.openai_models import load_api_key


st.set_page_config(page_title="Advanced Chat")
layout = Layout()
layout.show_header("pdf")

class SimpleBot:
    def __init__(self):
        self.llm, self.embeddings = None, None

    @st.spinner('Setting up conversational chain..')
    def setup_qa_chain_simple(self, file_content):
        if 'processed_data' not in st.session_state:
            agent = MultiModalRetrieverAgent()
            retriever_multi_vector_img, chain_multimodal_rag = agent.process_pdf_advanced(file_content)
            st.session_state['processed_data'] = (retriever_multi_vector_img, chain_multimodal_rag)
        else:
            retriever_multi_vector_img, chain_multimodal_rag = st.session_state['processed_data']
        return retriever_multi_vector_img, chain_multimodal_rag

    @st.spinner('Finding answers..')
    def get_answers(self, chain, user_query):
        result = chain.invoke(user_query)
        return result

    @chat_history
    def main(self):
        sidebar = Sidebar()
        user_api_key = None
        user_api_key = load_api_key()
        if not user_api_key:
            layout.show_api_key_missing()
        else:
            os.environ["OPENAI_API_KEY"] = user_api_key

        sidebar.show_options()
        sidebar.about()

        if user_api_key:
            uploaded_file = st.sidebar.file_uploader(label='Upload PDF files', type=['pdf'], accept_multiple_files=False)
        
            if not uploaded_file:
                st.error("Please upload PDF documents to proceed.")
                st.stop()

            with NamedTemporaryFile(suffix=".pdf") as temp:
                temp.write(uploaded_file.getvalue())

                retriever, qa_chain = self.setup_qa_chain_simple(temp.name)

                user_query = st.chat_input(placeholder="Ask questions on your document!")

                if uploaded_file and user_query:
                    display(user_query, 'user')

                    with st.chat_message("assistant"):
                        result = self.get_answers(qa_chain, user_query)
                        st.write(result)
                        st.session_state.messages.append({"role": "assistant", "content": result})

if __name__ == "__main__":
    obj = SimpleBot()
    obj.main()
