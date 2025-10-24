# HyFuzz Phase 3 - MCP Server (Windows)

A high-performance Model Context Protocol (MCP) server implementation for Windows, designed for the HyFuzz fuzzing framework. This server provides intelligent payload generation using Large Language Models (LLM) integrated with Ollama/DeepSeek.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [API Documentation](#api-documentation)
- [Architecture](#architecture)
- [Development](#development)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The MCP Server is a central component of the HyFuzz Phase 3 distributed architecture. It:

- Implements the Model Context Protocol (MCP) for client-server communication
- Integrates with Ollama/DeepSeek for intelligent payload generation
- Provides knowledge base management (CWE/CVE repositories)
- Supports multiple transport protocols (HTTP, stdio, WebSocket)
- Offers caching and optimization for improved performance
- Generates intelligent fuzzing payloads using Chain-of-Thought (CoT) reasoning

## Features

### Core Features

- **Model Context Protocol Implementation**: Full MCP 2024.01 compatibility
- **LLM Integration**: Seamless Ollama integration with DeepSeek model support
- **Knowledge Base Management**: CWE/CVE database integration
- **Intelligent Payload Generation**: CoT-based reasoning for complex payloads
- **Multi-Transport Support**: HTTP, stdio, and WebSocket protocols
- **Caching Layer**: Response and result caching for performance
- **Async Architecture**: Fully asynchronous request handling

### Security Features

- Request validation and sanitization
- Error handling and exception management
- Session management
- Optional API key authentication

### Monitoring & Observability

- Comprehensive logging system
- Performance monitoring
- Health check endpoints
- Metrics collection

## System Requirements

### Minimum Requirements

- **OS**: Windows 10 (Build 19041) or later, Windows Server 2019 or later
- **Python**: 3.9 or later
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB for venv + dependencies + data
- **Network**: TCP/IP connectivity for MCP communication

### Optional Dependencies

- **Ollama**: For local LLM inference (required for payload generation)
- **Redis**: For distributed caching (optional, uses in-memory cache by default)

### Recommended Setup

- **OS**: Windows 11 Pro or Windows Server 2022
- **Python**: 3.11 or later
- **RAM**: 16GB
- **GPU**: NVIDIA GPU with CUDA support for faster LLM inference
- **Network**: Gigabit Ethernet for optimal performance

## Installation

### Step 1: Clone or Download the Repository
```bash
# Clone from repository
git clone https://github.com/your-org/hyfuzz-server-windows.git
cd hyfuzz-server-windows

# Or extract from archive
# Extract the .zip file and navigate to the directory
```

### Step 2: Create Virtual Environment
```powershell
# Create Python virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

### Step 3: Install Dependencies
```powershell
# Install required packages
pip install -r requirements-dev.txt

# Or for production only
pip install -r requirements.txt
```

### Step 4: Configure Environment
```powershell
# Copy environment template to .env
copy config\.env.template .env

# Edit .env file with your configuration
notepad .env
```

### Step 5: Install Ollama (if not already installed)
```powershell
# Download from https://ollama.ai
# Follow installation instructions for Windows

# After installation, pull the model
ollama pull deepseek-r1

# Verify installation
ollama list
```

### Step 6: Verify Installation
```powershell
# Run health check
python scripts/health_check.py

# Expected output: All services operational
```

## Configuration

### Basic Configuration

Edit `.env` file:
```bash
# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=5000
TRANSPORT_TYPE=http

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-r1

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/server.log

# Development
DEBUG=false
```

### Advanced Configuration

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for detailed configuration options.

## Running the Server

### Quick Start
```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Run the server
python -m src

# Server will start on http://0.0.0.0:5000
```

### Using PyCharm

1. Open the project in PyCharm
2. Configure Python Interpreter: File → Settings → Project → Python Interpreter
3. Select virtual environment (venv\Scripts\python.exe)
4. Run Configuration: Run → Edit Configurations
5. Create new Python configuration:
   - Script path: `src/__main__.py`
   - Working directory: `<project root>`
6. Click Run or press Shift+F10

### Using Command Line
```powershell
# Run with specific configuration
python -m src --config config/config_dev.yaml

# Run with debug mode
python -m src --debug

# Run with custom port
python -m src --port 8000
```

### Health Check
```powershell
# Test server connectivity
curl http://localhost:5000/health

# Expected response:
# {"status": "healthy", "version": "1.0.0"}
```

## API Documentation

### MCP Endpoints

#### Initialize Connection
```http
POST /mcp/initialize
Content-Type: application/json

{
  "protocolVersion": "2024.01",
  "clientInfo": {
    "name": "hyfuzz-client",
    "version": "1.0.0"
  }
}
```

#### List Resources
```http
GET /mcp/resources
```

#### List Tools
```http
GET /mcp/tools
```

#### Call Tool
```http
POST /mcp/tools/call
Content-Type: application/json

{
  "name": "generate_payloads",
  "arguments": {
    "protocol": "coap",
    "target": "192.168.1.100",
    "context": "vulnerability testing"
  }
}
```

### Health & Status
```http
GET /health
GET /status
```

For complete API documentation, see [docs/API.md](docs/API.md).

## Architecture

### Component Overview
```
┌─────────────────────────────────────────────────┐
│         MCP Server (Windows)                    │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ MCP Server Core                          │  │
│  │ ├─ server.py (Main server class)        │  │
│  │ ├─ message_handler.py                   │  │
│  │ └─ capability_manager.py                │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Transport Layer                          │  │
│  │ ├─ http_transport.py                    │  │
│  │ ├─ stdio_transport.py                   │  │
│  │ └─ websocket_transport.py               │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ LLM Service Layer                        │  │
│  │ ├─ llm_client.py (Ollama integration)   │  │
│  │ ├─ llm_service.py (High-level API)      │  │
│  │ └─ cot_engine.py (CoT reasoning)        │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Knowledge Base                           │  │
│  │ ├─ cwe_repository.py                    │  │
│  │ ├─ cve_repository.py                    │  │
│  │ └─ graph_cache.py                       │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Module Dependencies

- **mcp_server**: Core MCP protocol implementation
- **llm**: Ollama integration and LLM operations
- **knowledge**: CWE/CVE database management
- **models**: Data model definitions
- **config**: Configuration management
- **utils**: Utilities and helpers

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

## Development

### Setting Up Development Environment
```powershell
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks (optional)
# Uncomment if using pre-commit
# pre-commit install
```

### Code Style

- **Python**: PEP 8 with Black formatter
- **Line length**: 100 characters
- **Type hints**: Required for all functions
- **Documentation**: Docstring for all classes and public methods

### Running Tests
```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_server.py

# Run with verbose output
pytest -v

# Run integration tests only
pytest tests/integration/
```

### Code Quality
```powershell
# Format code with Black
black src tests

# Check style with Flake8
flake8 src tests

# Type check with MyPy
mypy src
```

## Testing

### Test Structure

- **Unit Tests** (`tests/unit/`): Individual component testing
- **Integration Tests** (`tests/integration/`): Component interaction testing
- **Performance Tests** (`tests/performance/`): Benchmark and performance testing

### Running Specific Tests
```powershell
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run performance benchmarks
pytest tests/performance/

# Run a specific test
pytest tests/unit/test_server.py::test_server_initialization
```

## Troubleshooting

### Common Issues

#### Issue: "Cannot connect to Ollama"

**Solution:**
```powershell
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start Ollama
ollama serve

# Verify model is loaded
ollama list
```

#### Issue: "Port 5000 already in use"

**Solution:**
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use different port
set SERVER_PORT=5001
python -m src
```

#### Issue: "Module not found error"

**Solution:**
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements-dev.txt --force-reinstall
```

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for more issues and solutions.

## Performance Optimization

### For Production

1. **Use production configuration**: `config_prod.yaml`
2. **Enable caching**: Set `CACHE_ENABLED=true`
3. **Use Redis backend**: Set `CACHE_BACKEND=redis`
4. **Disable debug mode**: Set `DEBUG=false`
5. **Optimize logging**: Set `LOG_LEVEL=WARNING`

### Benchmarking
```powershell
# Run performance benchmarks
python scripts/benchmark.py

# Run with specific parameters
python scripts/benchmark.py --iterations 1000 --workers 4
```

## Contributing

### Development Workflow

1. Create feature branch: `git checkout -b feature/feature-name`
2. Make changes and write tests
3. Ensure all tests pass: `pytest`
4. Format code: `black src tests`
5. Check style: `flake8 src tests`
6. Commit changes: `git commit -m "Add feature"`
7. Push to repository: `git push origin feature/feature-name`
8. Create Pull Request

### Coding Guidelines

- Follow PEP 8 standards
- Use type hints for all functions
- Write comprehensive docstrings
- Include unit tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## Additional Resources

- [MCP Specification](https://modelcontextprotocol.io)
- [Ollama Documentation](https://github.com/jmorganca/ollama)
- [DeepSeek Model Card](https://huggingface.co/deepseek-ai/deepseek-r1)
- [Python Async Documentation](https://docs.python.org/3/library/asyncio.html)

## Support

For issues, questions, or suggestions:

1. Check [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
2. Review existing GitHub issues
3. Create new GitHub issue with detailed information
4. Contact development team

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

**Last Updated**: January 2025
**Version**: 1.0.0
**Status**: Production Ready