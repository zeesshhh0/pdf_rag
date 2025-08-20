# 📄 PDF RAG: Intelligent PDF Chat Assistant

**PDF RAG** is a powerful RAG (Retrieval-Augmented Generation) application that allows you to have intelligent conversations with your PDF documents. Simply upload a PDF, and our AI assistant, powered by Google's Gemini models, will answer your questions based on its content.

This project features a modern, decoupled architecture with a **Next.js** frontend, a **FastAPI** backend, and **Supabase** for vector storage and user authentication.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.9+-brightgreen.svg)](https://www.python.org/)
[![Framework: FastAPI](https://img.shields.io/badge/Framework-FastAPI-teal.svg)](https://fastapi.tiangolo.com/)
[![Framework: Next.js](https://img.shields.io/badge/Framework-Next.js-black.svg?logo=next.js)](https://nextjs.org/)

---

### 🚀 Live Demo

*comming soon*

### 🎬 App in Action

*comming soon*

## ✨ Features

-   **Seamless PDF Upload:** Easily upload PDF files through a modern, responsive user interface built with React.
-   **Intelligent Q&A:** Ask complex questions in natural language and get accurate, context-aware answers.
-   **RAG Pipeline:** Utilizes a state-of-the-art Retrieval-Augmented Generation pipeline for high-quality responses.
-   **Powered by Gemini:** Leverages Google's powerful `gemini-pro` for chat generation and `text-embedding-004` for creating vector embeddings.
-   **Secure User Authentication:** Manages users and chat sessions securely with Supabase Auth, integrated via the `supabase-js` library.
-   **Vector Database:** Uses Supabase with the `pgvector` extension for efficient similarity searches.
-   **Scalable Backend:** Built with FastAPI for a high-performance, asynchronous API.
-   **Interactive Frontend:** A clean and performant user interface created with Next.js and React.

## 🛠️ Tech Stack & Architecture

This project uses a decoupled architecture to separate concerns and improve scalability.

-   **Frontend:** [Next.js](https://nextjs.org/) (React Framework)
-   **Backend:** [FastAPI](https://fastapi.tiangolo.com/)
-   **Database & Vector Store:** [Supabase](https://supabase.io/) (PostgreSQL with `pgvector`)
-   **AI Models:** [Google Gemini API](https://ai.google.dev/)
-   **Deployment:** Docker (optional), Vercel, Netlify

### System Architecture
```mermaid
graph TD
    A[User] --> B[Next.js Frontend]
    B --> C[FastAPI Backend]

    %% Authentication & History
    B -->|User Auth (supabase-js)| D[Supabase Auth/DB]
    C -->|Chat History| D

    %% PDF Upload & Embedding
    B -->|Upload PDF| C
    C --> E[Process & Embed Text]
    E -->|Store Vectors| F["Supabase Vector Store - pgvector"]

    %% Question Asking
    B -->|Ask Question| C
    C -->|Query Vectors| F
    F -->|Relevant Context| C

    %% LLM API Call
    C -->|Context + Query| H[Google Gemini API]
    H -->|Generate Response| C

    %% Response back to UI
    C -->|Stream Response| B
```

## ⚙️ Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

-   Python 3.9+ and Pip
-   Node.js 18+ and npm/yarn/pnpm
-   [Git](https://git-scm.com/)
-   A [Supabase](https://supabase.io/) account
-   A [Google AI Studio API Key](https://aistudio.google.com/app/apikey)

### 1. Supabase Project Setup

1.  **Create a New Project:** Go to your Supabase dashboard and create a new project.
2.  **Enable pgvector Extension:** Navigate to `Database` -> `Extensions` and enable `vector`.
3.  **Create a Table:** Go to the `SQL Editor` and run the following script to create a table to store your document chunks and their embeddings.

    ```sql
    -- Create a table for your documents
    create table documents (
      id uuid primary key,
      content text, -- the text chunk
      embedding vector(768), -- embedding vector dimension for Gemini
      metadata jsonb -- optional metadata
    );

    -- Create a function for similarity search
    create or replace function match_documents (
      query_embedding vector(768),
      match_threshold float,
      match_count int
    )
    returns table (
      id uuid,
      content text,
      metadata jsonb,
      similarity float
    )
    language sql stable
    as $$
      select
        documents.id,
        documents.content,
        documents.metadata,
        1 - (documents.embedding <=> query_embedding) as similarity
      from documents
      where 1 - (documents.embedding <=> query_embedding) > match_threshold
      order by documents.embedding <=> query_embedding
      limit match_count;
    $$;
    ```

4.  **Get API Credentials:** Navigate to `Project Settings` -> `API` and copy your **Project URL** and **`anon` public key**. You will need these for the environment variables.

### 2. Local Installation

**A. Clone the Repository**

```bash
git clone [https://github.com/your-username/PDF RAG.git](https://github.com/your-username/PDF RAG.git)
cd PDF RAG
```

**B. Setup the Backend (FastAPI)**

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file from the example
cp .env.example .env
```

Now, edit the `backend/.env` file and add your credentials:

```env
# backend/.env

GOOGLE_API_KEY="your_google_ai_studio_api_key"
SUPABASE_URL="[https://your-project-ref.supabase.co](https://your-project-ref.supabase.co)"
SUPABASE_KEY="your_supabase_anon_public_key"
```

**C. Setup the Frontend (Next.js)**

```bash
# Navigate to the frontend directory from the root
cd frontend

# Install dependencies
npm install

# Create a .env.local file from the example
cp .env.example .env.local
```

Now, edit the `frontend/.env.local` file. You need to add the backend API URL and your public Supabase credentials, which the Next.js client will use for authentication.

```env
# frontend/.env.local

# The URL of your running FastAPI backend
NEXT_PUBLIC_BACKEND_API_URL="[http://127.0.0.1:8000](http://127.0.0.1:8000)"

# Public Supabase credentials for client-side auth
NEXT_PUBLIC_SUPABASE_URL="[https://your-project-ref.supabase.co](https://your-project-ref.supabase.co)"
NEXT_PUBLIC_SUPABASE_ANON_KEY="your_supabase_anon_public_key"
```

### 3. Running the Application

You need to run both the backend and frontend servers in separate terminal windows.

**A. Start the Backend Server**

```bash
# In the /backend directory
uvicorn main:app --reload
```

The FastAPI server will be running at `http://127.0.0.1:8000`.

**B. Start the Frontend Server**

```bash
# In the /frontend directory
npm run dev
```

The Next.js development server will open in your browser at `http://localhost:3000`.

## 🚀 Usage

1.  **Navigate** to the Streamlit app URL in your browser.
2.  **Sign Up / Login** using your email and a password.
3.  **Upload a PDF** file from your local machine.
4.  **Wait** for the application to process and index the document.
5.  **Start Chatting!** Ask questions in the chat input and receive answers based on the document's content.

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1.  **Fork** the repository.
2.  Create a new **branch** (`git checkout -b feature/your-feature-name`).
3.  Make your changes and **commit** them (`git commit -m 'Add some feature'`).
4.  **Push** to the branch (`git push origin feature/your-feature-name`).
5.  Open a **Pull Request**.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.