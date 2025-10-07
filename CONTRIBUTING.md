# Contributing to Code Explainer

First off, thank you for considering contributing to Code Explainer! It's people like you that make Code Explainer such a great tool.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, screenshots, etc.)
- **Describe the behavior you observed and what you expected**
- **Include your environment details** (OS, Python version, Node version, browser)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any similar features in other tools**

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Make your changes** ensuring code quality
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Ensure the test suite passes**
6. **Make sure your code lints** (follow existing code style)
7. **Issue the pull request**

## Development Setup

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python run.py
```

### Frontend Development

```bash
cd frontend
npm install
npm start
```

## Code Style Guidelines

### Python (Backend)
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused
- Add type hints where appropriate

### JavaScript/React (Frontend)
- Use functional components with hooks
- Follow React best practices
- Use meaningful component and variable names
- Keep components small and reusable
- Add PropTypes or TypeScript types

## Adding New Language Support

To add support for a new programming language:

1. Create a new analyzer in `backend/app/analyzers/`
2. Implement the analyzer interface:
   ```python
   def analyze_<language>(code: str) -> dict:
       # Your implementation
       pass
   ```
3. Add language patterns to `CodeProcessor._init_language_patterns()`
4. Update the frontend language dropdown
5. Add example code for the new language
6. Update documentation

## Adding New AI Models

To add a new AI model:

1. Update `backend/app/nlp/model.py` to support the new model
2. Add model information to `get_analyze_methods()` in `backend/app/main.py`
3. Update frontend model dropdown
4. Add model documentation
5. Test thoroughly with various code samples

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Documentation

- Update README.md for major changes
- Add inline comments for complex logic
- Update API documentation if endpoints change
- Add examples for new features

## Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when relevant

Examples:
```
Add support for Rust language analysis
Fix memory leak in NLP model loading
Update README with installation instructions
```

## Code Review Process

1. All submissions require review
2. Maintainers will review your PR
3. Address any feedback or requested changes
4. Once approved, your PR will be merged

## Community

- Be respectful and welcoming
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)
- Help others in issues and discussions

## Questions?

Feel free to create an issue with the "question" label or reach out to the maintainers.

Thank you for contributing! 🎉
