from typing import Any
import streamlit as st
from src.utils.openai_models import configure_endpoints
from utils.summarize import Summarize
from unstructured.partition.pdf import partition_pdf
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores.chroma import Chroma
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryStore
from langchain_core.documents import Document
import uuid
from langchain_core.runnables import RunnablePassthrough

class MultiModalRetrieverAgent:
    def __init__(self):
        self.llm, self.embeddings = configure_endpoints()
        self.summarize = Summarize()
        self.path = 'src/modules/images'

    @st.spinner('Extracting images, tables and text from pdf document..')
    def extract_images(self, files):
        raw_pdf_elements = partition_pdf(
            filename=files,
            # Using pdf format to find embedded image blocks
            extract_images_in_pdf=True,
            # Use layout model (YOLOX) to get bounding boxes (for tables) and find titles
            # Titles are any sub-section of the document
            infer_table_structure=True,
            # Post processing to aggregate text once we have the title
            chunking_strategy="by_title",
            # Chunking params to aggregate text blocks
            # Attempt to create a new chunk 3800 chars
            # Attempt to keep chunks > 2000 chars
            # Hard max on chunks
            max_characters=4000,
            new_after_n_chars=3800,
            combine_text_under_n_chars=2000,
            image_output_dir_path=self.path,
        )
        return raw_pdf_elements

    @st.spinner('Storing data in vector database..')
    def create_multi_vector_retriever(
        self, vectorstore, text_summaries, texts, table_summaries, tables, image_summaries, images
    ):
        """
        Create retriever that indexes summaries, but returns raw images or texts
        """

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

        # Add texts, tables, and images
        # Check that text_summaries is not empty before adding
        if text_summaries:
            add_documents(retriever, text_summaries, texts)
        # Check that table_summaries is not empty before adding
        if table_summaries:
            add_documents(retriever, table_summaries, tables)
        # Check that image_summaries is not empty before adding
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
        return chain

    @st.spinner('Extracting Data for simple Q&A..')
    def process_pdf_advanced(self, file_content):
        raw_pdf_elements = self.extract_images(file_content)
        text_summaries, texts, table_summaries, tables = self.summarize.generate_table_summaries(raw_pdf_elements)
        img_base64_list, image_summaries = self.summarize.generate_img_summaries(self.path)

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
            img_base64_list,
        )

        chain_multimodal_rag = self.multi_modal_rag_chain(retriever_multi_vector_img)
        return retriever_multi_vector_img, chain_multimodal_rag
