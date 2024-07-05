import os
import sys
import platform

# Adjust import for pysqlite3
if platform.system() != 'Darwin':  # 'Darwin' is the system name for macOS
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import uuid
from typing import Any

import streamlit as st
from streamlit import logger
import sqlite3
from src.utils.openai_models import configure_endpoints
from utils.summarize import Summarize
from unstructured.partition.pdf import partition_pdf
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores.chroma import Chroma
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryStore
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough



app_logger = logger.get_logger('myapp')
app_logger.info(f"SQLite version: {sqlite3.sqlite_version}")
app_logger.info(f"Python version: {sys.version}")


class MultiModalRetrieverAgent:
    def __init__(self):
        self.llm, self.embeddings = configure_endpoints()
        self.summarize = Summarize()
        self.path = 'src/modules/images'
        app_logger.info("MultiModalRetrieverAgent class initialized")

    @st.spinner('Extracting images, tables and text from PDF document..')
    def extract_images(self, files):
        raw_pdf_elements = partition_pdf(
            filename=files,
            extract_images_in_pdf=True,
            infer_table_structure=True,
            chunking_strategy="by_title",
            max_characters=4000,
            new_after_n_chars=3800,
            combine_text_under_n_chars=2000,
            extract_image_block_output_dir=self.path,
        )
        app_logger.info("Images, tables, and text extracted from PDF")
        return raw_pdf_elements

    @st.spinner('Storing data in vector database..')
    def create_multi_vector_retriever(
        self, vectorstore, text_summaries, texts, table_summaries, tables, image_summaries, images
    ):
        """
        Create retriever that indexes summaries, but returns raw images or texts
        """
        app_logger.info("Creating multi-vector retriever")
        
        # Initialize the storage layer
        store = InMemoryStore()
        id_key = "doc_id"

        # Create the multi-vector retriever
        retriever = MultiVectorRetriever(
            vectorstore=vectorstore,
            docstore=store,
            id_key=id_key,
        )

        # Helper function to add documents to the vectorstore and docstore
        def add_documents(retriever, doc_summaries, doc_contents):
            doc_ids = [str(uuid.uuid4()) for _ in doc_contents]
            summary_docs = [
                Document(page_content=s, metadata={id_key: doc_ids[i]})
                for i, s in enumerate(doc_summaries)
            ]
            retriever.vectorstore.add_documents(summary_docs)
            retriever.docstore.mset(list(zip(doc_ids, doc_contents)))
            app_logger.info(f"Added {len(doc_contents)} documents to retriever")

        # Add texts, tables, and images
        if text_summaries:
            add_documents(retriever, text_summaries, texts)
        if table_summaries:
            add_documents(retriever, table_summaries, tables)
        if image_summaries:
            add_documents(retriever, image_summaries, images)

        return retriever

    def multi_modal_rag_chain(self, retriever):
        """
        Multi-modal RAG chain
        """
        template = """Answer the question based only on the following context, which can include text, images and tables:
        {context}
        Question: {question}"""
        prompt = ChatPromptTemplate.from_template(template)
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        app_logger.info("Multi-modal RAG chain created")
        return chain

    @st.spinner('Extracting data for simple Q&A..')
    def process_pdf_advanced(self, file_content):
        raw_pdf_elements = self.extract_images(file_content)
        text_summaries, texts, table_summaries, tables = self.summarize.generate_table_summaries(raw_pdf_elements)
        img_base64_list, image_summaries = self.summarize.generate_img_summaries(self.path)
        
        # temporary measure since we dont need to display image back, i also dont want to waste too many tokens
        img_base64_list = ['' for _ in img_base64_list]
        
        # The vectorstore to use to index the summaries
        vectorstore = Chroma(
            collection_name="multi_modal_content", embedding_function=self.embeddings
        )

        # Create retriever
        retriever_multi_vector_img = self.create_multi_vector_retriever(
            vectorstore,
            text_summaries,
            texts,
            table_summaries,
            tables,
            image_summaries,
            img_base64_list
        )

        chain_multimodal_rag = self.multi_modal_rag_chain(retriever_multi_vector_img)
        app_logger.info("PDF processing and advanced Q&A setup complete")
        return retriever_multi_vector_img, chain_multimodal_rag
