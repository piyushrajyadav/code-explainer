import re

def analyze_javascript(code):
    """
    Analyze JavaScript code and return a structured explanation.
    """
    try:
        result = {
            "summary": "",
            "user_friendly_summary": "",
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
        features_found = []
        
        # Analyze functions
        function_patterns = [
            r'function\s+(\w+)',  # Regular functions
            r'const\s+(\w+)\s*=.*=>', # Arrow functions
            r'(\w+)\s*:\s*function', # Object methods
            r'async\s+function\s+(\w+)' # Async functions
        ]
        
        functions_found = []
        for pattern in function_patterns:
            matches = re.finditer(pattern, code)
            for match in matches:
                func_name = match.group(1)
                functions_found.append(func_name)
                result["functions"].append({
                    "name": func_name,
                    "type": "function",
                    "description": f"Function '{func_name}'"
                })
        
        if functions_found:
            if len(functions_found) == 1:
                func_name = functions_found[0]
                # Analyze function purpose based on name
                if 'calculate' in func_name.lower():
                    explanation_parts.append(f"This defines a function called '{func_name}' that performs mathematical calculations.")
                elif 'get' in func_name.lower() or 'fetch' in func_name.lower():
                    explanation_parts.append(f"This defines a function called '{func_name}' that retrieves or gets data.")
                elif 'set' in func_name.lower() or 'update' in func_name.lower():
                    explanation_parts.append(f"This defines a function called '{func_name}' that updates or modifies data.")
                elif 'show' in func_name.lower() or 'display' in func_name.lower():
                    explanation_parts.append(f"This defines a function called '{func_name}' that displays information.")
                else:
                    explanation_parts.append(f"This defines a function called '{func_name}' that performs specific operations.")
            else:
                explanation_parts.append(f"This defines {len(functions_found)} functions: {', '.join(functions_found[:3])}{'...' if len(functions_found) > 3 else ''} that work together to accomplish tasks.")
            features_found.append("defines reusable functions")
        
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
                explanation_parts.append(f"This defines a class called '{classes_found[0]}' that serves as a blueprint for creating objects.")
            else:
                explanation_parts.append(f"This defines {len(classes_found)} classes: {', '.join(classes_found)} that create different types of objects.")
            features_found.append("creates object-oriented classes")
        
        # Analyze variables
        var_patterns = [
            r'let\s+(\w+)',
            r'const\s+(\w+)',
            r'var\s+(\w+)'
        ]
        
        variables_found = []
        for pattern in var_patterns:
            matches = re.finditer(pattern, code)
            for match in matches:
                var_name = match.group(1)
                if var_name not in [f["name"] for f in result["functions"]]:  # Don't count function names as variables
                    variables_found.append(var_name)
                    result["variables"].append({
                        "name": var_name,
                        "type": "variable",
                        "scope": "unknown"
                    })
        
        if variables_found:
            if len(variables_found) == 1:
                explanation_parts.append(f"This creates a variable called '{variables_found[0]}' to store data.")
            else:
                explanation_parts.append(f"This creates {len(variables_found)} variables to store different pieces of data.")
            features_found.append("stores data in variables")
        
        # Check for common patterns
        if re.search(r'console\.log|alert|document\.write', code):
            explanation_parts.append("This displays output or information to the user.")
            features_found.append("displays output or information to the user")
        
        if re.search(r'addEventListener|onclick|onload', code):
            explanation_parts.append("This handles user interactions and events.")
            features_found.append("responds to user interactions")
        
        if re.search(r'document\.|getElementById|querySelector', code):
            explanation_parts.append("This manipulates HTML elements on the page.")
            features_found.append("modifies web page content")
        
        if re.search(r'fetch\(|axios|XMLHttpRequest', code):
            explanation_parts.append("This makes network requests to external services.")
            features_found.append("communicates with external services")
        
        if re.search(r'if\s*\(|else|switch', code):
            explanation_parts.append("This contains conditional logic for decision making.")
            features_found.append("makes decisions based on conditions")
        
        if re.search(r'for\s*\(|while\s*\(|forEach', code):
            explanation_parts.append("This uses loops to repeat operations.")
            features_found.append("repeats operations multiple times")
        
        if re.search(r'async|await|\.then\(|Promise', code):
            explanation_parts.append("This handles asynchronous operations.")
            features_found.append("performs operations that take time to complete")
        
        # Create full explanation
        full_text = " ".join(explanation_parts) if explanation_parts else "This JavaScript code contains basic programming structures."
        
        # Create summary
        if explanation_parts:
            summary = explanation_parts[0] if explanation_parts else "JavaScript code with basic functionality."
        else:
            summary = "This is a JavaScript code file."
        
        # Create user-friendly summary
        if features_found:
            if len(features_found) == 1:
                user_friendly = f"In simple terms, this JavaScript code {features_found[0]}."
            elif len(features_found) == 2:
                user_friendly = f"In simple terms, this JavaScript code {features_found[0]} and {features_found[1]}."
            else:
                user_friendly = f"In simple terms, this JavaScript code {', '.join(features_found[:-1])}, and {features_found[-1]}."
        else:
            user_friendly = "In simple terms, this JavaScript code performs basic programming operations."
        
        result["summary"] = summary
        result["user_friendly_summary"] = user_friendly
        result["full_explanation"] = full_text
        result["details"] = " ".join(explanation_parts[1:]) if len(explanation_parts) > 1 else ""
        
        return result
        
    except Exception as e:
        return {
            "summary": f"JavaScript analysis error: {str(e)}",
            "user_friendly_summary": "There was an error analyzing this JavaScript code.",
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
