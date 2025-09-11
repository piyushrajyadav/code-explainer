# Explain My Code

A code analysis tool that helps you understand what your code does and how it works by providing detailed explanations of its structure and functionality.

## Features

- **Code Analysis**: Get detailed explanations of your code's structure, functions, classes, and variables
- **Multi-language Support**: Currently supports JavaScript, Python, Java, and C++
- **Dual Analysis Methods**:
  - **Rule-based Analysis**: Pattern recognition through syntax parsing
  - **NLP-based Analysis**: Machine learning models to explain code (NEW!)
- **User-friendly Interface**: Clean, modern UI with syntax highlighting
- **Example Code**: Includes examples for all supported languages

## How It Works

This application analyzes your code using two distinct approaches:

### Rule-based Analysis

1. Identifying structural elements (functions, classes, variables)
2. Determining the purpose of functions and classes based on naming and code patterns
3. Recognizing common programming patterns and paradigms
4. Explaining functionality in human-readable terms

### NLP-based Analysis (New!)

1. Uses pre-trained transformer models specialized for code understanding
2. Analyzes code semantics based on learned patterns from training data
3. Provides natural language explanations of functionality
4. Understands code context and purpose at a deeper level

## Project Structure

The project consists of two main components:

### Backend (Flask API)

- Python-based API using Flask
- Code analyzers for multiple programming languages
- Pattern recognition and explanation generation
- NLP models for code analysis (NEW!)

### Frontend (React)

- Modern React application with Material-UI
- Code editor with syntax highlighting
- Organized display of code explanations
- Examples for each supported language
- Selection between rule-based and NLP analysis (NEW!)

## Getting Started

### Prerequisites

- Python 3.7+
- Node.js 14+
- npm or yarn
- PyTorch and Transformers libraries (for NLP analysis)

### Installation and Setup

#### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the NLP model (optional, but required for NLP-based analysis):
```bash
python app/nlp/setup.py
```

4. Run the Flask server:
```bash
python run.py
```

The backend will start on http://localhost:8000.

#### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will start on http://localhost:3000 and automatically connect to the backend API.

## Usage

1. Select your programming language from the dropdown
2. Choose an analysis method (Rule-based or NLP-based)
3. Paste your code in the editor or use one of the provided examples
4. Click "Analyze Code"
5. View the detailed explanation of your code's structure and functionality

## NLP Model Training (Advanced)

For advanced users who want to train or fine-tune the NLP models:

```bash
cd backend
python app/nlp/training.py --train-data path/to/data.json --output-dir ./trained_model
```

## License

MIT

## Acknowledgments

- React and Material-UI for the frontend framework
- CodeMirror for the code editor
- Flask for the backend API
- Hugging Face Transformers for NLP models # code-explainer
