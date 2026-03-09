# Enterprise Customer Support System

## Overview
This system is an AI-powered support agent designed to handle technical inquiries, warranty validations, and issue escalations for an enterprise environment. It utilizes Retrieval-Augmented Generation (RAG) to provide accurate answers based on localized product documentation.

## Technical Architecture
The system is built with a decoupled architecture consisting of a backend API and a dynamic web frontend.

### Backend
- Framework: FastAPI
- Orchestration: LangChain
- Model: Qwen 2.5 0.5B (Local via Ollama)
- Vector Store: FAISS
- Embeddings: nomic-embed-text (Local via Ollama)
- Memory: ConversationBufferMemory for context retention

### Frontend
- Framework: React (v18)
- Build Tool: Vite
- Icons: Lucide React
- Styling: Custom Vanilla CSS

## Core Features
- Product Knowledge Search: Retrieves technical specifications and setup guides from the markdown-based knowledge base.
- Warranty Validation: Checks the status of product serial numbers through a specialized tool.
- Issue Escalation: Automatically generates a support ticket and notifies a supervisor for critical issues or explicit requests.
- Multi-turn Interaction: Retains chat history to understand follow-up questions.

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- Node.js and npm
- Ollama (running qwen2.5:0.5b and nomic-embed-text)

### Installation
1. Install Python dependencies:
   ```bash
   pip install fastapi uvicorn langchain langchain-ollama faiss-cpu langchain-community
   ```
2. Install Frontend dependencies:
   ```bash
   cd frontend && npm install
   ```

### Running the Application
1. Start the FastAPI server:
   ```bash
   python app.py
   ```
2. The application will be accessible at http://localhost:8000.
