import re

def analyze_java(code):
    """
    Analyze Java code and return a structured explanation.
    """
    try:
        result = {
            "summary": "Java code analysis",
            "details": "",
            "full_explanation": "",
            "functions": [],
            "classes": [],
            "variables": [],
            "imports": [],
            "language": "java",
            "metadata": {
                "model_used": "rule-based",
                "analysis_type": "rule"
            }
        }
        
        explanation_parts = []
        
        # Basic analysis
        if re.search(r'package\s+[\w.]+;', code):
            explanation_parts.append("This Java code belongs to a package.")
        
        if re.search(r'import\s+[\w.]+;', code):
            explanation_parts.append("This code imports Java libraries or classes.")
        
        if re.search(r'class\s+\w+', code):
            explanation_parts.append("This code defines Java classes.")
        
        if re.search(r'public\s+static\s+void\s+main', code):
            explanation_parts.append("This code contains a main method (entry point).")
        
        if re.search(r'public\s+\w+\s+\w+\s*\(|private\s+\w+\s+\w+\s*\(', code):
            explanation_parts.append("This code defines methods.")
        
        if re.search(r'if\s*\(|switch\s*\(', code):
            explanation_parts.append("This code contains conditional logic.")
        
        if re.search(r'for\s*\(|while\s*\(', code):
            explanation_parts.append("This code contains loops.")
        
        if not explanation_parts:
            explanation_parts.append("This appears to be a simple Java code snippet.")
        
        full_text = " ".join(explanation_parts)
        result["summary"] = full_text[:200] + "..." if len(full_text) > 200 else full_text
        result["details"] = full_text[200:] if len(full_text) > 200 else ""
        result["full_explanation"] = full_text
        
        return result
        
    except Exception as e:
        return {
            "summary": f"Java analysis error: {str(e)}",
            "details": "An error occurred while analyzing the Java code.",
            "full_explanation": f"Error during analysis: {str(e)}",
            "functions": [],
            "classes": [],
            "variables": [],
            "imports": [],
            "language": "java",
            "metadata": {
                "model_used": "rule-based",
                "analysis_type": "rule",
                "error": True
            }
        }
