import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Header from './components/Header';
import CodeAnalyzer from './components/CodeAnalyzer';
import Footer from './components/Footer';

// Create a custom theme with a nice color palette
const theme = createTheme({
  palette: {
    primary: {
      main: '#4a148c', // Deep purple
      light: '#7c43bd',
      dark: '#12005e',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#ff6d00', // Deep orange
      light: '#ff9e40',
      dark: '#c43e00',
      contrastText: '#000000',
    },
    background: {
      default: '#f9fafb',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: [
      'Roboto',
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Arial',
      'sans-serif',
    ].join(','),
    h1: {
      fontWeight: 700,
    },
    h2: {
      fontWeight: 600,
    },
    h3: {
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.05)',
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="app">
        <Header />
        <main className="container">
          <CodeAnalyzer />
        </main>
        <Footer />
      </div>
    </ThemeProvider>
  );
}

export default App; 