import os
import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from typing import Any
import streamlit as st
from pydantic import BaseModel
from src.utils.openai_models import configure_endpoints
from unstructured.partition.pdf import partition_pdf
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import base64
import requests

class Summarize:
    def __init__(self):
        self.llm, self.embeddings = configure_endpoints()
        self.path = 'images/'
        self.user_api_key = st.session_state.api_key

    @st.spinner('Generating summaries for tables..')
    def generate_table_summaries(self, raw_pdf_elements):
        # Create a dictionary to store counts of each type
        category_counts = {}

        for element in raw_pdf_elements:
            category = str(type(element))
            if category in category_counts:
                category_counts[category] += 1
            else:
                category_counts[category] = 1

        # Unique categories will have unique elements
        unique_categories = set(category_counts.keys())
        category_counts

        class Element(BaseModel):
            type: str
            text: Any

        # Categorize by type
        categorized_elements = []
        for element in raw_pdf_elements:
            if "unstructured.documents.elements.Table" in str(type(element)):
                categorized_elements.append(Element(type="table", text=str(element)))
            elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
                categorized_elements.append(Element(type="text", text=str(element)))

        # Tables
        table_elements = [e for e in categorized_elements if e.type == "table"]
        print(len(table_elements))

        # Text
        text_elements = [e for e in categorized_elements if e.type == "text"]
        print(len(text_elements))

        # Prompt
        prompt_text = """You are an assistant tasked with explaining tables and text.
        If it's a table, extract all elements of the table.
        If it's a graph, explain the findings in the graph. Table, graph or text chunk: {element}"""
        prompt = ChatPromptTemplate.from_template(prompt_text)

        # Summary chain
        # model = AzureChatOpenAI(temperature=0, model="gpt-4")
        summarize_chain = {"element": lambda x: x} | prompt | self.llm | StrOutputParser()

        # Apply to text
        texts = [i.text for i in text_elements]
        text_summaries = texts
        # text_summaries = summarize_chain.batch(texts, {"max_concurrency": 5})

        # Apply to tables
        tables = [i.text for i in table_elements]
        table_summaries = tables
        # table_summaries = summarize_chain.batch(tables, {"max_concurrency": 5})

        return text_summaries, texts, table_summaries, tables

    def encode_image(self, image_path):
        """Getting the base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def gptv_call(self, encoded_image):
        sys_message = """You are financial analyst tasking with providing investment advice. \
        You will be given a mix of text, tables, and image(s) usually of charts or graphs. \
        Use this information to provide investment advice related to the user's question.
        """
        
        user_prompt = """You are an assistant tasked with explaining what is going on in the images.
        If it's a table, extract all elements of the table. If it's a graph, explain the findings in the graph.
        Do not include any numbers that are not mentioned in the image."""

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.user_api_key}",
        }
        # {"role": "system", "content": [{"type": "text", "text": sys_message}]},
        messages = [
            {"role": "system", "content": [{"type": "text", "text": sys_message}]},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
                ],
            },
        ]
        payload = {
            "model": "gpt-4o",
            "messages": messages,
            "temperature": 0.3,
            "top_p": 0.95,
            "max_tokens": 1000,
        }
        # try:
        #     api_url = "https://api.openai.com/v1/chat/completions"
        #     response_content = requests.post(api_url, headers=headers, json=payload)
        #     response_content = response_content.json()
        #     return response_content["choices"][0]["message"]["content"]
        # except Exception as e:
        #     print(f"Failed to call GPT-4 Turbo with Vision API. Error: {e}")
            
        from openai import RateLimitError
        import time
        import random
        
        for attempt in range(5):  # Retry up to 5 times
            try:
                api_url = "https://api.openai.com/v1/chat/completions"
                response = requests.post(api_url, headers=headers, json=payload)
                response_content = response.json()
                return response_content["choices"][0]["message"]["content"]
            except RateLimitError:
                wait_time = (2 ** attempt) + (random.randint(0, 1000) / 1000)
                print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            except Exception as e:
                print(f"Failed to call GPT-4 with Vision API. Error: {e}")
                break

    def image_summarize(self, img_base64):
        """Make image summary"""
        res = self.gptv_call(img_base64)
        return res

    @st.spinner('Generating summaries for images..')
    def generate_img_summaries(self, path):
        """
        Generate summaries and base64 encoded strings for images
        path: Path to list of .jpg files extracted by Unstructured
        """
        # Store base64 encoded images
        img_base64_list = []

        # Store image summaries
        image_summaries = []

        # Apply to images
        for img_file in sorted(os.listdir(path)):
            if img_file.endswith(".jpg"):
                img_path = os.path.join(path, img_file)
                base64_image = self.encode_image(img_path)
                img_base64_list.append(base64_image)
                image_summaries.append(self.image_summarize(base64_image))

        return img_base64_list, image_summaries
