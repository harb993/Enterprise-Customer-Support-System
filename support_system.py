import os
from typing import List, Dict, Any
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

# Configuration
KNOWLEDGE_BASE_DIR = "knowledge_base"
MODEL_NAME = "qwen2.5:0.5b"
EMBEDDING_MODEL = "nomic-embed-text"

def setup_rag():
    print(f"Initializing RAG system with {EMBEDDING_MODEL}...")
    # 1. Load documents
    loader = DirectoryLoader(KNOWLEDGE_BASE_DIR, glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()
    
    # 2. Chunk documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    
    # 3. Create embeddings and vector store using Ollama
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(texts, embeddings)
    
    return vectorstore.as_retriever()

# --- Specialized Tools ---

def check_warranty(serial_number: str) -> str:
    """Checks the warranty status for a given product serial number."""
    # Simulation logic
    sn = str(serial_number).strip().upper()
    if sn.startswith("SN-X1"):
        return "Warranty Status: ACTIVE. Coverage until Dec 2026."
    elif sn.startswith("SN-HUB"):
        return "Warranty Status: EXPIRED. Please contact support for extension options."
    else:
        return f"Warranty Status: NOT FOUND for {sn}. Please verify the serial number."

def escalate_ticket(issue_details: str) -> str:
    """Escalates a critical issue to a human supervisor."""
    print(f"DEBUG: Escalating issue: {issue_details}")
    return f"Ticket #ESC-{hash(str(issue_details)) % 10000} has been created and assigned to a human supervisor. They will contact you shortly."

# --- Agent Setup ---

def initialize_support_agent():
    retriever = setup_rag()
    
    # Define Tools
    def product_search(query: str) -> str:
        print(f"\n[TOOL] Searching Knowledge Base for: {query}")
        docs = retriever.invoke(str(query))
        res = "\n".join([doc.page_content for doc in docs])
        print(f"[TOOL] Found {len(docs)} relevant chunks.")
        return res

    def check_warranty_tool(serial_number: str) -> str:
        print(f"\n[TOOL] Checking Warranty for: {serial_number}")
        res = check_warranty(serial_number)
        print(f"[TOOL] Result: {res}")
        return res

    tools = [
        Tool(
            name="ProductSearch",
            func=product_search,
            description="Search product manuals and troubleshooting guides. Input: search query."
        ),
        Tool(
            name="WarrantyCheck",
            func=check_warranty_tool,
            description="Check warranty status. Input: product serial number (e.g. SN-X1...)."
        ),
        Tool(
            name="SupervisorEscalation",
            func=escalate_ticket,
            description="Use for critical issues or when human help is requested. Input: issue description."
        )
    ]
    
    # Initialize LLM (Local Qwen 2.5 0.5B)
    llm = ChatOllama(model=MODEL_NAME, temperature=0)
    
    # Setup Memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Simplified ReAct prompt for small models
    template = """You are a helpful Enterprise Support Assistant. 
You have access to tools. Use them only if you cannot answer from memory.

TOOLS:
------
{tools}

To use a tool, you MUST use this exact format:

Thought: Do I need to use a tool? Yes
Action: the action name from [{tool_names}]
Action Input: the input to the action
Observation: the result of the action

When you have the final answer, use this format:

Thought: Do I need to use a tool? No
Final Answer: [your detailed response here]

Begin!

Chat History:
{chat_history}

Question: {input}
{agent_scratchpad}"""

    prompt = PromptTemplate.from_template(template)
    
    # Create the agent
    agent = create_react_agent(llm, tools, prompt)
    
    # Execute
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        memory=memory, 
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=8
    )
    
    return agent_executor

if __name__ == "__main__":
    agent = initialize_support_agent()
    
    print("\n--- Enterprise Support System Online ---")
    print("Welcome! How can I help you today? (Type 'exit' to quit)")
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        try:
            response = agent.invoke({"input": user_input})
            print(f"\nAssistant: {response['output']}")
        except Exception as e:
            print(f"\nError: {str(e)}")
