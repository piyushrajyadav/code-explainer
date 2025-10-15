# Screenshots and Demo

## Web Interface

### Rule-based Analysis
![Rule-based Analysis](docs/screenshots/rule_based_analysis.png)
*Fast pattern recognition analyzing Python code structure*

### NLP-based Analysis with CodeGen
![NLP Analysis](docs/screenshots/nlp_analysis_codegen.png)
*AI-powered semantic explanation using CodeGen-350M*

### Model Selection
![Model Selection](docs/screenshots/model_selection.png)
*Choose between CodeBERT, CodeGen, or Gemini models*

### Multi-language Support
![Multi-language](docs/screenshots/multilanguage.png)
*Support for Python, JavaScript, Java, and C++*

## Creating Screenshots

To generate these screenshots for JOSS submission:

1. Start both backend and frontend servers
2. Navigate to `http://localhost:3000`
3. Use browser screenshot tools or extensions:
   - **Chrome**: F12 → Device Toolbar → Screenshot
   - **Firefox**: F12 → Screenshot icon → Save Full Page
   - **Extension**: [Awesome Screenshot](https://www.awesomescreenshot.com/)

4. Capture the following scenarios:
   - Home page with example code loaded
   - Rule-based analysis results
   - NLP analysis with different models
   - Language selector dropdown
   - Model comparison side-by-side

5. Save screenshots in `docs/screenshots/` directory:
   ```bash
   mkdir -p docs/screenshots
   ```

6. Recommended format: PNG at 1920x1080 or 1280x720 resolution
7. File naming convention: `feature_name.png`

## Recording Demo Video (Optional)

For enhanced submission, create a 2-3 minute demo video:

```bash
# Install screen recording tool
# Windows: OBS Studio (https://obsproject.com/)
# macOS: QuickTime Player (built-in)
# Linux: SimpleScreenRecorder

# Record workflow:
1. Landing page overview (10s)
2. Select language and paste code (15s)
3. Rule-based analysis demonstration (30s)
4. Switch to NLP analysis (20s)
5. Compare different models (30s)
6. Show example library (15s)
7. Conclusion (10s)

# Export as MP4, upload to YouTube as unlisted
# Add link to README: [Demo Video](https://youtube.com/...)
```

## API Usage Example

For programmatic access documentation:

```python
# Save as docs/examples/api_example.py
import requests

# Example 1: Rule-based analysis
response = requests.post('http://localhost:8000/explain/', json={
    'code': 'def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)',
    'language': 'python',
    'analysis_method': 'rule'
})
print("Rule-based:", response.json()['explanation'])

# Example 2: NLP analysis with CodeGen
response = requests.post('http://localhost:8000/explain/', json={
    'code': 'function quickSort(arr) { /* ... */ }',
    'language': 'javascript',
    'analysis_method': 'nlp',
    'model_name': 'codegen-350M-mono'
})
print("NLP-based:", response.json()['explanation'])
```

Run examples:
```bash
cd docs/examples
python api_example.py
```
