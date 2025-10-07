# 🚀 Code Explainer - AI-Powered Code Analysis Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.2.0-61dafb)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.2.3-green)](https://flask.palletsprojects.com/)

An intelligent code analysis tool that helps developers understand code functionality through detailed explanations. Supports both traditional rule-based analysis and cutting-edge AI/NLP-based analysis using transformer models.

<img width="2833" height="1523" alt="image" src="https://github.com/user-attachments/assets/6d40d4ad-af2c-4257-90a4-65162bc68aa1" />


## ✨ Features

- 🎯 **Intelligent Code Analysis**: Get detailed explanations of code structure, functions, classes, and variables
- 🌐 **Multi-language Support**: JavaScript, Python, Java, and C++
- 🤖 **Dual Analysis Methods**:
  - **Rule-based Analysis**: Fast pattern recognition through syntax parsing
  - **NLP-based Analysis**: AI-powered explanations using transformer models (CodeBERT, CodeGen, Gemini)
- 🎨 **Modern UI**: Clean interface with syntax highlighting powered by CodeMirror
- 📚 **Example Code Library**: Pre-loaded examples for all supported languages
- 💡 **Real-time Analysis**: Instant code explanations as you type
- 🔍 **Detailed Insights**: Function signatures, class hierarchies, and code complexity metrics

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

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 14+** and **npm** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/)

### Installation

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/piyushrajyadav/code-explainer.git
cd code-explainer
```

#### 2️⃣ Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (optional)
echo "FLASK_ENV=development" > .env
echo "FLASK_APP=run.py" >> .env
echo "PORT=8000" >> .env

# Run the Flask server
python run.py
```

✅ Backend will start on **http://localhost:8000**

#### 3️⃣ Frontend Setup

Open a **new terminal window**:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

✅ Frontend will start on **http://localhost:3000**

### 🎉 You're Ready!

Open your browser and navigate to `http://localhost:3000` to start analyzing code!

## 📖 Usage

### Basic Usage

1. **Select Language**: Choose your programming language (JavaScript, Python, Java, C++)
2. **Choose Analysis Method**:
   - **Rule-based**: Fast, offline analysis using pattern matching
   - **NLP-based**: AI-powered analysis using transformer models
3. **Select AI Model** (for NLP-based):
   - **Google Gemini Flash**: Fast and efficient (requires API key)
   - **CodeGen 350M**: Lightweight local model
   - **CodeBERT**: Base code understanding model
4. **Enter Code**: Paste your code or load an example
5. **Analyze**: Click "Analyze Code" button
6. **Review**: Get detailed explanations, structure analysis, and suggestions

### Example Workflow

```javascript
// Example: Analyzing a React Component
function TodoApp() {
  const [todos, setTodos] = useState([]);
  // ... rest of the code
}
```

**Result**: Detailed explanation of component structure, state management, and functionality.

## 🏗️ Project Structure

```
code-explainer/
├── backend/                  # Flask API Backend
│   ├── app/
│   │   ├── analyzers/       # Language-specific analyzers
│   │   │   ├── python_analyzer.py
│   │   │   ├── js_analyzer.py
│   │   │   ├── java_analyzer.py
│   │   │   └── cpp_analyzer.py
│   │   ├── nlp/             # NLP models and API
│   │   │   ├── model.py     # Model wrapper
│   │   │   ├── api.py       # NLP API endpoints
│   │   │   ├── gemini_analyzer.py
│   │   │   └── saved_models/ # Pre-trained models
│   │   └── main.py          # Flask routes
│   ├── requirements.txt
│   └── run.py               # Application entry point
├── frontend/                 # React Frontend
│   ├── public/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── CodeAnalyzer.js
│   │   │   ├── CodeExplanation.js
│   │   │   ├── Header.js
│   │   │   └── Footer.js
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── .gitignore
└── README.md
```

## 🤖 AI Models

### Available Models

| Model | Type | Size | Speed | Quality | Local/API |
|-------|------|------|-------|---------|-----------|
| **Google Gemini Flash** | LLM | - | ⚡ Very Fast | ⭐⭐⭐⭐⭐ | API |
| **CodeGen 350M** | Code Gen | 350M | 🚀 Fast | ⭐⭐⭐⭐ | Local |
| **CodeBERT** | Code Understanding | 125M | 🚀 Fast | ⭐⭐⭐ | Local |

### Using Gemini API (Optional)

To use Google Gemini for enhanced explanations:

1. Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create `.env` file in backend directory:
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```
3. Select "Google Gemini Flash" from the model dropdown

## 🛠️ Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production

#### Backend
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

#### Frontend
```bash
cd frontend
npm run build
# Serve build folder with your preferred static file server
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: Backend won't start
- **Solution**: Make sure Python 3.8+ is installed and virtual environment is activated

**Issue**: Frontend can't connect to backend
- **Solution**: Verify backend is running on port 8000 and CORS is enabled

**Issue**: Model download fails
- **Solution**: Check internet connection and ensure sufficient disk space (~2GB for models)

**Issue**: Port already in use
- **Solution**: Kill the process using the port or change the port in `.env` file

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Hugging Face](https://huggingface.co/)** - Transformer models and tokenizers
- **[Google Gemini](https://deepmind.google/technologies/gemini/)** - Advanced AI model
- **[React](https://reactjs.org/)** - Frontend framework
- **[Material-UI](https://mui.com/)** - UI components
- **[CodeMirror](https://codemirror.net/)** - Code editor
- **[Flask](https://flask.palletsprojects.com/)** - Backend framework
- **[Salesforce CodeGen](https://github.com/salesforce/CodeGen)** - Code generation model

## 👨‍💻 Developer 

**Piyush  Yadav**
[piyush yadav](https://piyushyadav.me)

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---
