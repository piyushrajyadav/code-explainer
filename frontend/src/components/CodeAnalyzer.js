import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, Button, FormControl, InputLabel, Select, MenuItem, Grid, Alert, CircularProgress, Tabs, Tab, Tooltip, IconButton } from '@mui/material';
import CodeMirror from '@uiw/react-codemirror';
import { javascript } from '@codemirror/lang-javascript';
import { python } from '@codemirror/lang-python';
import { java } from '@codemirror/lang-java';
import { cpp } from '@codemirror/lang-cpp';
import TerminalIcon from '@mui/icons-material/Terminal';
import InfoIcon from '@mui/icons-material/Info';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import axios from 'axios';
import CodeExplanation from './CodeExplanation';

// Sample code examples for different languages
const codeExamples = {
  javascript: `// Todo App Component
import React, { useState } from 'react';

function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [inputValue, setInputValue] = useState('');

  // Add a new todo item
  function handleAddTodo() {
    if (inputValue.trim() !== '') {
      setTodos([...todos, { 
        id: Date.now(), 
        text: inputValue, 
        completed: false 
      }]);
      setInputValue('');
    }
  }

  // Toggle todo completion status
  function toggleTodo(id) {
    setTodos(todos.map(todo => 
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ));
  }

  // Delete a todo
  function deleteTodo(id) {
    setTodos(todos.filter(todo => todo.id !== id));
  }

  return (
    <div className="todo-app">
      <h1>Todo List</h1>
      <div className="add-todo">
        <input 
          type="text" 
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Add a new task..."
        />
        <button onClick={handleAddTodo}>Add</button>
      </div>
      <ul className="todo-list">
        {todos.map(todo => (
          <li key={todo.id} className={todo.completed ? 'completed' : ''}>
            <span onClick={() => toggleTodo(todo.id)}>{todo.text}</span>
            <button onClick={() => deleteTodo(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TodoApp;`,
  python: `# A simple banking system
class BankAccount:
    def __init__(self, account_number, owner_name, balance=0):
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = balance
        self.transactions = []
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append("Deposit: +$" + str(amount))
            return True
        return False
    
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append("Withdrawal: -$" + str(amount))
            return True
        return False
    
    def get_balance(self):
        return self.balance
    
    def get_transaction_history(self):
        return self.transactions


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}
    
    def create_account(self, owner_name, initial_deposit=0):
        account_number = self._generate_account_number()
        account = BankAccount(account_number, owner_name, initial_deposit)
        self.accounts[account_number] = account
        return account_number
    
    def _generate_account_number(self):
        # Simple account number generation
        import random
        return str(random.randint(10000000, 99999999))
    
    def get_account(self, account_number):
        return self.accounts.get(account_number)


# Usage Example
bank = Bank("Example Bank")
acc_num = bank.create_account("John Doe", 1000)
account = bank.get_account(acc_num)

account.deposit(500)
account.withdraw(200)
print("Current balance: $" + str(account.get_balance()))
print("Transaction history:")
for transaction in account.get_transaction_history():
    print("- " + transaction)`,
  java: `// Simple Calculator Application
public class Calculator {
    private double memory;
    
    public Calculator() {
        this.memory = 0;
    }
    
    public double add(double a, double b) {
        double result = a + b;
        storeInMemory(result);
        return result;
    }
    
    public double subtract(double a, double b) {
        double result = a - b;
        storeInMemory(result);
        return result;
    }
    
    public double multiply(double a, double b) {
        double result = a * b;
        storeInMemory(result);
        return result;
    }
    
    public double divide(double a, double b) throws ArithmeticException {
        if (b == 0) {
            throw new ArithmeticException("Division by zero is not allowed");
        }
        double result = a / b;
        storeInMemory(result);
        return result;
    }
    
    public double squareRoot(double a) throws ArithmeticException {
        if (a < 0) {
            throw new ArithmeticException("Cannot calculate square root of negative number");
        }
        double result = Math.sqrt(a);
        storeInMemory(result);
        return result;
    }
    
    public double power(double base, double exponent) {
        double result = Math.pow(base, exponent);
        storeInMemory(result);
        return result;
    }
    
    private void storeInMemory(double value) {
        this.memory = value;
    }
    
    public double recallMemory() {
        return this.memory;
    }
    
    public void clearMemory() {
        this.memory = 0;
    }
    
    public static void main(String[] args) {
        Calculator calc = new Calculator();
        
        System.out.println("Addition: " + calc.add(10, 5));
        System.out.println("Subtraction: " + calc.subtract(10, 5));
        System.out.println("Multiplication: " + calc.multiply(10, 5));
        System.out.println("Division: " + calc.divide(10, 5));
        System.out.println("Square Root: " + calc.squareRoot(16));
        System.out.println("Power: " + calc.power(2, 3));
        System.out.println("Memory: " + calc.recallMemory());
    }
}`,
  "c++": `#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

// A class to represent a Task in a task management system
class Task {
private:
    int id;
    std::string title;
    std::string description;
    bool completed;
    int priority; // 1-5 (5 being highest)

public:
    // Constructor
    Task(int taskId, std::string taskTitle, std::string taskDesc = "", int taskPriority = 1) 
        : id(taskId), title(taskTitle), description(taskDesc), completed(false), priority(taskPriority) {
        // Ensure priority is within valid range
        if (priority < 1) priority = 1;
        if (priority > 5) priority = 5;
    }
    
    // Getters
    int getId() const { return id; }
    std::string getTitle() const { return title; }
    std::string getDescription() const { return description; }
    bool isCompleted() const { return completed; }
    int getPriority() const { return priority; }
    
    // Setters
    void setTitle(const std::string& newTitle) { title = newTitle; }
    void setDescription(const std::string& newDesc) { description = newDesc; }
    void setCompleted(bool status) { completed = status; }
    void setPriority(int newPriority) {
        if (newPriority >= 1 && newPriority <= 5) {
            priority = newPriority;
        }
    }
    
    // Display task info
    void displayTask() const {
        std::cout << "Task #" << id << ": " << title << " [Priority: " << priority << "]" << std::endl;
        std::cout << "Status: " << (completed ? "Completed" : "Pending") << std::endl;
        if (!description.empty()) {
            std::cout << "Description: " << description << std::endl;
        }
        std::cout << "----------------------------" << std::endl;
    }
};

// Task Manager to handle a collection of tasks
class TaskManager {
private:
    std::vector<Task> tasks;
    int nextId;
    
public:
    TaskManager() : nextId(1) {}
    
    // Add a new task
    int addTask(const std::string& title, const std::string& description = "", int priority = 1) {
        Task newTask(nextId, title, description, priority);
        tasks.push_back(newTask);
        return nextId++;
    }
    
    // Delete a task by ID
    bool deleteTask(int id) {
        auto it = std::find_if(tasks.begin(), tasks.end(), 
                             [id](const Task& task) { return task.getId() == id; });
        
        if (it != tasks.end()) {
            tasks.erase(it);
            return true;
        }
        return false;
    }
    
    // Mark a task as completed
    bool completeTask(int id) {
        for (auto& task : tasks) {
            if (task.getId() == id) {
                task.setCompleted(true);
                return true;
            }
        }
        return false;
    }
    
    // List all tasks
    void listAllTasks() const {
        if (tasks.empty()) {
            std::cout << "No tasks found." << std::endl;
            return;
        }
        
        for (const auto& task : tasks) {
            task.displayTask();
        }
    }
    
    // List tasks by completion status
    void listTasksByStatus(bool completed) const {
        bool found = false;
        for (const auto& task : tasks) {
            if (task.isCompleted() == completed) {
                task.displayTask();
                found = true;
            }
        }
        
        if (!found) {
            std::cout << "No " << (completed ? "completed" : "pending") << " tasks found." << std::endl;
        }
    }
};

// Main function to demonstrate the Task Manager
int main() {
    TaskManager manager;
    
    // Add some tasks
    int task1 = manager.addTask("Complete project report", "Finish the quarterly report", 5);
    int task2 = manager.addTask("Call client", "Discuss project requirements", 4);
    int task3 = manager.addTask("Buy groceries", "Milk, bread, eggs", 2);
    
    // Display all tasks
    std::cout << "All Tasks:" << std::endl;
    manager.listAllTasks();
    
    // Complete a task
    manager.completeTask(task2);
    
    // Display pending tasks
    std::cout << "Pending Tasks:" << std::endl;
    manager.listTasksByStatus(false);
    
    // Display completed tasks
    std::cout << "Completed Tasks:" << std::endl;
    manager.listTasksByStatus(true);
    
    // Delete a task
    manager.deleteTask(task3);
    
    // Final task list
    std::cout << "Final Task List:" << std::endl;
    manager.listAllTasks();
    
    return 0;
}
`
};

const CodeAnalyzer = () => {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('javascript');
  const [explanation, setExplanation] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [tabValue, setTabValue] = useState(0);
  const [copySuccess, setCopySuccess] = useState(false);
  const [analysisMethod, setAnalysisMethod] = useState('rule');
  const [analysisOptions, setAnalysisOptions] = useState({
    methods: [],
    models: []
  });
  const [selectedModel, setSelectedModel] = useState('');

  // Fetch available analysis methods and models when component loads
  useEffect(() => {
    fetchAnalysisMethods();
  }, []);

  const fetchAnalysisMethods = async () => {
    try {
      const response = await axios.get('http://localhost:8000/analyze_methods/');
      setAnalysisOptions(response.data);
      
      // Set default model if available
      if (response.data.models && response.data.models.length > 0) {
        setSelectedModel(response.data.models[0].id);
      }
    } catch (err) {
      console.error('Failed to fetch analysis methods:', err);
      // Fallback to hardcoded models if API fails
      setAnalysisOptions({
        methods: [
          { id: 'rule', name: 'Rule-based Analysis' },
          { id: 'nlp', name: 'NLP-based Analysis' }
        ],
        models: [
          { id: 'gemini-1.5-flash', name: 'Google Gemini Flash', description: 'Fast and efficient AI model' },
          { id: 'Salesforce/codegen-350M-mono', name: 'CodeGen 350M', description: 'Lightweight code generation model' },
          { id: 'microsoft/codebert-base', name: 'CodeBERT', description: 'Base model for code understanding' }
        ]
      });
      setSelectedModel('gemini-1.5-flash');
    }
  };

  const handleAnalysisMethodChange = (event) => {
    setAnalysisMethod(event.target.value);
  };

  const handleModelChange = (event) => {
    setSelectedModel(event.target.value);
  };

  const handleLanguageChange = (event) => {
    setLanguage(event.target.value);
    // If no custom code or using example tab, update with new language example
    if (tabValue === 1 || !code) {
      setCode(codeExamples[event.target.value]);
    }
  };

  const getLanguageExtension = () => {
    switch (language) {
      case 'javascript':
        return javascript();
      case 'python':
        return python();
      case 'java':
        return java();
      case 'c++':
        return cpp();
      default:
        return javascript();
    }
  };

  const handleCodeChange = (value) => {
    setCode(value);
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
    if (newValue === 1) {
      // Load example code
      setCode(codeExamples[language]);
    }
  };

  const handleLoadExample = () => {
    setCode(codeExamples[language]);
  };

  const handleCopyExample = () => {
    navigator.clipboard.writeText(codeExamples[language])
      .then(() => {
        setCopySuccess(true);
        setTimeout(() => setCopySuccess(false), 2000);
      });
  };

  const analyzeCode = async () => {
    if (!code.trim()) {
      setError('Please enter some code to analyze');
      return;
    }

    setError('');
    setLoading(true);
    
    try {
      const requestData = {
        code,
        language,
        analysis_method: analysisMethod
      };
      
      // Add model name if using NLP analysis
      if (analysisMethod === 'nlp' && selectedModel) {
        requestData.model_name = selectedModel;
      }
      
      const response = await axios.post('http://localhost:8000/explain/', requestData);
      
      // Handle response for both rule-based and NLP (including Gemini)
      if (response.data.error) {
        setError(response.data.error);
      } else {
        // Use full_explanation first (comprehensive), then summary as fallback
        const explanation = response.data.full_explanation || 
                            response.data.summary ||
                            response.data.user_friendly_summary ||
                            'No explanation was generated.';
        setExplanation(explanation);
      }
      
      setLoading(false);
    } catch (err) {
      setLoading(false);
      if (err.response && err.response.data && err.response.data.error) {
        setError(err.response.data.error);
      } else {
        setError('Failed to analyze code. Please try again later.');
      }
    }
  };

  return (
    <Box sx={{ mb: 6 }}>
      <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 1, fontWeight: 600 }}>
        Code Analyzer
      </Typography>
      
      <Typography variant="body1" sx={{ mb: 3, color: 'text.secondary' }}>
        Paste your code or use an example to see a detailed explanation of what your code does and how it works.
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper 
            elevation={0} 
            sx={{ 
              p: 3, 
              mb: 3, 
              border: '1px solid',
              borderColor: 'divider',
              bgcolor: 'background.paper'
            }}
          >
            <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
              <Tabs value={tabValue} onChange={handleTabChange} aria-label="code input tabs">
                <Tab label="Your Code" />
                <Tab label="Example" />
              </Tabs>
            </Box>
            
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" component="h2" gutterBottom sx={{ mb: 0 }}>
                {tabValue === 0 ? 'Your Code' : 'Example Code'}
                {tabValue === 1 && (
                  <Tooltip title={copySuccess ? "Copied!" : "Copy example to clipboard"}>
                    <IconButton 
                      size="small" 
                      onClick={handleCopyExample}
                      sx={{ ml: 1 }}
                    >
                      <ContentCopyIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                )}
              </Typography>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <FormControl variant="outlined" size="small" sx={{ minWidth: 150 }}>
                  <InputLabel id="language-select-label">Language</InputLabel>
                  <Select
                    labelId="language-select-label"
                    id="language-select"
                    value={language}
                    onChange={handleLanguageChange}
                    label="Language"
                  >
                    <MenuItem value="javascript">JavaScript</MenuItem>
                    <MenuItem value="python">Python</MenuItem>
                    <MenuItem value="java">Java</MenuItem>
                    <MenuItem value="c++">C++</MenuItem>
                  </Select>
                </FormControl>
                <FormControl variant="outlined" size="small" sx={{ minWidth: 150 }}>
                  <InputLabel id="analysis-method-label">Analysis Method</InputLabel>
                  <Select
                    labelId="analysis-method-label"
                    id="analysis-method-select"
                    value={analysisMethod}
                    onChange={handleAnalysisMethodChange}
                    label="Analysis Method"
                  >
                    <MenuItem value="rule">Rule-based</MenuItem>
                    <MenuItem value="nlp">NLP-based</MenuItem>
                  </Select>
                </FormControl>
              </Box>
            </Box>
            
            {/* Model selection dropdown - shown below language and analysis method */}
            {analysisMethod === 'nlp' && (
              <Box sx={{ mb: 2 }}>
                <FormControl fullWidth variant="outlined" size="small">
                  <InputLabel id="model-select-label">
                    Select AI Model
                    <Tooltip title="Choose which AI model to use for code explanation">
                      <InfoIcon sx={{ fontSize: 16, ml: 0.5, verticalAlign: 'middle' }} />
                    </Tooltip>
                  </InputLabel>
                  <Select
                    labelId="model-select-label"
                    id="model-select"
                    value={selectedModel}
                    onChange={handleModelChange}
                    label="Select AI Model"
                  >
                    {analysisOptions.models && analysisOptions.models.length > 0 ? (
                      analysisOptions.models.map(model => (
                        <MenuItem key={model.id} value={model.id}>
                          <Box>
                            <Typography variant="body1">{model.name}</Typography>
                            {model.description && (
                              <Typography variant="caption" color="text.secondary">
                                {model.description}
                              </Typography>
                            )}
                          </Box>
                        </MenuItem>
                      ))
                    ) : (
                      <MenuItem value="">No models available</MenuItem>
                    )}
                  </Select>
                </FormControl>
              </Box>
            )}
            
            {/* Info box for selected model */}
            {analysisMethod === 'nlp' && selectedModel && (
              <Alert severity="info" sx={{ mb: 2 }}>
                <Typography variant="body2">
                  <strong>Selected Model:</strong> {analysisOptions.models?.find(m => m.id === selectedModel)?.name || selectedModel}
                </Typography>
                {analysisOptions.models?.find(m => m.id === selectedModel)?.description && (
                  <Typography variant="caption" display="block">
                    {analysisOptions.models.find(m => m.id === selectedModel).description}
                  </Typography>
                )}
              </Alert>
            )}
            
            <Box 
              sx={{ 
                border: '1px solid',
                borderColor: 'divider',
                borderRadius: 1,
                overflow: 'hidden',
                mb: 2,
                '& .cm-editor': {
                  fontSize: '14px',
                  fontFamily: '"Fira Code", monospace',
                },
                height: '400px'
              }}
            >
              <CodeMirror
                value={code}
                height="400px"
                extensions={[getLanguageExtension()]}
                onChange={handleCodeChange}
                theme="light"
              />
            </Box>

            {tabValue === 0 && (
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Button 
                  variant="outlined" 
                  color="secondary"
                  size="medium"
                  onClick={handleLoadExample}
                >
                  Load Example
                </Button>
                <Tooltip title={
                  analysisMethod === 'nlp' 
                    ? "The NLP analyzer uses machine learning to understand and explain code based on learned patterns from training data."
                    : "The rule-based analyzer identifies code structure, patterns, and purpose by examining function and variable names, control flow, and common programming patterns"
                }>
                  <IconButton color="primary">
                    <InfoIcon />
                  </IconButton>
                </Tooltip>
              </Box>
            )}

            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            <Button 
              variant="contained" 
              color="primary" 
              size="large"
              fullWidth
              startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <TerminalIcon />}
              onClick={analyzeCode}
              disabled={loading || !code.trim()}
            >
              {loading ? 'Analyzing...' : 'Analyze Code'}
            </Button>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <CodeExplanation 
            explanation={explanation} 
            loading={loading}
          />
        </Grid>
      </Grid>
    </Box>
  );
};

export default CodeAnalyzer; 