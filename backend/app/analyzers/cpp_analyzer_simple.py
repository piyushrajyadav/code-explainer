import re

def analyze_cpp(code):
    """
    Analyze C++ code and return a structured explanation.
    """
    try:
        result = {
            "summary": "C++ code analysis",
            "details": "",
            "full_explanation": "",
            "functions": [],
            "classes": [],
            "variables": [],
            "imports": [],
            "language": "c++",
            "metadata": {
                "model_used": "rule-based",
                "analysis_type": "rule"
            }
        }
        
        explanation_parts = []
        
        # Basic analysis
        if re.search(r'#include\s*[<"]', code):
            explanation_parts.append("This C++ code includes header files.")
        
        if re.search(r'using\s+namespace\s+std;', code):
            explanation_parts.append("This code uses the standard namespace.")
        
        if re.search(r'class\s+\w+|struct\s+\w+', code):
            explanation_parts.append("This code defines classes or structures.")
        
        if re.search(r'int\s+main\s*\(', code):
            explanation_parts.append("This code contains a main function (entry point).")
        
        if re.search(r'\w+\s+\w+\s*\([^)]*\)\s*{', code):
            explanation_parts.append("This code defines functions.")
        
        if re.search(r'if\s*\(|switch\s*\(', code):
            explanation_parts.append("This code contains conditional logic.")
        
        if re.search(r'for\s*\(|while\s*\(', code):
            explanation_parts.append("This code contains loops.")
        
        if re.search(r'cout\s*<<|printf\s*\(', code):
            explanation_parts.append("This code performs output operations.")
        
        if not explanation_parts:
            explanation_parts.append("This appears to be a simple C++ code snippet.")
        
        full_text = " ".join(explanation_parts)
        result["summary"] = full_text[:200] + "..." if len(full_text) > 200 else full_text
        result["details"] = full_text[200:] if len(full_text) > 200 else ""
        result["full_explanation"] = full_text
        
        return result
        
    except Exception as e:
        return {
            "summary": f"C++ analysis error: {str(e)}",
            "details": "An error occurred while analyzing the C++ code.",
            "full_explanation": f"Error during analysis: {str(e)}",
            "functions": [],
            "classes": [],
            "variables": [],
            "imports": [],
            "language": "c++",
            "metadata": {
                "model_used": "rule-based",
                "analysis_type": "rule",
                "error": True
            }
        }
