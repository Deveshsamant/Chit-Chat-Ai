from llm import LLM
import time

def test_llm():
    print("Initializing LLM...")
    # By default, it uses the path in llm.py, which is likely the transformers model
    # To test GGUF, verify the path updates in the main app or change default here
    llm = LLM()
    
    prompt = "Hello, tell me a very short joke."
    print(f"\nPrompt: {prompt}")
    
    start = time.time()
    response = llm.generate_response(prompt)
    end = time.time()
    
    print(f"\nResponse: {response}")
    print(f"Total time: {end - start:.2f}s")

if __name__ == "__main__":
    test_llm()
