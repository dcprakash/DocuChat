import os
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


import streamlit as st
from streamlit import logger
import sqlite3

app_logger = logger.get_logger('myapp')
app_logger.info(f"sql lite version {sqlite3.sqlite_version}")
app_logger.info(f"sql lite version {sys.version}")

from tempfile import NamedTemporaryFile
from src.modules.Layout import Layout
from src.modules.ConversationRetriever import ConversationRetrieverAgent
from src.modules.Sidebar import Sidebar
from src.utils.frontend import display, chat_history
from src.utils.openai_models import load_api_key


st.set_page_config(page_title="Simple Chat")
layout = Layout()
layout.show_header("pdf")
st.info('Chat with your documents! It does NOT answer questions on tables or images in pdf, for this release.')

class SimpleBot:
    def __init__(self):
        self.llm, self.embeddings = None, None

    @st.spinner('Setting up conversational chain..')
    def setup_qa_chain_simple(self, files):
        if 'processed_data' not in st.session_state:
            agent = ConversationRetrieverAgent()
            qa_chain = agent.process_pdf_simple(files)
            st.session_state['processed_data'] = qa_chain
        else:
            qa_chain = st.session_state['processed_data']
        return qa_chain

    @st.spinner('Finding answers..')
    def get_answers(self, chain, user_query):
        result = chain.invoke({
            "input": user_query},
            config = {
                "configurable": {"session_id": "abc123"}  # TODO: We dont persist chat, otherwise get all messages belong to the user
            },
        )
        return result

    @chat_history
    def main(self):
        try:
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

                    qa_chain = self.setup_qa_chain_simple(temp.name)

                    user_query = st.chat_input(placeholder="Ask questions on your document!")

                    if uploaded_file and user_query:
                        display(user_query, 'user')

                        with st.chat_message("assistant"):
                            result = self.get_answers(qa_chain, user_query)
                            response = result["answer"]
                            st.write(response)

                            # to show references
                            for idx, doc in enumerate(result['context'], 1):
                                # filename = os.path.basename(doc.metadata['source'])
                                page_num = doc.metadata['page']
                                ref_title = f"{idx}: *page.{page_num}*"
                                with st.popover(ref_title):
                                    st.caption(doc.page_content)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            app_logger.error("An error occurred", exc_info=True)

if __name__ == "__main__":
    obj = SimpleBot()
    obj.main()
