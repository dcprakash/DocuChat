# DocuChat
DocuChat is an advanced chatbot that empowers you to explore and understand your data effortlessly. It integrates Langchain, Langsmith, Unstructured Loader, ChromaDB, and Streamlit to offer dynamic, context-aware interactions for deeper insights into your PDF data.

## Features
- Extracts and analyzes text, tables, and images from PDF documents.
- Uses sophisticated LLMs to provide context-aware responses.
- Supports dynamic interactions through a Streamlit web interface.


## Prerequisites
- Refer to below blogs for details:
- [part-1](https://medium.com/@chinvar/docuchat-empowering-you-to-explore-and-understand-your-data-effortlessly-part-1-bfd88f5e47d2)


## Prerequisites
- Python 3.7 or higher
- [pip](https://pip.pypa.io/en/stable/installation/)

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/dcprakash/DocuChat.git
    cd docuchat
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project directory and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

## Running the Application
To run the application, execute the provided shell script:

```sh
./setup_and_run.sh
```

The application will start, and you can access it in your web browser at `http://localhost:8501`.

## Contributing
Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
Created by **Darshan Chinvar**. Reach out at [chinvarpd@gmail.com](mailto:chinvarpd@gmail.com).

