from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LLM:
    def __init__(self, model_path=r"local_models\Qwen2.5-Coder-3B-Instruct"):
        print(f"Loading LLM: {model_path}...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path, 
                device_map="auto", 
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            print(f"LLM loaded on {self.device}")
        except Exception as e:
            print(f"Error loading LLM: {e}")
            raise e

        self.history = [
            {"role": "system", "content": "You are a helpful AI assistant that listens to audio discussions and answers questions concisely."}
        ]

    def generate_response(self, user_text):
        if not user_text:
            return ""

        self.history.append({"role": "user", "content": user_text})
        
        text = self.tokenizer.apply_chat_template(
            self.history,
            tokenize=False,
            add_generation_prompt=True
        )
        
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)

        # Generate response (Limited to 256 for speed)
        generated_ids = self.model.generate(
            model_inputs.input_ids,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id # Fix attention mask warning
        )
        
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        self.history.append({"role": "assistant", "content": response})
        return response

    def reload_model(self, model_path):
        import gc
        print(f"Reloading LLM: {model_path}...")
        
        # Reset history on reload to prevent context format issues
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
            
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path, 
                device_map="auto", 
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            print(f"LLM reloaded: {model_path}")
            return True
        except Exception as e:
            print(f"Error reloading LLM: {e}")
            return False
