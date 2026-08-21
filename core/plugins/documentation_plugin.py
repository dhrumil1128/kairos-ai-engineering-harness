"""
File: core/plugins/documentation_plugin.py

Purpose:
Production-grade documentation plugin.

Generates project documentation
using the currently selected LLM.

Architecture:

Workflow Planner
        ↓
Documentation Plugin
        ↓
Provider Manager
        ↓
Current Session Model
        ↓
Generated Documentation
        ↓
Filesystem Plugin

Supported Actions:

- generate_readme
- generate_architecture
- generate_api_docs
- generate_setup_guide
- generate_developer_guide
- generate_project_summary
- generate_changelog
- generate_project_tree
- generate_all

Generated Files:

README.md
ARCHITECTURE.md
API.md
SETUP.md
DEVELOPER_GUIDE.md
PROJECT_SUMMARY.md
CHANGELOG.md
PROJECT_TREE.md

V1:
- LLM documentation generation

V2:
- Repository analysis

V3:
- Automatic API discovery

V4:
- Documentation updates

V5:
- Autonomous documentation

Enterprise:

- Team documentation
- Versioned documentation
- Compliance documentation
- Documentation review workflows
"""

from pathlib import Path
import json

from core.plugins.plugin_base import (
    PluginBase
)

from core.providers.provider_manager import (
    ProviderManager
)

from core.providers.provider_registry import (
    ProviderRegistry
)

from core.analyzers.project_analyzer import (
    ProjectAnalyzer
)


class DocumentationPlugin(
    PluginBase
):
    """
    Documentation plugin.
    """

    def __init__(
        self,
        runtime
    ):
        """
        Initialize plugin.
        """

        super().__init__(
            name="DocumentationPlugin"
        )
        self.runtime = runtime
        
        self.provider_manager = (
            ProviderManager(
                ProviderRegistry()
            )
        )
        
        self.project_analyzer = (
            ProjectAnalyzer(
                self.runtime
            )
        )
        
        
        
        
    def _build_project_context(
        self
    ) -> str:
        """
        Build project context
        for documentation generation.
        """

        context = (
            self.project_analyzer
            .analyze_project()
        )

        lightweight_context = {

            "project_name":
                context.get(
                    "project_name"
                ),

            "tech_stack":
                context.get(
                    "tech_stack"
                ),

            "frameworks":
                context.get(
                    "frameworks"
                ),

            "agents":
                context.get(
                    "agents"
                ),

            "plugins":
                context.get(
                    "plugins"
                ),

            "providers":
                context.get(
                    "providers"
                ),

            "mcps":
                context.get(
                    "mcps"
                ),

            "architecture_summary":
                context.get(
                    "architecture_summary"
                ),

            "project_summary":
                context.get(
                    "project_summary"
                )
        }

        return json.dumps(
            lightweight_context,
            indent=4
        )
        
    # Helper Function to create the Folder in working Directory  
    def _get_docs_path(
        self
    ):
        project = (
            self.runtime
            .get_active_project()
        )

        docs_path = (
            Path(project)
            / "docs"
        )

        docs_path.mkdir(
            parents=True,
            exist_ok=True
        )

        return docs_path
    
    # Helper Function to Save the Generated Files .  
    def _save_document(
        self,
        filename: str,
        content: str
    ):
        docs_path = (
            self._get_docs_path()
        )

        file_path = (
            docs_path
            / filename
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        return str(
            file_path
        )




    def execute(
        self,
        action: str,
        project_name: str
    ) -> str:
        """
        Execute documentation action.
        """

        actions = {

            "generate_readme":
                self.generate_readme,

            "generate_architecture":
                self.generate_architecture,

            "generate_api_docs":
                self.generate_api_docs,

            "generate_setup_guide":
                self.generate_setup_guide,

            "generate_developer_guide":
                self.generate_developer_guide,

            "generate_project_summary":
                self.generate_project_summary,

            "generate_changelog":
                self.generate_changelog,

            "generate_project_tree":
                self.generate_project_tree,

            "generate_all":
                self.generate_all
        }

        if action not in actions:

            raise ValueError(
                f"Unknown action: {action}"
            )

        return (
            actions[action](
                project_name
            )
        )

    def _generate(
        self,
        prompt: str
    ) -> str:
        """
        Generate documentation
        using active provider.
        """

        return (
            self.provider_manager
            .execute(
                task_type="documentation",
                prompt=prompt
            )
        )



# For The Readme file .
    def generate_readme(
        self,
        project_name: str
    ) -> str:
        """
        Generate README.
        """
        project_context = (
        self._build_project_context()
    )

        prompt = f"""
Generate a professional README.md.

Project:
{project_name}

Context:
{project_context}

Include:

- Overview
- Key Features
- Architecture Summary
- Technology Stack
- Installation
- Configuration
- Usage
- Project Structure
- Testing
- Security
- Roadmap

Rules:

- Markdown only
- Professional engineering tone
- No placeholders
- No AI disclaimers
- Suitable for GitHub
"""

        content = (
            self._generate(
                prompt
            )
        )

        return (
            self._save_document(
                "README.md",
                content
            )
        )




# For the ARCHITECTURE.md File.
    def generate_architecture(
        self,
        project_name: str
    ) -> str:
        """
        Generate architecture docs.
        """
        project_context = (
        self._build_project_context()
    )
        prompt = f"""
Generate ARCHITECTURE.md.

Project:
{project_name}

Context:
{project_context}

Include:

- System Overview
- Architectural Principles
- Core Components
- Request Flow
- Execution Flow
- Data Flow
- Security Architecture
- Error Handling
- Scalability
- Architecture Diagram
- Future Evolution

Rules:

- Markdown only
- Senior-engineer audience
- No placeholders
- No AI disclaimers
"""

        content = (
            self._generate(
                prompt
            )
        )

        return (
            self._save_document(
                "ARCHITECTURE.md",
                content
            )
        )
        
        
        
        
    # For the API.md File.
    def generate_api_docs(
        self,
        project_name: str
    ) -> str:
        """
        Generate API docs.
        """

        project_context = (
    self._build_project_context()
)
        
        
        prompt = f"""
Generate API.md.

Project:
{project_name}

Context:
{project_context}

Include:

- API Overview
- Authentication
- Endpoints
- Request Lifecycle
- Validation Rules
- Error Handling
- Security
- Integration Examples
- Monitoring
- Future API Roadmap

Rules:

- Markdown only
- Production-ready documentation
- No placeholders
- No AI disclaimers
"""
        content = (
            self._generate(
                prompt
            )
        )

        return (
            self._save_document(
                "API.md",
                content
            )
        )




# For the SETUP.md File.
    def generate_setup_guide(
        self,
        project_name: str
    ) -> str:
        """
        Generate setup guide.
        """
        project_context = (
    self._build_project_context()
)
        
        
        prompt = f"""
Generate SETUP.md.

Project:
{project_name}

Context:
{project_context}

Include:

- Requirements
- Prerequisites
- Installation
- Configuration
- Environment Variables
- Running the Project
- Running Tests
- Verification
- Troubleshooting
- Security Recommendations

Rules:

- Markdown only
- Clear step-by-step instructions
- No placeholders
- No AI disclaimers
"""
        content = (
            self._generate(
                prompt
            )
        )

        return (
            self._save_document(
                "SETUP.md",
                content
            )
        )




# For DEVELOPER_GUIDE.md File.
    def generate_developer_guide(
        self,
        project_name: str
    ) -> str:
        """
        Generate developer guide.
        """
        project_context = (
    self._build_project_context()
)
        prompt = f"""
Generate DEVELOPER_GUIDE.md.

Project:
{project_name}

Context:
{project_context}

Include:

- Development Philosophy
- Architecture Overview
- Project Structure
- Coding Standards
- Development Workflow
- Core Components
- Plugin Development
- Testing Standards
- Security Guidelines
- Debugging
- Contribution Guide

Rules:

- Markdown only
- Professional engineering handbook
- No placeholders
- No AI disclaimers
"""
        content = (
            self._generate(
                prompt
            )
        )

        return (
            self._save_document(
                "DEVELOPER_GUIDE.md",
                content
            )
        )







# For PROJECT_SUMMARY.md File.
    def generate_project_summary(
        self,
        project_name: str
    ) -> str:
        """
        Generate project summary.
        """
        project_context = (
    self._build_project_context()
)
        prompt = f"""
Generate PROJECT_SUMMARY.md.

Project:
{project_name}

Repository Intelligence:
{project_context}

You are analyzing a real software repository.

Do NOT write generic project summaries.

Use the repository intelligence to determine:

- What the system actually does
- Main architecture
- Core agents
- Core plugins
- Core providers
- Core MCP integrations
- Execution flow
- User workflow
- Technical capabilities

Include:

# Executive Summary

Explain the actual purpose of the project.

# Problem Statement

What problem does this project solve?

# Objectives

List the primary goals.

# Core Components

Explain important agents, plugins,
providers, MCPs, managers,
and orchestration components.

# Key Features

List major capabilities.

# Target Users

Who will use this system?

# Technology Stack

Use only technologies found in the repository.

# Architecture Summary

Describe the architecture based on the repository.

# Development Status

Summarize current implementation maturity.

# Risks

List realistic technical risks.

# Future Opportunities

List realistic future improvements.

Rules:

- Use repository intelligence
- Use detected components
- Do not invent dates
- Do not invent roadmaps
- Do not invent technologies
- Do not invent users
- Do not write generic startup language
- Be specific to this repository
- Markdown only
- No placeholders
- No AI disclaimers
"""
        content = (
            self._generate(
                prompt
            )
        )
        print(
    self._build_project_context()
)
        return (
            self._save_document(
                "PROJECT_SUMMARY.md",
                content
            )
        )



# For CHANGELOG.md File.
    def generate_changelog(
        self,
        project_name: str
    ) -> str:
        """
        Generate changelog.
        """
        project_context = (
    self._build_project_context()
)
        
        prompt = f"""
Generate CHANGELOG.md.

Project:
{project_name}

Context:
{project_context}

Include:

- Version History
- Major Features
- Improvements
- Bug Fixes
- Security Updates
- Infrastructure Changes
- Known Issues
- Breaking Changes
- Future Releases

Rules:

- Markdown only
- Follow semantic versioning
- No placeholders
- No AI disclaimers
"""
        content = (
            self._generate(
                prompt
            )
        )

        return (
            self._save_document(
                "CHANGELOG.md",
                content
            )
        )
        
        
        
        
        
        
        
# For PROJECT_TREE.md File.
    def generate_project_tree(
        self,
        project_name: str
    ) -> str:
        """
        Generate project tree.
        """
        project_context = (
    self._build_project_context()
)
        
        prompt = f"""
Generate PROJECT_TREE.md.

Project:
{project_name}

Context:
{project_context}

Include:

- Repository Overview
- Complete Project Tree
- Directory Responsibilities
- Core Modules
- Component Relationships
- Execution Flow
- Testing Structure
- Security Structure
- Logging Structure
- Future Repository Evolution

Rules:

- Markdown only
- Reflect actual project structure
- No placeholders
- No AI disclaimers
"""
        content = (
            self._generate(
                prompt
            )
        )

        return (
            self._save_document(
                "PROJECT_TREE.md",
                content
            )
        )

    def generate_all(
        self,
        project_name: str
    ) -> dict:
        """
        Generate all documentation.
        """

        return {

            "README.md":
                self.generate_readme(
                    project_name
                ),

            "ARCHITECTURE.md":
                self.generate_architecture(
                    project_name
                ),

            "API.md":
                self.generate_api_docs(
                    project_name
                ),

            "SETUP.md":
                self.generate_setup_guide(
                    project_name
                ),

            "DEVELOPER_GUIDE.md":
                self.generate_developer_guide(
                    project_name
                ),

            "PROJECT_SUMMARY.md":
                self.generate_project_summary(
                    project_name
                ),

            "CHANGELOG.md":
                self.generate_changelog(
                    project_name
                ),

            "PROJECT_TREE.md":
                self.generate_project_tree(
                    project_name
                )
        }