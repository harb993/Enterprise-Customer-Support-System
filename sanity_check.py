from langchain_ollama import ChatOllama

def sanity_check():
    print("Starting Sanity Check...")
    try:
        llm = ChatOllama(model="qwen2.5:0.5b")
        print("Invoking LLM...")
        response = llm.invoke("Hello, how are you?")
        print(f"LLM Response: {response.content}")
    except Exception as e:
        print(f"Sanity Check FAILED: {e}")

if __name__ == "__main__":
    sanity_check()
