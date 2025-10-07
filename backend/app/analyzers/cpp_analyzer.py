import re

def analyze_cpp(code):
    """
    Analyze C++ code and return a structured explanation.
    """
    try:
        result = {
            "summary": "C++ code analysis",
            "user_friendly_summary": "",
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
        features_found = []
        
        # Basic analysis
        if re.search(r'#include\s*[<"]', code):
            explanation_parts.append("This C++ code includes header files.")
            features_found.append("uses external C++ libraries")
        
        if re.search(r'using\s+namespace\s+std;', code):
            explanation_parts.append("This code uses the standard namespace.")
        
        if re.search(r'class\s+\w+', code):
            explanation_parts.append("This code defines C++ classes.")
            features_found.append("creates object-oriented classes")
        
        if re.search(r'int\s+main\s*\(', code):
            explanation_parts.append("This code contains a main function - the program entry point.")
            features_found.append("serves as a program starting point")
        
        if re.search(r'\w+\s+\w+\s*\([^)]*\)\s*\{', code):
            explanation_parts.append("This code defines functions.")
            features_found.append("defines reusable functions")
        
        if re.search(r'cout\s*<<|printf\s*\(', code):
            explanation_parts.append("This code outputs text to the console.")
            features_found.append("displays output to users")
        
        if re.search(r'cin\s*>>|scanf\s*\(', code):
            explanation_parts.append("This code reads input from users.")
            features_found.append("gets information from users")
        
        if re.search(r'if\s*\(|else|switch', code):
            explanation_parts.append("This code contains conditional logic.")
            features_found.append("makes decisions based on conditions")
        
        if re.search(r'for\s*\(|while\s*\(|do\s*\{', code):
            explanation_parts.append("This code uses loops for repetition.")
            features_found.append("repeats operations multiple times")
        
        # Create explanations
        full_text = " ".join(explanation_parts) if explanation_parts else "This C++ code contains basic programming structures."
        
        summary = explanation_parts[0] if explanation_parts else "C++ code with basic functionality."
        
        # Create user-friendly summary
        if features_found:
            if len(features_found) == 1:
                user_friendly = f"In simple terms, this C++ code {features_found[0]}."
            elif len(features_found) == 2:
                user_friendly = f"In simple terms, this C++ code {features_found[0]} and {features_found[1]}."
            else:
                user_friendly = f"In simple terms, this C++ code {', '.join(features_found[:-1])}, and {features_found[-1]}."
        else:
            user_friendly = "In simple terms, this C++ code performs basic programming operations."
        
        full_text = " ".join(explanation_parts)
        result["summary"] = full_text[:200] + "..." if len(full_text) > 200 else full_text
        result["user_friendly_summary"] = user_friendly
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
