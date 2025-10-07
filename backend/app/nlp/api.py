"""
API module for the NLP-based code explanation.

This module provides functions to analyze code using the NLP model and
interface with the Flask API.
"""

import os
from typing import Dict, Any
from .model import ModelManager
from .gemini_analyzer import analyze_code_with_gemini


def analyze_code_nlp(code: str, language: str, model_name: str = None) -> Dict[str, Any]:
    """
    Analyze code using the NLP model.
    
    Args:
        code: The source code to analyze.
        language: The programming language of the code.
        model_name: Optional name of the model to use. If None, uses the default model.
        
    Returns:
        A dictionary containing the explanation and metadata.
    """
    # Check if Gemini model is requested
    if model_name and model_name.lower() in ['gemini', 'gemini-1.5-flash', 'gemini-flash', 'google-gemini']:
        try:
            return analyze_code_with_gemini(code, language)
        except Exception as e:
            return {
                "error": f"Gemini analysis failed: {str(e)}",
                "raw_explanation": "",
                "structured_explanation": {}
            }
    
    # Map language to standardized format
    lang_map = {
        'python': 'python',
        'py': 'python',
        'javascript': 'javascript',
        'js': 'javascript',
        'typescript': 'javascript',
        'ts': 'javascript',
        'java': 'java',
        'c++': 'cpp',
        'cpp': 'cpp',
    }
    
    # Standardize language
    std_language = lang_map.get(language.lower(), language.lower())
    
    # Get the model
    if model_name:
        # Compute the local model path
        model_short_name = model_name.split("/")[-1] if "/" in model_name else model_name
        local_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_models", model_short_name)
        model = ModelManager.get_model(model_name, local_model_path)
    else:
        # Default to Salesforce CodeGen model which is more suitable for generation
        default_model_name = "Salesforce/codegen-350M-mono"
        model_short_name = default_model_name.split("/")[-1]
        local_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_models", model_short_name)
        model = ModelManager.get_model(default_model_name, local_model_path)
    
    # Get the explanation
    result = model.explain_code(code, std_language)
    
    return result


def format_explanation(explanation_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format the explanation result to match the expected output format.
    
    Args:
        explanation_result: The result from analyze_code_nlp.
        
    Returns:
        A dictionary in the format expected by the frontend.
    """
    if "error" in explanation_result:
        return {"error": explanation_result["error"]}
    
    structured = explanation_result.get("structured_explanation", {})
    raw_explanation = explanation_result.get("raw_explanation", "")
    
    # Create a formatted explanation that matches the expected format
    formatted = {
        "summary": structured.get("summary", raw_explanation[:200] if raw_explanation else ""),
        "user_friendly_summary": structured.get("user_friendly_summary", "This code performs programming operations."),
        "details": structured.get("details", ""),
        "full_explanation": structured.get("full_explanation", raw_explanation),
        "raw_explanation": raw_explanation,  # Include raw explanation for debugging
        "functions": [],
        "classes": [],
        "variables": [],
        "imports": [],
        "language": explanation_result.get("language", ""),
        "metadata": {
            "model_used": explanation_result.get("model_used", ""),
            "analysis_type": "nlp"
        }
    }
    
    # Add functions if available
    for func in structured.get("functions", []):
        formatted["functions"].append(func)
    
    # Add classes if available
    for cls in structured.get("classes", []):
        formatted["classes"].append(cls)
    
    # Add variables if available
    for var in structured.get("variables", []):
        formatted["variables"].append(var)
    
    return formatted 