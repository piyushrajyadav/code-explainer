# Explain My Code - Frontend

This is the frontend application for "Explain My Code", a tool that analyzes code snippets and provides human-readable explanations.

## Features

- Support for multiple programming languages (JavaScript, Python, Java, C++)
- Syntax highlighting with CodeMirror
- Clean and intuitive user interface
- Responsive design for mobile and desktop
- Real-time analysis

## Getting Started

### Prerequisites

- Node.js (version 14.x or higher)
- npm (usually comes with Node.js)

### Installation

1. Clone the repository
2. Navigate to the frontend directory
3. Install dependencies:

```bash
npm install
```

### Running the development server

```bash
npm start
```

This will start the development server at [http://localhost:3000](http://localhost:3000).

### Building for production

```bash
npm run build
```

This creates an optimized production build in the `build` folder.

## Technologies Used

- React.js - UI library
- Material-UI - Component library
- CodeMirror - Code editor
- Axios - HTTP client

## Backend Integration

The frontend is configured to talk to the backend API running at `http://localhost:8000`. This can be changed in the `package.json` file's `proxy` field.

## Project Structure

- `src/components` - React components
- `src/context` - React context providers
- `public` - Static assets

## License

MIT 