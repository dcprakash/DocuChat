import os
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from streamlit import logger
import sqlite3

app_logger = logger.get_logger('myapp')
app_logger.info(f"sql lite version {sqlite3.sqlite_version}")
app_logger.info(f"sql lite version {sys.version}")
# Config
st.set_page_config(layout="wide", page_icon="📖", page_title="DocuChat | Chat-Bot 📖")

# Contact
with st.sidebar.expander("📖 Contact"):
    st.write("###### GitHub: [github](https://github.com/dcprakash/DocuChat)")
    st.write("###### Medium: [medium](https://medium.com/@chinvarpd/docuchat-empowering-you-to-explore-and-understand-your-data-effortlessly-part-1-bfd88f5e47d2/)")
    st.write("###### LinkedIn: [linkedin](https://www.linkedin.com/in/chinvar/)")
    st.write("###### Mail: chinvarpd@gmail.com")
    st.write("###### Created by **Darshan Chinvar**")

# Title
st.markdown(
    """
    <h3 style='text-align: center;'>DocuChat, Empowering you to explore and understand your data effortlessly. 📖</h3>
    """,
    unsafe_allow_html=True,
)
st.markdown("---")

# Description
st.markdown(
    """
    <h6 style='text-align: left;'>Welcome to DocuChat! I am an advanced chatbot crafted with the integration of Langchain, Langsmith, Unstructured Loader, ChromaDB, and Streamlit.
    Using sophisticated LLMs, I offer dynamic, context-aware interactions to help you dive deeper into your pdf data.</h6>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

st.markdown(
    """
    <h5 style='text-align: left;'>📖 Explore My App</h5>
    """,
    unsafe_allow_html=True,
)
st.markdown("---")

st.write(
    """
    - **DocuChat**: To create a RAG chain with chat history in-memory, I utilize the create_retrieval_chain and create_history_aware_retriever functions from langchain.chains.
      Additionally, I employ the PyPDFLoader to load the documents, RecursiveCharacterTextSplitter to split them into smaller chunks, and Chroma to index the chunks based on their embeddings.
      It's important to note that this setup does not support answering questions related to images or tables within the PDF documents.
    - **DocuChat-Advanced**: I use [Unstructured Loader](https://unstructured.io/blog/how-to-process-pdf-in-python) to extract text, tables, and images from PDFs, then employ GPT-4o to describe the images and tables.
      Store all extracted and described data in a vector store for efficient retrieval, enabling comprehensive and intelligent query responses.
    """
)
st.markdown("---")

# Contributing
st.markdown(
    """
    <h5 style='text-align: left;'>🤝 Contributing</h5>
    """,
    unsafe_allow_html=True,
)
st.write(
    """
    DocuChat is continually evolving. Your contributions can help enhance its data-awareness and overall capabilities.
    """,
    unsafe_allow_html=True,
)
