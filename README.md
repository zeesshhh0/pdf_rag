# PDF RAG Project

This project is a PDF-based question-answering system that uses a Retrieval-Augmented Generation (RAG) architecture to answer questions about a given PDF document.

## Features

* **Chat Interface**: A user-friendly chat interface built with [Chainlit](https://chainlit.io/) to interact with your PDF document.
* **Command-Line Interface**: A command-line interface for querying your PDF document.
* **Google Gemini Models**: Utilizes Google's `gemini-embedding-001` for creating text embeddings and `gemini-2.5-flash` for generating answers.
* **ChromaDB**: Uses [ChromaDB](https.trychroma.com) as the vector store for efficient similarity search.
* **LangChain**: Built with the [LangChain](https://www.langchain.com/) framework for building LLM-powered applications.

## Project Structure

* `app.py`: The main file for the Chainlit chat application.
* `chat_pdf.py`: A script for interacting with the PDF through the command line.
* `create_embeddings.py`: A script to create and store embeddings from the PDF document.
* `pyproject.toml`: The project's dependency file.

## How it Works

The project follows a RAG architecture:

1.  **Load and Split**: The PDF document is loaded and split into smaller chunks.
2.  **Create Embeddings**: Text embeddings are created for each chunk using Google's `gemini-embedding-001` model.
3.  **Store Embeddings**: The embeddings are stored in a ChromaDB vector store.
4.  **User Query**: When a user asks a question, the application creates an embedding for the query.
5.  **Similarity Search**: A similarity search is performed on the vector store to find the most relevant chunks of text from the PDF.
6.  **Generate Answer**: The retrieved text chunks are then passed to the `gemini-2.5-flash` model along with the user's question to generate a human-like answer.

## Getting Started

### Prerequisites

* Python 3.11 or higher
* A Google API key with the "Generative Language API" enabled.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/zeesshhh0/pdf_rag.git
    cd pdf_rag
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r pyproject.toml
    ```

3.  **Set up your environment variables:**

    Create a `.env` file in the root directory and add your Google API key:

    ```
    GOOGLE_API_KEY="your-google-api-key"
    ```

### Usage

**Run the Chat Application**:
  ```bash
  chainlit run app.py -w
  ```

  This will start a local web server, and you can access the chat interface in your browser.


## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.
