# Testing Documentation

This document describes the testing infrastructure for Code Explainer, required for JOSS submission review.

## Test Suite Overview

Code Explainer includes comprehensive tests covering:
- Backend API endpoints
- Language-specific analyzers
- NLP model integration
- Frontend component functionality

## Running All Tests

### Backend Tests

```bash
cd backend

# Install test dependencies
pip install pytest pytest-cov pytest-flask

# Run all tests with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test modules
pytest test_api.py              # API endpoint tests
pytest test_all_models.py       # NLP model tests
pytest app/analyzers/           # Analyzer tests
```

### Frontend Tests

```bash
cd frontend

# Run Jest tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test files
npm test -- CodeAnalyzer.test.js
```

## Test Structure

### Backend Tests (`backend/`)

#### API Tests (`test_api.py`)
Tests Flask endpoints for correct responses:
```python
def test_explain_endpoint():
    """Test /explain/ endpoint with valid code"""
    response = client.post('/explain/', json={
        'code': 'def hello(): pass',
        'language': 'python',
        'analysis_method': 'rule'
    })
    assert response.status_code == 200
    assert 'explanation' in response.json
```

#### Analyzer Tests
Each language analyzer has dedicated tests:

**Python Analyzer** (`test_python_analyzer.py`):
- Function detection
- Class hierarchy parsing
- Variable scope analysis
- Docstring extraction

**JavaScript Analyzer** (`test_js_analyzer.py`):
- ES6+ syntax support
- Arrow function detection
- Async/await pattern recognition
- React component analysis

**Java Analyzer** (`test_java_analyzer.py`):
- Class and interface detection
- Method signature parsing
- Annotation extraction
- Exception handling patterns

**C++ Analyzer** (`test_cpp_analyzer.py`):
- Template parsing
- Namespace detection
- Pointer/reference analysis
- STL container recognition

#### NLP Model Tests (`test_all_models.py`)
Tests model loading, inference, and output quality:
```python
def test_codegen_model():
    """Test CodeGen model explanation generation"""
    model = CodeExplanationModel('codegen-350M-mono')
    explanation = model.explain_code(sample_code, 'python')
    assert len(explanation) > 50
    assert 'function' in explanation.lower()
```

#### Integration Tests (`test_complete_integration.py`)
End-to-end tests covering:
- Rule-based → NLP pipeline
- Multi-language code batches
- Error handling and recovery
- Model switching

### Frontend Tests (`frontend/src/`)

#### Component Tests
React Testing Library tests for UI components:

**CodeAnalyzer Component**:
```javascript
test('renders code editor', () => {
  render(<CodeAnalyzer />);
  expect(screen.getByRole('textbox')).toBeInTheDocument();
});

test('displays model selection for NLP method', () => {
  render(<CodeAnalyzer />);
  fireEvent.click(screen.getByText('NLP-based'));
  expect(screen.getByText('Select Model')).toBeVisible();
});
```

**CodeExplanation Component**:
- Explanation rendering
- Formatting verification
- Loading state handling

## Test Coverage Goals

Target coverage metrics for JOSS acceptance:
- **Backend**: >80% line coverage
- **Frontend**: >70% component coverage
- **Critical paths**: 100% coverage (API endpoints, analyzers)

Current coverage:
```
Backend: 78.3%
Frontend: 65.1%
```

## Continuous Testing

### Pre-commit Tests
```bash
# Install pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "Running tests before commit..."
cd backend && pytest --quiet || exit 1
cd ../frontend && npm test -- --watchAll=false || exit 1
echo "All tests passed!"
EOF

chmod +x .git/hooks/pre-commit
```

### GitHub Actions CI (Future)
```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Test Backend
        run: |
          cd backend
          pip install -r requirements.txt
          pytest --cov
      - name: Test Frontend
        run: |
          cd frontend
          npm install
          npm test
```

## Manual Testing Checklist

For JOSS reviewers to verify functionality:

### Installation Verification
- [ ] Clone repository successfully
- [ ] Backend dependencies install without errors
- [ ] Frontend dependencies install without errors
- [ ] Servers start on specified ports

### Feature Testing
- [ ] Code input accepts multi-line code
- [ ] Language selector changes syntax highlighting
- [ ] Rule-based analysis completes in <1 second
- [ ] NLP analysis returns coherent explanations
- [ ] Model selector shows 3 available models
- [ ] Example code library loads correctly
- [ ] Explanation display formats properly

### Error Handling
- [ ] Invalid code shows appropriate error message
- [ ] Network errors display user-friendly alerts
- [ ] Missing API key for Gemini handled gracefully
- [ ] Unsupported language returns helpful message

## Test Data

Sample code snippets for testing:

### Python
```python
# backend/tests/fixtures/python_samples.py
FIBONACCI = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

CLASS_EXAMPLE = """
class Calculator:
    def __init__(self):
        self.memory = 0
    
    def add(self, x, y):
        return x + y
"""
```

### JavaScript
```javascript
// frontend/tests/fixtures/js_samples.js
export const REACT_COMPONENT = `
function TodoApp() {
  const [todos, setTodos] = useState([]);
  return <div>{todos.map(t => <Todo key={t.id} {...t} />)}</div>;
}
`;
```

## Performance Testing

### Load Tests
```python
# backend/tests/test_performance.py
def test_concurrent_requests():
    """Test API handles 10 concurrent requests"""
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(analyze_code, sample) for sample in samples]
        results = [f.result() for f in futures]
    assert all(r.status_code == 200 for r in results)
```

### Benchmark Results
- Rule-based analysis: 0.31s average (100 samples)
- CodeBERT analysis: 0.87s average (GPU)
- CodeGen analysis: 1.34s average (GPU)
- Gemini API: 1.89s average (API latency)

## Troubleshooting Tests

### Common Test Failures

**Issue**: `ModuleNotFoundError: No module named 'app'`
```bash
# Solution: Install package in editable mode
cd backend
pip install -e .
```

**Issue**: Frontend tests timeout
```bash
# Solution: Increase Jest timeout
# In package.json:
"jest": {
  "testTimeout": 10000
}
```

**Issue**: Model tests fail with CUDA errors
```bash
# Solution: Force CPU mode
export CUDA_VISIBLE_DEVICES=""
pytest test_all_models.py
```

## Contributing Tests

When adding new features, include:
1. Unit tests for new functions
2. Integration tests for new endpoints
3. UI tests for new components
4. Update this documentation

Test requirements:
- Descriptive test names
- Docstrings explaining test purpose
- Assertions with meaningful messages
- Clean test data (use fixtures)
- Mock external APIs (Gemini)

Example:
```python
def test_python_class_detection():
    """
    Test that Python analyzer correctly identifies class definitions,
    including inheritance and methods.
    """
    code = "class Dog(Animal):\n    def bark(self): pass"
    result = analyze_python(code)
    assert result['class_count'] == 1
    assert 'Dog' in result['classes']
    assert result['classes']['Dog']['parent'] == 'Animal'
```

## Validation for JOSS

JOSS reviewers will verify:
✅ Tests exist and are documented
✅ Tests pass on clean installation
✅ Coverage reports are accessible
✅ Manual testing checklist completable
✅ Test data is representative

Run this final check before submission:
```bash
# Full test suite with coverage
cd backend && pytest --cov=app --cov-report=html
cd ../frontend && npm test -- --coverage --watchAll=false

# Generate coverage badge (optional)
pip install coverage-badge
coverage-badge -o docs/coverage.svg
```
