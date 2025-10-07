"""
Training module for fine-tuning NLP models on code explanation tasks.

This module provides classes and functions for preparing training data,
fine-tuning models, and evaluating their performance.
"""

import os
import json
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from transformers import (
    T5ForConditionalGeneration,
    AutoTokenizer,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
    DataCollatorForSeq2Seq
)
from typing import Dict, Any, List, Tuple, Optional


class CodeExplanationDataset(Dataset):
    """Dataset class for code-explanation pairs."""
    
    def __init__(self, data: List[Dict[str, str]], tokenizer, max_input_length: int = 512, max_target_length: int = 256):
        """
        Initialize the dataset.
        
        Args:
            data: List of dictionaries with 'code' and 'explanation' keys.
            tokenizer: The tokenizer to use.
            max_input_length: Maximum length for input text.
            max_target_length: Maximum length for target text.
        """
        self.data = data
        self.tokenizer = tokenizer
        self.max_input_length = max_input_length
        self.max_target_length = max_target_length
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx) -> Dict[str, torch.Tensor]:
        item = self.data[idx]
        code = item["code"]
        explanation = item["explanation"]
        language = item.get("language", "")
        
        # Preprocess input with language marker
        if language:
            input_text = f"<{language}>\n{code}"
        else:
            input_text = code
            
        input_encodings = self.tokenizer(
            input_text,
            truncation=True,
            max_length=self.max_input_length,
            padding="max_length",
            return_tensors="pt"
        )
        
        target_encodings = self.tokenizer(
            explanation,
            truncation=True,
            max_length=self.max_target_length,
            padding="max_length",
            return_tensors="pt"
        )
        
        input_ids = input_encodings["input_ids"].squeeze()
        attention_mask = input_encodings["attention_mask"].squeeze()
        labels = target_encodings["input_ids"].squeeze()
        labels[labels == self.tokenizer.pad_token_id] = -100  # Replace pad tokens
        
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels
        }


def load_training_data(data_path: str) -> List[Dict[str, str]]:
    """
    Load training data from a JSON file.
    
    Args:
        data_path: Path to the JSON file containing training data.
        
    Returns:
        List of dictionaries with 'code' and 'explanation' keys.
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Training data file not found: {data_path}")
        
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    return data


def train_model(
    model_name: str = "t5-base",
    train_data_path: str = "./training_data.json",
    eval_data_path: Optional[str] = None,
    output_dir: str = "./trained_model",
    num_train_epochs: int = 3,
    batch_size: int = 8,
    learning_rate: float = 5e-5
) -> None:
    """
    Fine-tune a model on code explanation data.
    
    Args:
        model_name: The name of the pretrained model to fine-tune.
        train_data_path: Path to the training data.
        eval_data_path: Optional path to evaluation data.
        output_dir: Directory to save the fine-tuned model.
        num_train_epochs: Number of training epochs.
        batch_size: Training batch size.
        learning_rate: Learning rate for training.
    """
    # Load the model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    
    # Load the data
    train_data = load_training_data(train_data_path)
    eval_data = load_training_data(eval_data_path) if eval_data_path else None
    
    # Create the datasets
    train_dataset = CodeExplanationDataset(train_data, tokenizer)
    eval_dataset = CodeExplanationDataset(eval_data, tokenizer) if eval_data else None
    
    # Set up training arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir=f"{output_dir}/logs",
        logging_steps=100,
        save_total_limit=2,
        learning_rate=learning_rate,
        predict_with_generate=True,
        evaluation_strategy="epoch" if eval_dataset else "no"
    )
    
    # Create a data collator for seq2seq
    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        model=model
    )
    
    # Create the trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator
    )
    
    # Fine-tune the model
    trainer.train()
    
    # Save the model and tokenizer
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    print(f"Model fine-tuning complete. Model saved to {output_dir}")


def prepare_training_data_template():
    """
    Return a template for preparing training data.
    """
    template = [
        {
            "code": "def add(a, b):\n    return a + b",
            "explanation": "This function adds two numbers and returns the result.",
            "language": "python"
        },
        {
            "code": "function calculateTotal(items) {\n    return items.reduce((sum, item) => sum + item.price, 0);\n}",
            "explanation": "This function calculates the total price of items by summing up the price property of each item.",
            "language": "javascript"
        }
    ]
    
    return template 