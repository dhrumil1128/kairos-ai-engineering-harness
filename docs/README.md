# KAIROS

KAIROS is a high-agency autonomous AI system designed for complex software engineering tasks, desktop automation, and systemic orchestration. By integrating a modular provider architecture with Model Context Protocol (MCP) capabilities, KAIROS enables the seamless execution of software planning, architectural design, and production-ready code generation.

## Overview

KAIROS operates as an autonomous engine that bridges the gap between high-level intent and technical execution. By leveraging a plugin-based ecosystem and multi-provider LLM support, the system can interact with local environments, manage version control, and execute browser-based automation to solve end-to-end engineering challenges.

## Key Features

- **Multi-Provider LLM Integration**: Native support for both cloud-based (OpenAI) and local (Ollama) providers, managed via a centralized provider settings system.
- **Model Context Protocol (MCP)**: Implementation of MCP clients and servers to extend AI capabilities into Docker environments and web browsers.
- **Extensible Plugin System**: Modular plugins for Git operations, automated testing, and browser interaction.
- **Autonomous Agency**: Specialized agents capable of maintaining state and executing complex pipelines.
- **Environment Orchestration**: Ability to interface directly with the OS for file system manipulation and tool execution.

## Architecture Summary

KAIROS utilizes a decoupled architecture to ensure scalability and provider independence:

- **Agents**: 1 (Specialized logic for project generation and memory management).
- **Plugins**: 3 (Browser, Git, and Testing utilities).
- **Providers**: 4 (OpenAI, Ollama, ProviderSettings, and Stub management).
- **MCPs**: 3 (BrowserMCP, DockerMCP, and a core MCPClient).

## Technology Stack

- **Backend**: Python (Core Logic, Agents, MCP)
- **Runtime**: Node.js (Automation and Tooling)
- **LLM Integration**: OpenAI API, Ollama (Local LLMs)
- **Protocols**: Model Context Protocol (MCP)

## Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker (for DockerMCP functionality)
- Ollama (for local model execution)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/kairos.git
   cd kairos
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Node.js dependencies:
   ```bash
   npm install
   ```

## Configuration

KAIROS is configured via `core/config/provider_settings.py`. Ensure the following environment variables are set:

```env
OPENAI_API_KEY=your_openai_key
OLLAMA_BASE_URL=http://localhost:11434
KAIROS_LOG_LEVEL=INFO
```

## Usage

### Initializing the System
To start the KAIROS core and initialize the provider manager:
```bash
python main.py
```

### Executing a Task
KAIROS can be invoked to generate project structures or automate browser tasks:
```bash
python core/cli.py --task "Generate a production-ready FastAPI project structure"
```

## Project Structure

```text
KAIROS/
├── core/
│   ├── agents/             # Autonomous agent implementations
│   ├── config/              # ProviderSettings and system configuration
│   ├── mcp/                # MCP Client and Server implementations (Browser, Docker)
│   ├── plugins/            # System plugins (Git, Browser, Testing)
│   └── providers/          # LLM Provider integrations (OpenAI, Ollama)
├── tests/
│   └── unit/
│       ├── agents/         # Agent logic validation
│       └── pipeline/       # Project generation pipeline tests
└── requirements.txt        # Python dependencies
```

## Testing

KAIROS employs a rigorous unit testing suite to ensure the reliability of the autonomous pipeline.

### Running Tests
Execute the test suite using pytest:
```bash
pytest tests/unit/
```

### Test Coverage
- **Agent Validation**: Verified via `test_memory_agent.py` using `StubProviderManager`.
- **Pipeline Validation**: Verified via `test_generation_project_structure.py` using `DummyMemoryAgent`.

## Security

- **Provider Isolation**: API keys are managed through environment variables and never hardcoded.
- **Sandboxed Execution**: DockerMCP ensures that autonomous code execution occurs within isolated containers.
- **Permission Scoping**: Plugins are designed with specific scopes to prevent unauthorized system-wide modifications.

## Roadmap

- [ ] Implementation of additional specialized agents for Refactoring and Security Auditing.
- [ ] Expansion of MCP servers to include Database and Cloud Infrastructure providers.
- [ ] Integration of a persistent vector database for long-term agent memory.
- [ ] Development of a GUI dashboard for real-time agent monitoring.