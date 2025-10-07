#!/usr/bin/env python
"""
Setup script for the NLP code explanation model.

This script handles:
1. Downloading pre-trained models
2. Setting up the environment
3. Running initial model tests
"""

import os
import sys
import torch
import argparse
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import torch
        import transformers
        import numpy
        
        print("✅ All dependencies are installed.")
        print(f"   - PyTorch version: {torch.__version__}")
        print(f"   - Transformers version: {transformers.__version__}")
        print(f"   - CUDA available: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"   - CUDA device: {torch.cuda.get_device_name(0)}")
            
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install all required packages: pip install -r requirements.txt")
        return False

def download_models(model_name, save_path=None, force=False):
    """
    Download the pre-trained model and tokenizer.
    
    Args:
        model_name: Name of the model to download (from Hugging Face)
        save_path: Path to save the model for offline use
        force: If True, re-download even if already exists
    """
    if not save_path:
        # Create default save path in the same directory as this script
        save_path = os.path.join(os.path.dirname(__file__), "saved_models", model_name.split("/")[-1])
    
    print(f"Downloading model: {model_name}")
    print(f"Model will be saved to: {save_path}")
    
    # Check if model already exists at save path
    if os.path.exists(save_path) and not force:
        print(f"✅ Model already exists at {save_path}. Use --force to re-download.")
        print("Testing existing model...")
        
        try:
            # Load the tokenizer and model from saved path
            tokenizer = AutoTokenizer.from_pretrained(save_path)
            
            # Check model type and load accordingly
            if "codegen" in model_name.lower() or "codellama" in model_name.lower():
                model = AutoModelForCausalLM.from_pretrained(save_path)
            else:
                model = AutoModel.from_pretrained(save_path)
                
            print(f"✅ Successfully loaded model from {save_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading saved model: {e}")
            print("Will attempt to re-download...")
    
    try:
        # Download tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        print(f"✅ Tokenizer downloaded: {model_name}")
        
        # Download model based on type
        if "codegen" in model_name.lower() or "codellama" in model_name.lower():
            model = AutoModelForCausalLM.from_pretrained(model_name)
        else:
            model = AutoModel.from_pretrained(model_name)
            
        print(f"✅ Model downloaded: {model_name}")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save model and tokenizer
        print(f"Saving model to {save_path} for offline use...")
        model.save_pretrained(save_path)
        tokenizer.save_pretrained(save_path)
        print(f"✅ Model saved to {save_path}")
        
        # Simple test
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = model.to(device)
        
        test_input = "def add(a, b):\n    return a + b"
        inputs = tokenizer(test_input, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model(**inputs)
            
        print("\nTest inference:")
        print(f"Input: {test_input}")
        print(f"Output shape: {outputs.last_hidden_state.shape if hasattr(outputs, 'last_hidden_state') else 'N/A'}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to download model: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Setup NLP model for code explanation")
    parser.add_argument("--model", default="Salesforce/codegen-350M-mono", 
                        help="Model name to download")
    parser.add_argument("--save-path", 
                        help="Path to save the model for offline use")
    parser.add_argument("--force", action="store_true", 
                        help="Force re-download of models even if they exist")
    args = parser.parse_args()
    
    print("=" * 50)
    print("NLP Code Explanation Model Setup")
    print("=" * 50)
    
    if not check_dependencies():
        sys.exit(1)
    
    if download_models(args.model, args.save_path, args.force):
        print("\n✅ Setup completed successfully!")
        print("You can now use the model offline without internet connection.")
        print(f"The model is saved at: {args.save_path or os.path.join(os.path.dirname(__file__), 'saved_models', args.model.split('/')[-1])}")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 