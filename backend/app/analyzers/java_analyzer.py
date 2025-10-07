import re

def analyze_java(code):
    """
    Analyze Java code and return a structured explanation.
    """
    try:
        result = {
            "summary": "Java code analysis",
            "user_friendly_summary": "",
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
        features_found = []
        
        # Analyze classes
        class_matches = re.finditer(r'class\s+(\w+)', code)
        classes_found = []
        for match in class_matches:
            class_name = match.group(1)
            classes_found.append(class_name)
            result["classes"].append({
                "name": class_name,
                "type": "class",
                "description": f"Class '{class_name}'"
            })
        
        if classes_found:
            if len(classes_found) == 1:
                explanation_parts.append(f"This defines a Java class called '{classes_found[0]}' that serves as a blueprint for creating objects.")
            else:
                explanation_parts.append(f"This defines {len(classes_found)} Java classes: {', '.join(classes_found)} that create different types of objects.")
            features_found.append("creates object-oriented classes")
        
        # Analyze methods
        method_matches = re.finditer(r'(public|private|protected|static)?\s*(public|private|protected|static)?\s*\w+\s+(\w+)\s*\([^)]*\)\s*\{', code)
        methods_found = []
        for match in method_matches:
            method_name = match.group(3)
            if method_name not in ['main', 'if', 'for', 'while']:  # Exclude keywords
                methods_found.append(method_name)
                result["functions"].append({
                    "name": method_name,
                    "type": "method",
                    "description": f"Method '{method_name}'"
                })
        
        if methods_found:
            explanation_parts.append(f"This defines {len(methods_found)} method(s) that perform specific operations.")
            features_found.append("defines reusable methods")
        
        # Check for main method
        if re.search(r'public\s+static\s+void\s+main', code):
            explanation_parts.append("This contains a main method that serves as the program's entry point.")
            features_found.append("serves as a program starting point")
        
        # Check for output statements
        if re.search(r'System\.out\.print', code):
            explanation_parts.append("This displays output to the console.")
            features_found.append("displays output to users")
        
        # Check for imports
        if re.search(r'import\s+[\w.]+;', code):
            explanation_parts.append("This imports external Java libraries or classes.")
            features_found.append("uses external Java libraries")
        
        # Check for control structures
        if re.search(r'if\s*\(|else|switch', code):
            explanation_parts.append("This contains conditional logic for decision making.")
            features_found.append("makes decisions based on conditions")
        
        if re.search(r'for\s*\(|while\s*\(|do\s*\{', code):
            explanation_parts.append("This uses loops to repeat operations.")
            features_found.append("repeats operations multiple times")
        
        # Create explanations
        full_text = " ".join(explanation_parts) if explanation_parts else "This Java code contains basic programming structures."
        
        # Create summary (first sentence or 200 chars)
        sentences = full_text.split('. ')
        if len(sentences) >= 2:
            summary = sentences[0] + '.'
            details = '. '.join(sentences[1:]) if len(sentences) > 1 else ""
        else:
            summary = full_text[:200] + "..." if len(full_text) > 200 else full_text
            details = full_text[200:] if len(full_text) > 200 else ""
        
        # Create user-friendly summary
        if features_found:
            if len(features_found) == 1:
                user_friendly = f"In simple terms, this Java code {features_found[0]}."
            elif len(features_found) == 2:
                user_friendly = f"In simple terms, this Java code {features_found[0]} and {features_found[1]}."
            else:
                user_friendly = f"In simple terms, this Java code {', '.join(features_found[:-1])}, and {features_found[-1]}."
        else:
            user_friendly = "In simple terms, this Java code performs basic programming operations."
        
        # Set the results
        result["summary"] = summary
        result["user_friendly_summary"] = user_friendly
        result["details"] = details
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
