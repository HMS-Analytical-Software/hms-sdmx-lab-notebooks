# HMS SDMX Lab Notebooks

Interactive Jupyter notebooks for working with SDMX data and the HMS FMR (Fusion Metadata Registry) system.

## 🚀 Try it Online

**[Launch JupyterLite →](https://hms-analytical-software.github.io/hms-sdmx-lab-notebooks/)**

Click the link above to run these notebooks directly in your browser - no installation required!

## 📚 What's Included

### Notebooks
- **FMR Workflow Demo - Submit & Retrieve**: Learn how to submit data and metadata to an FMR instance and retrieve information
- **FMR Workflow Demo - Validation**: Explore synchronous and asynchronous validation workflows

### Sample Data
- Example SDMX dataflows, data files, and provision agreements
- Both valid and invalid examples for testing validation workflows

### Utilities
- Helper functions for validation, error checking, and API operations

## 🔧 Development Setup

If you want to run these notebooks locally or contribute to the project:

### Prerequisites
- Python 3.8+
- Git

### Local Installation
```bash
git clone https://github.com/hms-analytical-software/hms-sdmx-lab-notebooks.git
cd hms-sdmx-lab-notebooks
pip install -r requirements.txt
jupyter notebook
```

### JupyterLite Development
To build and test the JupyterLite version locally:

```bash
pip install jupyterlite-core[all]
jupyter lite build --contents content --output-dir dist
# Serve locally
python -m http.server 8000 --directory dist
```

## 🌐 Deployment

This repository is configured for automatic deployment to GitHub Pages using JupyterLite. When you push to the main branch, GitHub Actions will:

1. Build the JupyterLite site with all notebooks
2. Deploy to GitHub Pages automatically

### Enabling GitHub Pages
1. Go to your repository's Settings
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select "GitHub Actions"
4. The site will be available at `https://yourusername.github.io/repositoryname/`

## 🔑 Authentication

To use the FMR API examples, you'll need:
- Access credentials for an HMS Lab instance
- The base URL of your FMR instance

## 🛠 Technical Details

### JupyterLite Environment
- Runs Python in the browser using Pyodide
- Pre-installed packages: `requests`, `lxml`
- No server required - fully client-side

### Browser Compatibility
- Modern browsers with WebAssembly support
- Chrome, Firefox, Safari, Edge (recent versions)

## 📖 Documentation

For more information about HMS and SDMX:
- [HMS Official Documentation](https://www.metadatatechnology.com/)
- [SDMX Standards](https://sdmx.org/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with JupyterLite
5. Submit a pull request

## 📄 License

See [LICENSE](LICENSE) file for details.

This repository contains Jupyter notebooks with examples of how to interact with the SDMX Lab via the REST API.
