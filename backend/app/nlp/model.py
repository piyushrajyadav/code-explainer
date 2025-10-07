"""
NLP Model for Code Explanation.

This module contains classes and functions for loading and using the NLP model
to analyze and explain code across different programming languages.
"""

import os
import torch
import traceback
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import Dict, Any, Optional, Tuple


class CodeExplanationModel:
    """
    Wrapper class for the NLP model that explains code.
    
    This class handles loading the model, preprocessing code, and generating
    explanations using a sequence-to-sequence transformer model.
    """
    
    def __init__(self, model_name: str = "Salesforce/codegen-350M-mono", local_model_path: Optional[str] = None):
        """
        Initialize the model.
        
        Args:
            model_name: The name of the pretrained model to use.
                        Default is "Salesforce/codegen-350M-mono".
            local_model_path: Optional path to locally saved model.
                              If provided, model will be loaded from this path instead.
        """
        self.model_name = model_name
        # Ensure we use the model name's last part (e.g., codegen-350M-mono) as the directory name
        model_short_name = model_name.split("/")[-1] if "/" in model_name else model_name
        self.local_model_path = local_model_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_models", model_short_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = None
        self.model = None
        self.initialized = False
        # Default max length settings - adjust based on model
        if "codebert" in model_name.lower():
            self.max_input_length = 350  # Much more conservative for CodeBERT
            self.max_new_tokens = 50    # Reduced generation length
        else:
            self.max_input_length = 450  # Reduced from 512 to leave room for generation
            self.max_new_tokens = 200
    
    def load_model(self) -> None:
        """
        Load the tokenizer and model.
        
        First attempts to load from local_model_path, falls back to downloading if needed.
        """
        try:
            # Check if model exists locally
            if os.path.exists(self.local_model_path) and os.path.isdir(self.local_model_path):
                print(f"Loading model from local path: {self.local_model_path}")
                try:
                    # Try with local_files_only first
                    self.tokenizer = AutoTokenizer.from_pretrained(
                        self.local_model_path,
                        trust_remote_code=True,
                        local_files_only=True
                    )
                    self.model = AutoModelForCausalLM.from_pretrained(
                        self.local_model_path, 
                        trust_remote_code=True,
                        local_files_only=True
                    ).to(self.device)
                except Exception as e:
                    print(f"Error loading with local_files_only=True: {e}")
                    print("Trying without local_files_only...")
                    self.tokenizer = AutoTokenizer.from_pretrained(
                        self.local_model_path,
                        trust_remote_code=True
                    )
                    self.model = AutoModelForCausalLM.from_pretrained(
                        self.local_model_path, 
                        trust_remote_code=True
                    ).to(self.device)
                print("Model loaded successfully from local path")
            else:
                print(f"Local model path not found: {self.local_model_path}")
                print(f"Downloading model: {self.model_name} to {self.device}")
                
                # Create directory if it doesn't exist
                os.makedirs(self.local_model_path, exist_ok=True)
                
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
                self.model = AutoModelForCausalLM.from_pretrained(self.model_name, trust_remote_code=True).to(self.device)
                
                # Save the model locally
                print(f"Saving model to: {self.local_model_path}")
                self.tokenizer.save_pretrained(self.local_model_path)
                self.model.save_pretrained(self.local_model_path)
                print(f"Model saved to: {self.local_model_path}")
                
            # Set padding token if it doesn't exist
            if self.tokenizer.pad_token is None:
                # First check if there's already a pad token id
                if hasattr(self.tokenizer, 'pad_token_id') and self.tokenizer.pad_token_id is not None:
                    # If pad_token_id exists but pad_token is None, set it
                    self.tokenizer.pad_token = self.tokenizer.convert_ids_to_tokens(self.tokenizer.pad_token_id)
                else:
                    # For CodeBERT/RoBERTa models, don't add new tokens - use EOS instead
                    if "codebert" in self.model_name.lower() or "roberta" in self.model_name.lower():
                        print("Setting EOS token as padding token for CodeBERT/RoBERTa model")
                        self.tokenizer.pad_token = self.tokenizer.eos_token
                    else:
                        # For CodeGen and other models, try to add new padding token
                        try:
                            self.tokenizer.add_special_tokens({'pad_token': '<|pad|>'})
                            # Resize model embeddings to accommodate new token
                            self.model.resize_token_embeddings(len(self.tokenizer))
                            print("Added new padding token: <|pad|>")
                        except:
                            # Fallback to EOS token if adding new token fails
                            print("Setting EOS token as padding token")
                            self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Set bos and eos tokens if they're None
            if self.tokenizer.bos_token is None and self.tokenizer.eos_token is not None:
                self.tokenizer.bos_token = self.tokenizer.eos_token
                
            if self.tokenizer.eos_token is None and self.tokenizer.bos_token is not None:
                self.tokenizer.eos_token = self.tokenizer.bos_token
                
            self.initialized = True
            print("Model initialization complete")
        except Exception as e:
            print(f"Error loading model: {e}")
            print(traceback.format_exc())
            self.initialized = False
    
    def explain_code(self, code: str, language: str) -> Dict[str, Any]:
        """
        Generate an explanation for the provided code.
        
        Args:
            code: The source code to explain.
            language: The programming language of the code.
            
        Returns:
            A dictionary containing the explanation and metadata.
        """
        if not self.initialized:
            print("Model not initialized. Attempting to load...")
            self.load_model()
            
        if not self.initialized:
            print("Failed to initialize model")
            return {"error": "Failed to load NLP model"}
            
        try:
            # Preprocess the code
            preprocessed_code = self._preprocess_code(code, language)
            print(f"Preprocessed code length: {len(preprocessed_code)} chars")
            
            # Tokenize the code
            encoded_input = self.tokenizer(
                preprocessed_code, 
                return_tensors="pt",
                truncation=True, 
                padding=False,
                max_length=self.max_input_length
            ).to(self.device)
            
            input_ids = encoded_input["input_ids"]
            attention_mask = encoded_input.get("attention_mask")
            input_length = input_ids.shape[1]
            print(f"Input sequence length: {input_length} tokens")
            
            # Generate explanation using improved parameters
            print("Generating explanation...")
            with torch.no_grad():
                # Use different parameters based on the model
                if "codebert" in self.model_name.lower():
                    # CodeBERT is not designed for generation, use minimal parameters
                    outputs = self.model.generate(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        max_new_tokens=30,  # Very short for CodeBERT
                        do_sample=False,    # Use greedy decoding
                        pad_token_id=self.tokenizer.pad_token_id,
                        eos_token_id=self.tokenizer.eos_token_id
                    )
                else:
                    # CodeGen with optimized parameters
                    outputs = self.model.generate(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        max_new_tokens=80,  # Focused, shorter responses
                        do_sample=True,
                        top_p=0.85,         # More focused sampling
                        top_k=30,           # Reduced top_k for better quality
                        temperature=0.6,    # Lower temperature for coherence
                        num_return_sequences=1,
                        pad_token_id=self.tokenizer.pad_token_id,
                        eos_token_id=self.tokenizer.eos_token_id,
                        repetition_penalty=1.2,  # Higher penalty to reduce repetition
                        no_repeat_ngram_size=3   # Avoid repeating 3-grams
                    )
            
            # Check if generation worked
            output_length = outputs.shape[1]
            new_tokens = output_length - input_length
            print(f"Output sequence length: {output_length} tokens, new tokens: {new_tokens}")
            
            if new_tokens <= 0:
                print("Warning: No new tokens generated")
                return {"error": "Model did not generate any explanation"}
                
            # Only decode the newly generated tokens, not the input
            explanation = self.tokenizer.decode(
                outputs[0][input_length:], 
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )
            
            # Clean up the explanation
            explanation = self._clean_explanation(explanation)
            
            print(f"Generated explanation length: {len(explanation)} chars")
            print(f"Raw explanation content: {repr(explanation[:200])}")  # Debug: show first 200 chars
            
            # If generated text is empty or very short, return error
            if len(explanation.strip()) < 10:
                print(f"Warning: Generated explanation is too short: '{explanation}'")
                return {"error": "Generated explanation is too short or empty"}
            
            # Parse the explanation into structured format
            structured_explanation = self._structure_explanation(explanation)
            
            return {
                "raw_explanation": explanation,
                "structured_explanation": structured_explanation,
                "language": language,
                "model_used": self.model_name
            }
            
        except Exception as e:
            print(f"Error generating explanation: {str(e)}")
            print(traceback.format_exc())
            return {"error": f"Error generating explanation: {str(e)}"}
    
    def _preprocess_code(self, code: str, language: str) -> str:
        """
        Preprocess the code before sending it to the model.
        
        Args:
            code: The source code to preprocess.
            language: The programming language of the code.
            
        Returns:
            The preprocessed code as a string.
        """
        # If code is longer than 1500 characters, truncate it
        if len(code) > 1500:
            print(f"Code is too long ({len(code)} chars), truncating to 1500 chars")
            code = code[:1500] + "\n# ... code truncated for brevity ...\n"
            
        # Create instruction-based prompts that force natural language explanations
        if "codebert" in self.model_name.lower():
            # Disable CodeBERT for now as it's not working well for generation
            preprocessed = f"""Explain what this code does: {code.strip()[:200]}...
Answer:"""
        else:
            # For CodeGen, use a very simple format that forces explanation
            preprocessed = f"""{language} code:
{code.strip()}

What does this code do?
This code"""
        
        return preprocessed
    
    def _structure_explanation(self, raw_explanation: str) -> Dict[str, Any]:
        """
        Convert the raw model output into a structured explanation.
        
        Args:
            raw_explanation: The raw text generated by the model.
            
        Returns:
            A dictionary containing structured explanation components.
        """
        # Clean up the explanation text
        cleaned_explanation = raw_explanation.strip()
        
        # Split into paragraphs for better structure
        paragraphs = [p.strip() for p in cleaned_explanation.split('\n\n') if p.strip()]
        
        # Create a simple, user-friendly summary
        summary_phrases = [
            "creates", "defines", "implements", "performs", "executes", "handles", "processes",
            "manages", "calculates", "displays", "stores", "retrieves", "sends", "receives"
        ]
        
        # Generate a simple summary
        if len(paragraphs) > 0:
            first_para = paragraphs[0]
            # Try to extract the main action from the first paragraph
            summary = f"This code {first_para.lower()}" if not first_para.lower().startswith('this') else first_para
            
            # Limit summary to first sentence if it's too long
            if len(summary) > 150:
                sentences = summary.split('. ')
                summary = sentences[0] + '.' if sentences else summary[:150] + '...'
                
            # Create details from remaining content
            if len(paragraphs) > 1:
                details = '\n\n'.join(paragraphs[1:])
            else:
                # If only one paragraph, split at natural break points
                sentences = cleaned_explanation.split('. ')
                if len(sentences) > 2:
                    summary = '. '.join(sentences[:2]) + '.'
                    details = '. '.join(sentences[2:])
                else:
                    details = ""
        else:
            summary = "This code performs programming operations."
            details = cleaned_explanation
        
        # Create user-friendly explanation components
        sections = {
            "summary": summary,
            "details": details,
            "full_explanation": cleaned_explanation,
            "user_friendly_summary": self._create_user_friendly_summary(cleaned_explanation),
            "functions": [],
            "classes": [],
            "variables": [],
            "patterns": []
        }
        
        return sections
    
    def _create_user_friendly_summary(self, explanation: str) -> str:
        """Create a simple, user-friendly summary of what the code does."""
        explanation_lower = explanation.lower()
        
        # Common programming patterns and their user-friendly descriptions
        patterns = {
            'function': 'defines functions that can be called to perform specific tasks',
            'class': 'creates classes which are blueprints for objects',
            'variable': 'stores data in variables for later use',
            'loop': 'repeats certain operations multiple times',
            'condition': 'makes decisions based on certain conditions',
            'import': 'brings in external libraries or modules',
            'print': 'displays output or information to the user',
            'input': 'gets information from the user',
            'calculate': 'performs mathematical calculations',
            'process': 'processes or manipulates data',
            'file': 'works with files (reading, writing, or managing)',
            'database': 'interacts with databases to store or retrieve information',
            'api': 'communicates with external services or APIs',
            'web': 'creates web applications or handles web requests'
        }
        
        found_patterns = []
        for pattern, description in patterns.items():
            if pattern in explanation_lower:
                found_patterns.append(description)
        
        if found_patterns:
            if len(found_patterns) == 1:
                return f"In simple terms, this code {found_patterns[0]}."
            elif len(found_patterns) == 2:
                return f"In simple terms, this code {found_patterns[0]} and {found_patterns[1]}."
            else:
                return f"In simple terms, this code {', '.join(found_patterns[:-1])}, and {found_patterns[-1]}."
        else:
            return "In simple terms, this code performs programming operations to accomplish a specific task."
    
    def _clean_explanation(self, explanation: str) -> str:
        """Clean up the generated explanation to remove artifacts and improve quality."""
        import re
        
        if not explanation or len(explanation.strip()) < 5:
            return "creates and defines programming functionality to perform specific tasks"
        
        # Remove common artifacts and clean up
        cleaned = explanation.strip()
        
        # If the explanation is too short or looks like fallback, keep it as is initially
        original_cleaned = cleaned
        
        # Remove problematic patterns but be less aggressive
        cleaned = re.sub(r'will be executed when.*?shell', 'performs operations', cleaned)
        cleaned = re.sub(r'you type.*?command', 'when executed', cleaned)
        cleaned = re.sub(r'print on screen.*?happen', 'displays output', cleaned)
        
        # Only remove these if they're clearly broken
        if 'because we are using' in cleaned and len(cleaned) < 50:
            cleaned = re.sub(r'because we are using.*?purpose', '', cleaned)
        if 'We should use' in cleaned and len(cleaned) < 50:
            cleaned = re.sub(r'We should use.*?statement', '', cleaned)
        
        # Remove trailing fragments only if they're clearly broken
        cleaned = re.sub(r'\binstead so as to avoid.*', '', cleaned)
        cleaned = re.sub(r'\bExample.*$', '', cleaned)
        
        # Clean up spacing
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # If cleaning removed too much meaningful content, use original
        if len(cleaned) < len(original_cleaned) * 0.5 and len(original_cleaned) > 20:
            cleaned = original_cleaned
        
        # If the result is too short or meaningless, provide a targeted fallback
        if len(cleaned) < 15 or len(cleaned.split()) < 3:
            return "creates and defines programming functionality to perform specific tasks"
        
        # Ensure proper sentence structure
        if not cleaned.endswith('.'):
            cleaned += '.'
        
        # Ensure it starts properly - but keep good content
        if not cleaned.lower().startswith(('this', 'the', 'it', 'create', 'define', 'implement', 'perform', 'calcul', 'print', 'display', 'return')):
            if not cleaned.lower().startswith('creates'):
                cleaned = "creates " + cleaned.lower()
        
        return cleaned


class ModelManager:
    """
    Singleton class to manage NLP model instances.
    
    This ensures we only load each model once across the application.
    """
    
    _instances: Dict[str, CodeExplanationModel] = {}
    
    @classmethod
    def get_model(cls, model_name: str = "Salesforce/codegen-350M-mono", local_model_path: Optional[str] = None) -> CodeExplanationModel:
        """
        Get or create a model instance.
        
        Args:
            model_name: The name of the pretrained model to use.
            local_model_path: Optional path to locally saved model.
            
        Returns:
            An instance of CodeExplanationModel.
        """
        if model_name not in cls._instances:
            cls._instances[model_name] = CodeExplanationModel(model_name, local_model_path)
            
        return cls._instances[model_name] 