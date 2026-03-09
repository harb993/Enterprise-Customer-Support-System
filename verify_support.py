from support_system import initialize_support_agent
import time

def run_tests():
    print("Starting Automated Verification...")
    try:
        print("Initializing agent...")
        agent = initialize_support_agent()
        print("Agent initialized successfully.")
    except Exception as e:
        print(f"FAILED to initialize agent: {e}")
        return
    
    test_cases = [
        {
            "name": "RAG Knowledge Retrieval",
            "input": "What are the technical specifications of the TechGizmo Pro X1?"
        },
        {
            "name": "Warranty Tool Usage",
            "input": "Can you check the warranty for my device? Serial number is SN-X19876."
        },
        {
            "name": "Conversation Memory",
            "input": "When does it expire?"
        },
        {
            "name": "Escalation Tool Usage",
            "input": "I am very unhappy with the device, I want to talk to your boss immediately."
        }
    ]
    
    for test in test_cases:
        print(f"\n--- Testing: {test['name']} ---")
        print(f"User Question: {test['input']}")
        try:
            print("Invoking agent...")
            start_time = time.time()
            response = agent.invoke({"input": test['input']})
            end_time = time.time()
            print(f"Agent Finished. Status: Success.")
            print(f"Assistant Response: {response['output']}")
            print(f"Latency: {end_time - start_time:.2f}s")
        except Exception as e:
            print(f"Error during test '{test['name']}': {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("Verification script started.")
    run_tests()
    print("Verification script finished.")
