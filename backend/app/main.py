from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the project directory to the path so we can import analyzers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import rule-based analyzers
from app.analyzers.python_analyzer import analyze_python
from app.analyzers.js_analyzer import analyze_javascript
from app.analyzers.java_analyzer import analyze_java
from app.analyzers.cpp_analyzer import analyze_cpp

# Import NLP-based analyzer
from app.nlp.api import analyze_code_nlp, format_explanation

app = Flask(__name__)
CORS(app)

@app.route('/')
def read_root():
    return jsonify({"message": "Welcome to Explain My Code API"})

@app.route('/explain/', methods=['POST'])
def explain_code():
    data = request.json
    
    if not data or 'code' not in data or 'language' not in data:
        return jsonify({"error": "Request must include code and language"}), 400
    
    code = data['code']
    language = data['language'].lower()
    # Get analysis method: 'rule' or 'nlp'
    analysis_method = data.get('analysis_method', 'rule').lower()
    # Get NLP model name if specified
    model_name = data.get('model_name')
    
    if not code:
        return jsonify({"error": "Code cannot be empty"}), 400
    
    try:
        if analysis_method == 'nlp':
            # Use NLP-based analysis
            explanation_result = analyze_code_nlp(code, language, model_name)
            
            # Check if this is a Gemini response (which is already properly formatted)
            if (model_name and model_name.lower() in ['gemini', 'gemini-1.5-flash', 'gemini-flash', 'google-gemini']) or \
               (explanation_result.get('metadata', {}).get('provider') == 'google'):
                # Gemini responses are already properly formatted
                return jsonify(explanation_result)
            else:
                # Traditional NLP models need formatting
                formatted_explanation = format_explanation(explanation_result)
                return jsonify(formatted_explanation)
        else:
            # Use rule-based analysis
            explanation_result = None
            
            if language == "python":
                explanation_result = analyze_python(code)
            elif language == "javascript":
                explanation_result = analyze_javascript(code)
            elif language == "java":
                explanation_result = analyze_java(code)
            elif language == "c++":
                explanation_result = analyze_cpp(code)
            else:
                return jsonify({
                    "error": f"Language {language} is not supported. Supported languages: python, javascript, java, c++"
                }), 400
            
            # Format rule-based analysis to match NLP format
            if isinstance(explanation_result, str):
                # Legacy format - convert to structured format
                formatted_result = {
                    "summary": explanation_result[:200] + "..." if len(explanation_result) > 200 else explanation_result,
                    "user_friendly_summary": "In simple terms, this code performs programming operations.",
                    "details": explanation_result if len(explanation_result) > 200 else "",
                    "full_explanation": explanation_result,
                    "functions": [],
                    "classes": [],
                    "variables": [],
                    "imports": [],
                    "language": language,
                    "metadata": {
                        "model_used": "rule-based",
                        "analysis_type": "rule"
                    }
                }
            else:
                # New structured format
                formatted_result = explanation_result
                
            return jsonify(formatted_result)
    
    except Exception as e:
        return jsonify({"error": f"Error analyzing code: {str(e)}"}), 500

@app.route('/analyze_methods/', methods=['GET'])
def get_analyze_methods():
    """Return available analysis methods and models."""
    methods = {
        "methods": [
            {
                "id": "rule",
                "name": "Rule-based Analysis",
                "description": "Uses pattern matching and syntax parsing to analyze code."
            },
            {
                "id": "nlp",
                "name": "NLP-based Analysis",
                "description": "Uses machine learning models to analyze and explain code."
            }
        ],
        "models": [
            {
                "id": "gemini-1.5-flash",
                "name": "Google Gemini Flash",
                "description": "Google's fast and efficient AI model for high-quality code explanations (API-based)."
            },
            {
                "id": "Salesforce/codegen-350M-mono",
                "name": "CodeGen 350M",
                "description": "Lightweight code generation model optimized for local use."
            },
            {
                "id": "microsoft/codebert-base",
                "name": "CodeBERT",
                "description": "Base model for code understanding."
            }
            # Add more models as they become available
        ]
    }
    return jsonify(methods)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 