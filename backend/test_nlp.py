#!/usr/bin/env python

"""
Test script for the NLP API
"""

from app.nlp.api import analyze_code_nlp

# Simple test code
test_code = '''
def hello():
    """Say hello to the world."""
    return "Hello, world!"
'''

# Test the API
print("Testing NLP API...")
result = analyze_code_nlp(test_code, 'python')

# Print the result
print("\nResult:")
print(result) 