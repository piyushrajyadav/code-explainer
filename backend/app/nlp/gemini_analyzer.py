"""
Gemini-based code analyzer for high-quality explanations.
Uses Google's Gemini API to provide Copilot-level code explanations.
"""

import google.generativeai as genai
import os
from typing import Dict, Any
import logging

class GeminiCodeAnalyzer:
    """
    High-quality code analyzer using Google's Gemini AI.
    Provides detailed, natural language explanations similar to GitHub Copilot.
    """
    
    def __init__(self, api_key: str = None):
        """Initialize the Gemini analyzer with API key."""
        self.api_key = GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        
        # Use Gemini Flash model - lighter and more cost-effective
        self.model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        # Language-specific prompt templates
        self.language_contexts = {
            'python': {
                'description': 'Python programming language',
                'features': 'dynamic typing, object-oriented programming, functional programming, extensive standard library',
                'common_patterns': 'functions, classes, decorators, list comprehensions, context managers'
            },
            'javascript': {
                'description': 'JavaScript programming language',
                'features': 'dynamic typing, event-driven programming, asynchronous programming, DOM manipulation',
                'common_patterns': 'functions, arrow functions, promises, async/await, objects, arrays'
            },
            'java': {
                'description': 'Java programming language',
                'features': 'static typing, object-oriented programming, platform independence, strong type system',
                'common_patterns': 'classes, interfaces, inheritance, polymorphism, exception handling'
            },
            'cpp': {
                'description': 'C++ programming language',
                'features': 'static typing, low-level control, object-oriented programming, template metaprogramming',
                'common_patterns': 'classes, templates, pointers, memory management, RAII'
            },
            'c': {
                'description': 'C programming language',
                'features': 'static typing, procedural programming, low-level control, manual memory management',
                'common_patterns': 'functions, structures, pointers, arrays, manual memory allocation'
            }
        }
    
    def create_expert_prompt(self, code: str, language: str) -> str:
        """
        Create an expert-level prompt for Gemini that produces Copilot-quality explanations.
        """
        lang_info = self.language_contexts.get(language.lower(), self.language_contexts['python'])
        
        prompt = f"""You are a senior software engineer and coding mentor with expertise in {lang_info['description']}. 
Your task is to explain code in a clear, educational, and comprehensive manner similar to how GitHub Copilot explains code.

**Code to Analyze ({language.upper()}):**
```{language}
{code}
```

**Your Task:**
Provide a detailed explanation that includes:

1. **Overview**: Start with a clear, one-sentence summary of what this code does
2. **Step-by-Step Breakdown**: Explain each major part of the code in logical order
3. **Purpose & Functionality**: Describe the specific purpose and how it accomplishes its goal
4. **Key Concepts**: Highlight important programming concepts being used
5. **Context & Usage**: Explain when and why someone would use this code

**Guidelines for Your Explanation:**
- Write in clear, conversational English that a developer would understand
- Use technical terms appropriately but explain complex concepts
- Focus on WHAT the code does, HOW it works, and WHY it's structured this way
- Be specific about the {language} features being used: {lang_info['features']}
- Mention relevant {language} patterns: {lang_info['common_patterns']}
- Keep explanations practical and actionable
- Use bullet points or numbered lists for clarity when needed

**Example Style:**
"This code defines a Python function that... The function works by first... Then it... This is useful because..."

**Important**: 
- Be thorough but concise
- Focus on understanding, not just describing
- Explain the "why" behind the code choices
- Make it educational and insightful

Please provide your explanation now:"""

        return prompt
    
    def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        """
        Analyze code using Gemini and return structured explanation.
        
        Args:
            code: The source code to analyze
            language: Programming language (python, javascript, java, cpp, etc.)
            
        Returns:
            Dictionary containing the analysis results
        """
        try:
            print(f"[DEBUG] Gemini: Analyzing {language} code...")
            print(f"[DEBUG] Code length: {len(code)} characters")
            
            # Create the expert prompt
            prompt = self.create_expert_prompt(code, language)
            print(f"[DEBUG] Prompt created, length: {len(prompt)} characters")
            
            # Generate response using Gemini
            print("[DEBUG] Calling Gemini API...")
            response = self.model.generate_content(prompt)
            print(f"[DEBUG] Gemini response received: {bool(response)}")
            
            if not response:
                print("[DEBUG] No response from Gemini")
                return self._create_error_response("Gemini did not generate a response")
            
            if not response.text:
                print("[DEBUG] Response has no text")
                return self._create_error_response("Gemini response is empty")
            
            explanation = response.text.strip()
            print(f"[DEBUG] Explanation length: {len(explanation)} characters")
            print(f"[DEBUG] Explanation preview: {explanation[:100]}...")
            
            # Structure the response
            result = self._structure_gemini_response(explanation, language)
            print(f"[DEBUG] Structured response created with keys: {list(result.keys())}")
            
            return result
            
        except Exception as e:
            print(f"[DEBUG] Gemini analysis error: {str(e)}")
            logging.error(f"Gemini analysis error: {str(e)}")
            return self._create_error_response(f"Error during Gemini analysis: {str(e)}")
    
    def _structure_gemini_response(self, explanation: str, language: str) -> Dict[str, Any]:
        """Structure the Gemini response into the expected format."""
        
        # Extract different parts of the explanation
        lines = explanation.split('\n')
        
        # Try to find overview/summary (usually in the first few lines)
        summary_lines = []
        detailed_lines = []
        
        in_detailed_section = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Skip markdown headers and formatting
            if line.startswith('#') or line.startswith('**') or line.startswith('*'):
                in_detailed_section = True
                continue
                
            if not in_detailed_section and len(summary_lines) < 3:
                summary_lines.append(line)
            else:
                detailed_lines.append(line)
        
        # Create summary and full explanation
        summary = ' '.join(summary_lines[:2]) if summary_lines else explanation[:200] + "..."
        user_friendly = f"In simple terms, this {language} code " + (summary_lines[0].lower() if summary_lines else "performs programming operations.")
        
        return {
            "summary": summary,
            "user_friendly_summary": user_friendly,
            "full_explanation": explanation,
            "details": ' '.join(detailed_lines) if detailed_lines else "",
            "functions": [],  # Gemini doesn't extract structured data
            "classes": [],
            "variables": [],
            "imports": [],
            "language": language,
            "metadata": {
                "model_used": "gemini-1.5-flash",
                "analysis_type": "nlp",
                "provider": "google"
            }
        }
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create a standardized error response."""
        return {
            "summary": f"Error: {error_message}",
            "user_friendly_summary": "Sorry, there was an error analyzing your code.",
            "full_explanation": f"Analysis failed: {error_message}",
            "details": "",
            "functions": [],
            "classes": [],
            "variables": [],
            "imports": [],
            "language": "unknown",
            "metadata": {
                "model_used": "gemini-1.5-flash",
                "analysis_type": "nlp",
                "provider": "google",
                "error": True
            }
        }

# Main function for integration with existing system
def analyze_code_with_gemini(code: str, language: str) -> Dict[str, Any]:
    """
    Main function to analyze code using Gemini.
    This is the entry point that integrates with the existing NLP system.
    """
    analyzer = GeminiCodeAnalyzer()
    return analyzer.analyze_code(code, language)

# Test function
if __name__ == "__main__":
    # Test the Gemini analyzer
    test_code = """
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

print(calculate_fibonacci(10))
"""
    
    result = analyze_code_with_gemini(test_code, "python")
    print("Summary:", result["summary"])
    print("\nFull Explanation:", result["full_explanation"])
