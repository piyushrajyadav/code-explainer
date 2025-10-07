import re

def analyze_javascript(code):
    """
    Analyze JavaScript code and return a structured explanation.
    """
    try:
        result = {
            "summary": "JavaScript code analysis",
            "details": "",
            "full_explanation": "",
            "functions": [],
            "classes": [],
            "variables": [],
            "imports": [],
            "language": "javascript",
            "metadata": {
                "model_used": "rule-based",
                "analysis_type": "rule"
            }
        }
        
        explanation_parts = []
        
        # Basic analysis
        if re.search(r'function\s+\w+|const\s+\w+\s*=.*=>', code):
            explanation_parts.append("This JavaScript code contains function definitions.")
        
        if re.search(r'class\s+\w+', code):
            explanation_parts.append("This code defines classes.")
        
        if re.search(r'import\s+.*from|require\s*\(', code):
            explanation_parts.append("This code imports modules or dependencies.")
        
        if re.search(r'let\s+|const\s+|var\s+', code):
            explanation_parts.append("This code declares variables.")
        
        if re.search(r'if\s*\(|switch\s*\(', code):
            explanation_parts.append("This code contains conditional logic.")
        
        if re.search(r'for\s*\(|while\s*\(|forEach', code):
            explanation_parts.append("This code contains loops or iterations.")
        
        if not explanation_parts:
            explanation_parts.append("This appears to be a simple JavaScript code snippet.")
        
        full_text = " ".join(explanation_parts)
        result["summary"] = full_text[:200] + "..." if len(full_text) > 200 else full_text
        result["details"] = full_text[200:] if len(full_text) > 200 else ""
        result["full_explanation"] = full_text
        
        return result
        
    except Exception as e:
        return {
            "summary": f"JavaScript analysis error: {str(e)}",
            "details": "An error occurred while analyzing the JavaScript code.",
            "full_explanation": f"Error during analysis: {str(e)}",
            "functions": [],
            "classes": [],
            "variables": [],
            "imports": [],
            "language": "javascript",
            "metadata": {
                "model_used": "rule-based",
                "analysis_type": "rule",
                "error": True
            }
        }
