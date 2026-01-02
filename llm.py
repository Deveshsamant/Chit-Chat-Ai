from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time
import os
import sys
import threading

# Force Absolute Path for finding local resources
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    from llama_cpp import Llama
    HAS_LLAMA_CPP = True
except ImportError:
    HAS_LLAMA_CPP = False
    print("Warning: llama_cpp not installed. GGUF models will not work.")

class LLM:
    def __init__(self, model_path=r"local_models\qwen2.5-coder-3b-instruct-q4_k_m.gguf"):
        # Resolve absolute path
        if not os.path.isabs(model_path):
            self.model_path = os.path.join(BASE_DIR, model_path)
        else:
            self.model_path = model_path
            
        print(f"[LLM] Loading LLM from: {self.model_path}")
        
        if not os.path.exists(self.model_path):
            print(f"Error: Model file not found at {self.model_path}")
            # List directory to help debug
            folder = os.path.dirname(self.model_path)
            if os.path.exists(folder):
                print(f"Contents of {folder}: {os.listdir(folder)}")
            else:
                print(f"Folder {folder} does not exist.")
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_type = "transformers"
        
        # Check if it's a GGUF model
        if self.model_path.lower().endswith(".gguf"):
            if HAS_LLAMA_CPP:
                print("Detected GGUF model. Using llama_cpp for high performance.")
                self.model_type = "llama_cpp"
                try:
                    self.model = Llama(
                        model_path=self.model_path,
                        n_gpu_layers=-1, # Offload all layers to GPU
                        n_ctx=2048,      # Context window
                        verbose=False
                    )
                    print(f"LLM (GGUF) loaded on {self.device}")
                except Exception as e:
                    print(f"Error loading GGUF model: {e}")
                    raise e
            else:
                print("Error: GGUF model detected but llama_cpp is not installed.")
                raise ImportError("Please install llama-cpp-python to use GGUF models.")
        else:
            # Fallback to transformers
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_path, 
                    device_map="auto", 
                    trust_remote_code=True,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
                )
                print(f"LLM (Transformers) loaded on {self.device}")
            except Exception as e:
                print(f"Error loading LLM: {e}")
                raise e

        self.history = [
            {"role": "system", "content": "You are a code-generator. \nRULES:\n1. NO conversational text. NO 'Certainly', 'Here is the code', 'Below is', NO conclusions.\n2. Start immediately with the code block.\n3. After the code, provide a Time and Space Complexity analysis.\n4. FORMAT:\n```language\n<code>\n```\n### Complexity\nTime: O(...)\nSpace: O(...)"}
        ]

    def generate_response(self, user_text, stream_callback=None):
        if not user_text:
            return ""

        self.history.append({"role": "user", "content": user_text})
        
        print(f"[LLM] Generating response...")
        start_time = time.time()
        response = ""
        
        if self.model_type == "llama_cpp":
            # Llama.cpp generation
            stream = self.model.create_chat_completion(
                messages=self.history,
                max_tokens=1024,
                temperature=0.7,
                stream=True
            )
            
            print("[LLM] Stream: ", end="", flush=True)
            for chunk in stream:
                if 'content' in chunk['choices'][0]['delta']:
                    token = chunk['choices'][0]['delta']['content']
                    print(token, end="", flush=True)
                    response += token
                    if stream_callback:
                        stream_callback(token)
            print() # Newline after stream
            
        else:
            # Transformers generation (Streaming with TextIteratorStreamer)
            from transformers import TextIteratorStreamer
            streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
            
            text = self.tokenizer.apply_chat_template(
                self.history,
                tokenize=False,
                add_generation_prompt=True
            )
            
            model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)

            generation_kwargs = dict(
                inputs=model_inputs.input_ids,
                max_new_tokens=1024,
                do_sample=True,
                temperature=0.7,
                attention_mask=model_inputs.attention_mask,
                pad_token_id=self.tokenizer.eos_token_id,
                streamer=streamer
            )

            # Run generation in a separate thread so we can iterate streamer
            thread = threading.Thread(target=self.model.generate, kwargs=generation_kwargs)
            thread.start()

            print("[LLM] Stream: ", end="", flush=True)
            for token in streamer:
                print(token, end="", flush=True)
                response += token
                if stream_callback:
                    stream_callback(token)
            
            thread.join()
            print() # Newline

        end_time = time.time()
        duration = end_time - start_time
        
        # Estimate TPS (Tokens Per Second)
        # Note: simplistic token count for stats
        num_tokens = len(response.split()) * 1.3 # Rough estimate
        tps = num_tokens / duration if duration > 0 else 0
        print(f"[LLM] Finished in {duration:.2f}s (~{tps:.2f} t/s)")
        
        self.history.append({"role": "assistant", "content": response})
        return response

    def reload_model(self, model_path):
        import gc
        print(f"Reloading LLM: {model_path}...")
        
        # Reset history
        self.history = [
            {"role": "system", "content": "You are a helpful AI assistant. Answer concisely."}
        ]
        
        # Clean up old model
        if hasattr(self, 'model'):
            del self.model
        if hasattr(self, 'tokenizer'):
            del self.tokenizer
            
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            
        return self.__init__(model_path) # Re-init with new path logic
