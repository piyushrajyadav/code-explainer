import ast
import astor

def analyze_python(code):
    """
    Analyze Python code and return a structured explanation.
    
    Returns:
        Dict with structured explanation including summary, functions, classes, etc.
    """
    try:
        tree = ast.parse(code)
        
        # Initialize result structure
        result = {
            "summary": "",
            "user_friendly_summary": "",
            "details": "",
            "full_explanation": "",
            "functions": [],
            "classes": [],
            "variables": [],
            "imports": [],
            "language": "python",
            "metadata": {
                "model_used": "rule-based",
                "analysis_type": "rule"
            }
        }
        
        explanation_parts = []
        
        # Get file level docstring if exists
        module_docstring = ast.get_docstring(tree)
        if module_docstring:
            explanation_parts.append(f"This Python module includes documentation: '{module_docstring}'")
        
        # Process imports
        imports_found = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    import_info = {
                        "name": name.name,
                        "alias": name.asname,
                        "type": "import"
                    }
                    imports_found.append(import_info)
                    result["imports"].append(import_info)
            elif isinstance(node, ast.ImportFrom):
                for name in node.names:
                    import_info = {
                        "name": f"{node.module}.{name.name}" if node.module else name.name,
                        "alias": name.asname,
                        "type": "from_import",
                        "module": node.module
                    }
                    imports_found.append(import_info)
                    result["imports"].append(import_info)
                    
        if imports_found:
            import_names = [imp["name"] for imp in imports_found]
            explanation_parts.append(f"The code imports the following modules: {', '.join(import_names)}.")
        
        # Process functions
        functions_found = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = analyze_function(node)
                functions_found.append(func_info)
                result["functions"].append(func_info)
                
        if functions_found:
            func_descriptions = [f["description"] for f in functions_found]
            explanation_parts.extend(func_descriptions)
        
        # Process classes
        classes_found = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = analyze_class(node)
                classes_found.append(class_info)
                result["classes"].append(class_info)
                
        if classes_found:
            class_descriptions = [c["description"] for c in classes_found]
            explanation_parts.extend(class_descriptions)
        
        # Process main level variables and code
        main_code_parts = []
        variables_found = []
        
        for node in tree.body:
            if not isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef)):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            var_info = {
                                "name": target.id,
                                "type": "variable",
                                "scope": "module"
                            }
                            variables_found.append(var_info)
                            result["variables"].append(var_info)
                    main_code_parts.append("Variable assignment at module level.")
                else:
                    # Analyze other main-level code
                    code_desc = analyze_statement(node)
                    if code_desc:
                        main_code_parts.append(code_desc)
        
        if main_code_parts:
            # Create more natural main code description
            if len(main_code_parts) == 1:
                explanation_parts.append(f"The main code {main_code_parts[0].lower()}")
            else:
                explanation_parts.append(f"The main code {' and '.join(main_code_parts).lower()}")
        
        # Create summary and full explanation
        full_text = " ".join(explanation_parts)
        
        # Generate summary (first 2 sentences or first 200 chars)
        sentences = full_text.split('. ')
        if len(sentences) >= 2:
            summary = '. '.join(sentences[:2]) + '.'
            details = '. '.join(sentences[2:]) if len(sentences) > 2 else ""
        else:
            summary = full_text[:200] + "..." if len(full_text) > 200 else full_text
            details = full_text[200:] if len(full_text) > 200 else ""
        
        # Create user-friendly summary
        features_found = []
        if functions_found:
            features_found.append("defines reusable functions")
        if classes_found:
            features_found.append("creates object-oriented classes")
        if variables_found:
            features_found.append("stores data in variables")
        if imports_found:
            features_found.append("uses external libraries")
        if main_code_parts:
            features_found.append("executes main program logic")
        
        if features_found:
            if len(features_found) == 1:
                user_friendly = f"In simple terms, this Python code {features_found[0]}."
            elif len(features_found) == 2:
                user_friendly = f"In simple terms, this Python code {features_found[0]} and {features_found[1]}."
            else:
                user_friendly = f"In simple terms, this Python code {', '.join(features_found[:-1])}, and {features_found[-1]}."
        else:
            user_friendly = "In simple terms, this Python code performs basic programming operations."
        
        result["summary"] = summary
        result["user_friendly_summary"] = user_friendly
        result["details"] = details
        result["full_explanation"] = full_text
        
        return result
        
    except SyntaxError as e:
        return {
            "summary": f"Python syntax error: {str(e)}",
            "details": "The code contains syntax errors and cannot be parsed.",
            "full_explanation": f"Python syntax error at line {e.lineno}: {str(e)}",
            "functions": [],
            "classes": [],
            "variables": [],
            "imports": [],
            "language": "python",
            "metadata": {
                "model_used": "rule-based",
                "analysis_type": "rule",
                "error": True
            }
        }
    except Exception as e:
        return {
            "summary": f"Analysis error: {str(e)}",
            "details": "An error occurred while analyzing the Python code.",
            "full_explanation": f"Error during analysis: {str(e)}",
            "functions": [],
            "classes": [],
            "variables": [],
            "imports": [],
            "language": "python",
            "metadata": {
                "model_used": "rule-based",
                "analysis_type": "rule",
                "error": True
            }
        }

def analyze_function(func_node):
    """
    Analyze a function definition node.
    """
    func_name = func_node.name
    
    # Get function arguments
    args = []
    for arg in func_node.args.args:
        args.append(arg.arg)
    
    # Get function docstring
    docstring = ast.get_docstring(func_node)
    
    # Analyze function body
    statements = analyze_function_body(func_node.body)
    
    # Create a more natural description
    if func_name == 'main':
        description = f"This defines the main function that serves as the program's entry point"
    elif func_name.startswith('__'):
        description = f"This defines a special method '{func_name}' that handles specific object behavior"
    else:
        description = f"This defines a function called '{func_name}'"
        
    if args:
        if len(args) == 1:
            description += f" that takes one input parameter called '{args[0]}'"
        else:
            description += f" that takes {len(args)} input parameters: {', '.join(args)}"
    else:
        description += " that doesn't require any input parameters"
        
    # Add functional description based on statements
    if 'Returns a value' in statements:
        description += " and returns a calculated result"
    elif any('Calls function' in s for s in statements):
        description += " and calls other functions to perform its work"
    elif statements:
        description += " and performs various operations"
    
    description += "."
    
    return {
        "name": func_name,
        "args": args,
        "docstring": docstring,
        "description": description,
        "type": "function"
    }

def analyze_class(class_node):
    """
    Analyze a class definition node.
    """
    class_name = class_node.name
    
    # Get base classes
    bases = []
    for base in class_node.bases:
        if isinstance(base, ast.Name):
            bases.append(base.id)
    
    # Get class docstring
    docstring = ast.get_docstring(class_node)
    
    # Count methods
    methods = []
    for node in class_node.body:
        if isinstance(node, ast.FunctionDef):
            methods.append(node.name)
    
    description = f"Class '{class_name}'"
    if bases:
        description += f" inherits from {', '.join(bases)}"
    description += f" with {len(methods)} method(s): {', '.join(methods) if methods else 'none'}."
    if docstring:
        description += f" Docstring: '{docstring}'"
    
    return {
        "name": class_name,
        "bases": bases,
        "methods": methods,
        "docstring": docstring,
        "description": description,
        "type": "class"
    }

def analyze_function_body(body):
    """
    Analyze the body of a function and return a list of statement descriptions.
    """
    statements = []
    
    for node in body:
        if isinstance(node, ast.Return):
            statements.append("Returns a value.")
        elif isinstance(node, ast.Assign):
            statements.append("Assigns value(s) to variable(s).")
        elif isinstance(node, ast.AugAssign):
            statements.append("Updates a variable value.")
        elif isinstance(node, ast.If):
            statements.append("Contains a conditional (if) statement.")
        elif isinstance(node, ast.For):
            statements.append("Contains a for loop.")
        elif isinstance(node, ast.While):
            statements.append("Contains a while loop.")
        elif isinstance(node, ast.Try):
            statements.append("Contains a try/except block for error handling.")
        elif isinstance(node, ast.Raise):
            statements.append("Raises an exception.")
        elif isinstance(node, ast.Assert):
            statements.append("Contains an assertion.")
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                statements.append(f"Calls function '{node.func.id}'.")
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name):
                statements.append(f"Calls function '{node.value.func.id}'.")
    
    return statements

def analyze_statement(node):
    """
    Analyze a statement node and return a description.
    """
    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
        func = node.value.func
        if isinstance(func, ast.Name):
            func_name = func.id
            if func_name == 'print':
                return "displays output to the user"
            elif func_name in ['input', 'raw_input']:
                return "gets input from the user"
            elif func_name in ['open', 'file']:
                return "works with files"
            else:
                return f"calls the '{func_name}' function"
        elif isinstance(func, ast.Attribute):
            return "calls a method or function"
    elif isinstance(node, ast.If):
        return "makes decisions using conditional logic"
    elif isinstance(node, ast.For):
        return "repeats actions using a for loop"
    elif isinstance(node, ast.While):
        return "repeats actions using a while loop"
    elif isinstance(node, ast.Try):
        return "handles potential errors safely"
    elif isinstance(node, ast.With):
        return "Uses a context manager (with statement)."
    
    return "Contains executable code."