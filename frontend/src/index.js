import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// Error boundary for catching rendering errors
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
    console.error("React Error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ 
          margin: '20px', 
          padding: '20px', 
          border: '1px solid #e44', 
          borderRadius: '5px', 
          backgroundColor: '#fee' 
        }}>
          <h2>Something went wrong.</h2>
          <details style={{ whiteSpace: 'pre-wrap' }}>
            <summary>Error Details</summary>
            {this.state.error && this.state.error.toString()}
            <br />
            {this.state.errorInfo && this.state.errorInfo.componentStack}
          </details>
        </div>
      );
    }
    return this.props.children;
  }
}

try {
  console.log("Initializing React application...");
  const root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(
    <React.StrictMode>
      <ErrorBoundary>
        <App />
      </ErrorBoundary>
    </React.StrictMode>
  );
  console.log("React application rendered successfully");
} catch (error) {
  console.error("Fatal error during React initialization:", error);
  document.getElementById('root').innerHTML = `
    <div style="margin: 20px; padding: 20px; border: 1px solid #e44; border-radius: 5px; background-color: #fee;">
      <h2>Fatal Error During Initialization</h2>
      <p>${error.message}</p>
      <pre>${error.stack}</pre>
    </div>
  `;
} 