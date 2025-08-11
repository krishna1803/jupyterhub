#!/bin/bash

# JupyterHub Manager Development Setup Script

set -e

echo "🚀 Setting up JupyterHub Manager development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.10"

if [[ $(echo "$python_version >= $required_version" | bc -l) -eq 0 ]]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create environment file template
if [ ! -f ".env" ]; then
    echo "📝 Creating .env template..."
    cat > .env << EOF
# JupyterHub Manager Configuration
JUPYTERHUB_MANAGER_JUPYTERHUB_URL=https://your-hub.example.com
JUPYTERHUB_MANAGER_API_TOKEN=your-admin-api-token
JUPYTERHUB_MANAGER_VERIFY_SSL=true
JUPYTERHUB_MANAGER_REQUEST_TIMEOUT=30
JUPYTERHUB_MANAGER_API_HOST=0.0.0.0
JUPYTERHUB_MANAGER_API_PORT=8080
JUPYTERHUB_MANAGER_STREAMLIT_PORT=8501
EOF
    echo "📄 .env file created. Please update with your JupyterHub details."
fi

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -v

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Update .env file with your JupyterHub URL and API token"
echo "2. Source the environment: source .venv/bin/activate"
echo "3. Start the API server: uvicorn jupyterhub_manager.api.main:app --reload"
echo "4. Start the UI: streamlit run jupyterhub_manager/ui/app.py"
echo ""
echo "📖 Documentation:"
echo "- API docs: http://localhost:8080/docs"
echo "- UI: http://localhost:8501"
echo ""
echo "🔧 Development commands:"
echo "- Run tests: pytest"
echo "- Lint code: ruff check ."
echo "- Format code: ruff format ."
