"""
File: core/analyzers/project_analyzer.py

Purpose:
Analyze and understand
the active project.

Why:

Documentation generation,
planning, coding, testing,
security analysis, memory,
and future autonomous
capabilities require deep
project awareness.

This analyzer converts a
repository into structured
intelligence that can be
consumed by agents,
plugins, MCPs, providers,
and LLMs.

Unlike a simple file scanner,
this analyzer performs:

- Repository discovery
- Code intelligence
- Architecture detection
- Dependency analysis
- Context generation

Architecture:

Active Project
       ↓
ProjectAnalyzer
       ↓
Repository Discovery
       ↓
Code Intelligence
       ↓
Architecture Intelligence
       ↓
Project Context
       ↓
Documentation Plugin
       ↓
Provider Manager
       ↓
LLM

Repository Discovery:

- Project tree
- Source files
- Documentation
- Tests
- Dependencies

Code Intelligence:

- Class extraction
- Function extraction
- Import extraction
- Symbol indexing

Architecture Intelligence:

- Agent detection
- Plugin detection
- Provider detection
- MCP detection
- Manager detection

Context Generation:

- Project summary
- Architecture summary
- Repository context
- Documentation context

Ignored Files:

- .git
- .venv
- venv
- __pycache__
- node_modules
- dist
- build
- coverage
- logs

Ignored Secrets:

- .env
- .env.*
- credentials.json
- secrets.json
- *.key
- *.pem
- *.crt

V1:

- Repository discovery
- Code intelligence
- Architecture extraction
- Context generation

V2:

- Dependency graph engine
- Cross-file relationships

V3:

- Repository intelligence
- Architecture mapping

V4:

- Refactoring intelligence
- Impact analysis

V5:

- Autonomous repository
  understanding

Enterprise:

- Multi-repository analysis
- Repository governance
- Dependency intelligence
- Architecture compliance
- Organization-wide context
"""

from pathlib import Path
import ast
import json



class ProjectAnalyzer:
    """
    Analyze project structure.
    """

    # Ignored directories.
    IGNORE_DIRS = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
        "coverage",
        ".pytest_cache",
        ".mypy_cache",
        "logs"
    }

    # Ignored files.
    IGNORE_FILES = {
        ".env",
        "credentials.json",
        "secrets.json"
    }

    # Ignored extensions.
    IGNORE_EXTENSIONS = {
        ".key",
        ".pem",
        ".crt",
        ".db",
        ".sqlite"
    }

    # Supported source files.
    SOURCE_EXTENSIONS = {
        ".py",
        ".js",
        ".ts",
        ".java",
        ".cpp",
        ".c",
        ".cs",
        ".go",
        ".rs"
    }
    
    
    def __init__(
        self,
        runtime
    ):
        """
        Initialize analyzer.
        """

        self.runtime = runtime


    def should_ignore(
        self,
        path: Path
    ) -> bool:
        """
        Check if path should be ignored.
        """

        # Ignore directories.
        for part in path.parts:

            if part in self.IGNORE_DIRS:

                return True

        # Ignore files.
        if (
            path.name
            in self.IGNORE_FILES
        ):

            return True

        # Ignore .env.*
        if (
            path.name.startswith(
                ".env"
            )
        ):

            return True

        # Ignore secret extensions.
        if (
            path.suffix.lower()
            in self.IGNORE_EXTENSIONS
        ):

            return True

        return False


    
    def collect_key_files(
        self,
        root: Path
    ) -> dict:
        """
        Collect important project files
        and their contents.
        """

        important_files = [

            "README.md",
            "ARCHITECTURE.md",
            "AGENTS.md",
            "MEMORY.md",
            "ROADMAP.md",
            "PROJECT_CONTEXT.md",
            "SECURITY_PROTOCOL.md",
            "SECURITY.md",
            "requirements.txt",
            "pyproject.toml",
            "package.json"
        ]

        results = {}

        for filename in important_files:

            matches = list(
                root.rglob(
                    filename
                )
            )

            if not matches:
                continue

            file = matches[0]

            try:

                content = (
                    file.read_text(
                        encoding="utf-8",
                        errors="ignore"
                    )
                )

                results[
                    str(
                        file.relative_to(
                            root
                        )
                    )
                ] = content[:10000]

            except Exception:

                continue

        return results



    def analyze_project(
        self
    ) -> dict:
        """
        Full project analysis.
        """

        project_path = (
            self.runtime
            .get_active_project()
        )

        if not project_path:

            raise ValueError(
                "No active project set."
            )

        root = Path(
            project_path
        )

        # variable Creation 
        
        code_contents = (
            self.collect_code_contents(
                root
            )
        )
        
        
        classes = (
            self.extract_classes(
            code_contents
            )
        )
        
        
        agents = (
            self.detect_agents(
                classes
        )
    )

        plugins = (
            self.detect_plugins(
                classes
            )
        )

        providers = (
            self.detect_providers(
                classes
            )
        )

        mcps = (
            self.detect_mcps(
                classes
            )
        )
        
        
        tech_stack = (
            self.detect_tech_stack(
                root
            )
        )

        frameworks = (
            self.detect_frameworks(
                root
            )
        )
        
        
        source_files = (
            self.collect_source_files(
                root
            )
        )


        documentation = (
            self.collect_docs(
                root
            )
        )

        tests = (
            self.collect_tests(
                root
            )
        )



        return {

            "project_name":
                root.name,

            "project_path":
                str(root),
                
            "context_files":
                self.collect_key_files(
                    root
                ),

            "tree":
                self.build_project_tree(
                    root
                ),

            "tech_stack":
                tech_stack,

            "frameworks":
                frameworks,

            "source_files":
                source_files,
            
            "code_contents":
                code_contents,
            
            "classes":
                classes,

            "functions":
                self.extract_functions(
                    code_contents
                ),

    

            "imports":
                self.extract_imports(
                    code_contents
                ),

           "agents":
                agents,
                
            "providers":
                providers,
            
            "mcps":
                mcps,

            "plugins":
                plugins,
            
            
            
      
            
            "architecture_summary":
                self.build_architecture_summary(
                    agents,
                    plugins,
                    providers,
                    mcps
                ),
    

            "project_summary":
                self.build_project_summary(
                    root.name,
                    tech_stack,
                    frameworks,
                    agents,
                    plugins,
                    providers
                ),
          
           "documentation":
                documentation,

            "tests":
                tests
            
        }

    def build_project_tree(
        self,
        root: Path,
        max_depth: int = 4
    ) -> str:
        """
        Build ASCII project tree.
        """

        lines = []

        def walk(
            directory,
            prefix="",
            depth=0
        ):

            if depth > max_depth:
                return

            items = sorted(
                directory.iterdir(),
                key=lambda x: (
                    not x.is_dir(),
                    x.name.lower()
                )
            )

            for index, item in enumerate(items):

                connector = (
                    "└── "
                    if index == len(items) - 1
                    else "├── "
                )

                lines.append(
                    f"{prefix}{connector}{item.name}"
                )

                if item.is_dir():

                    extension = (
                        "    "
                        if index == len(items) - 1
                        else "│   "
                    )

                    walk(
                        item,
                        prefix + extension,
                        depth + 1
                    )

        lines.append(
            root.name
        )

        walk(root)

        return "\n".join(
            lines
        )

    def detect_tech_stack(
        self,
        root: Path
    ) -> list:
        """
        Detect technologies.
        """

        stack = []

        files = {
            p.name.lower()
            for p in root.rglob("*")
        }

        if "requirements.txt" in files:
            stack.append(
                "Python"
            )

        if "pyproject.toml" in files:
            stack.append(
                "Python"
            )

        if "package.json" in files:
            stack.append(
                "Node.js"
            )

        if "dockerfile" in files:
            stack.append(
                "Docker"
            )

        if ".github" in str(files):
            stack.append(
                "GitHub Actions"
            )

        return sorted(
            set(stack)
        )

    def detect_frameworks(
        self,
        root: Path
    ) -> list:
        """
        Detect frameworks.
        """

        frameworks = []

        requirements = (
            root
            / "requirements.txt"
        )

        if requirements.exists():

            content = (
                requirements
                .read_text(
                    encoding="utf-8",
                    errors="ignore"
                )
                .lower()
            )

            checks = {

                "flask":
                    "Flask",

                "fastapi":
                    "FastAPI",

                "django":
                    "Django",

                "streamlit":
                    "Streamlit",

                "sqlalchemy":
                    "SQLAlchemy",

                "pytest":
                    "Pytest"
            }

            for key, value in checks.items():

                if key in content:

                    frameworks.append(
                        value
                    )

        return frameworks

    def collect_source_files(
        self,
        root: Path
    ) -> list:
        """
        Collect source files.
        """

        extensions = {

            ".py",
            ".js",
            ".ts",
            ".java",
            ".cpp",
            ".c",
            ".cs",
            ".go",
            ".rs"
        }

        files = []

        for file in root.rglob("*"):
            if self.should_ignore(
                file
            ):
                continue

            if (
                file.is_file()
                and file.suffix.lower()
                in extensions
            ):

                files.append(
                    str(
                        file.relative_to(
                            root
                        )
                    )
                )

        return files
    
    
    
    def collect_code_contents(
        self,
        root: Path,
        max_chars: int = 500
    ) -> dict:
        """
        Collect source code contents.
        """

        results = {}

        for file in root.rglob("*"):

            # Skip ignored files.
            if self.should_ignore(
                file
            ):
                continue

            # Skip non-files.
            if not file.is_file():
                continue

            # Skip unsupported files.
            if (
                file.suffix.lower()
                not in self.SOURCE_EXTENSIONS
            ):
                continue

            try:

                content = (
                    file.read_text(
                        encoding="utf-8",
                        errors="ignore"
                    )
                )

                results[
                    str(
                        file.relative_to(
                            root
                        )
                    )
                ] = content[:max_chars]

            except Exception:

                continue

        return results
    
    
    
    
    def extract_classes(
        self,
        code_contents: dict
    ) -> list:
        """
        Extract classes.
        """

        classes = []

        for file_path, content in (
            code_contents.items()
        ):

            try:

                tree = ast.parse(
                    content
                )

                for node in ast.walk(
                    tree
                ):

                    if isinstance(
                        node,
                        ast.ClassDef
                    ):

                        classes.append(
                            {
                                "name":
                                    node.name,

                                "file":
                                    file_path
                            }
                        )

            except Exception:

                continue

        return classes
    
    
    def extract_functions(
        self,
        code_contents: dict
    ) -> list:
        """
        Extract functions.
        """

        functions = []

        for file_path, content in (
            code_contents.items()
        ):

            try:

                tree = ast.parse(
                    content
                )

                for node in ast.walk(
                    tree
                ):

                    if isinstance(
                        node,
                        ast.FunctionDef
                    ):

                        functions.append(
                            {
                                "name":
                                    node.name,

                                "file":
                                    file_path
                            }
                        )

            except Exception:

                continue

        return functions

        
    def extract_imports(
        self,
        code_contents: dict
    ) -> list:
        """
        Extract imports.
        """

        imports = []

        for file_path, content in (
            code_contents.items()
        ):

            try:

                tree = ast.parse(
                    content
                )

                for node in ast.walk(
                    tree
                ):

                    # import x
                    if isinstance(
                        node,
                        ast.Import
                    ):

                        for name in (
                            node.names
                        ):

                            imports.append(
                                {
                                    "module":
                                        name.name,

                                    "file":
                                        file_path
                                }
                            )

                    # from x import y
                    elif isinstance(
                        node,
                        ast.ImportFrom
                    ):

                        imports.append(
                            {
                                "module":
                                    (
                                        node.module
                                        or ""
                                    ),

                                "file":
                                    file_path
                            }
                        )

            except Exception:

                continue

        return imports   
        
        
        
    def detect_agents(
        self,
        classes: list
    ) -> list:
        """
        Detect agents.
        """

        agents = []

        for item in classes:

            class_name = (
                item["name"]
            )

            file_name = (
                item["file"]
            )

            if (
                "agent"
                in class_name.lower()
            ):

                agents.append(
                    {
                        "name":
                            class_name,

                        "file":
                            file_name,

                        "type":
                            "agent"
                    }
                )

        return agents
    
    
    
    def detect_plugins(
        self,
        classes: list
    ) -> list:
        """
        Detect plugins.
        """

        plugins = []

        for item in classes:

            class_name = (
                item["name"]
            )

            file_name = (
                item["file"]
            )

            if (
                "plugin"
                in class_name.lower()
            ):

                plugins.append(
                    {
                        "name":
                            class_name,

                        "file":
                            file_name,

                        "type":
                            "plugin"
                    }
                )

        return plugins



    
    def detect_providers(
        self,
        classes: list
    ) -> list:
        """
        Detect providers.
        """

        providers = []

        for item in classes:

            class_name = (
                item["name"]
            )

            file_name = (
                item["file"]
            )

            if (
                "provider"
                in class_name.lower()
            ):

                providers.append(
                    {
                        "name":
                            class_name,

                        "file":
                            file_name,

                        "type":
                            "provider"
                    }
                )

        return providers
    
    
    def detect_mcps(
        self,
        classes: list
    ) -> list:
        """
        Detect MCPs.
        """

        mcps = []

        for item in classes:

            class_name = (
                item["name"]
            )

            file_name = (
                item["file"]
            )

            if (
                "mcp"
                in class_name.lower()
            ):

                mcps.append(
                    {
                        "name":
                            class_name,

                        "file":
                            file_name,

                        "type":
                            "mcp"
                    }
                )

        return mcps
    
    
    
    def build_architecture_summary(
        self,
        agents: list,
        plugins: list,
        providers: list,
        mcps: list
    ) -> str:
        """
        Build architecture summary.
        """

        summary = []

        # Agents.
        if agents:

            summary.append(
                f"Agents: {len(agents)}"
            )

        # Plugins.
        if plugins:

            summary.append(
                f"Plugins: {len(plugins)}"
            )

        # Providers.
        if providers:

            summary.append(
                f"Providers: {len(providers)}"
            )

        # MCPs.
        if mcps:

            summary.append(
                f"MCPs: {len(mcps)}"
            )

        if not summary:

            return (
                "No architecture "
                "components detected."
            )

        return " | ".join(
            summary
        )
    
    
    
    
    def build_project_summary(
        self,
        project_name: str,
        tech_stack: list,
        frameworks: list,
        agents: list,
        plugins: list,
        providers: list
    ) -> str:
        """
        Build project summary.
        """

        return (
            f"Project: {project_name} | "
            f"Tech Stack: {len(tech_stack)} | "
            f"Frameworks: {len(frameworks)} | "
            f"Agents: {len(agents)} | "
            f"Plugins: {len(plugins)} | "
            f"Providers: {len(providers)}"
        )
        
        
    def collect_docs(
        self,
        root: Path
    ) -> list:
        """
        Collect documentation.
        """

        docs = []

        for file in root.rglob("*.md"):

            docs.append(
                str(
                    file.relative_to(
                        root
                    )
                )
            )

        return docs

    def collect_tests(
        self,
        root: Path
    ) -> list:
        """
        Collect test files.
        """

        tests = []

        for file in root.rglob("*"):

            if not file.is_file():
                continue

            if (
                "test"
                in file.name.lower()
            ):

                tests.append(
                    str(
                        file.relative_to(
                            root
                        )
                    )
                )

        return tests

    def get_context_json(
        self
    ) -> str:
        """
        Return optimized
        project context.
        """

        context = (
            self.analyze_project()
        )

        # Prevent huge prompts.
        if (
            "code_contents"
            in context
        ):

            trimmed = {}

            for (
                file,
                content
            ) in (
                context[
                    "code_contents"
                ]
                .items()
            ):

                trimmed[
                    file
                ] = content[:2000]

            context[
                "code_contents"
            ] = trimmed

        return json.dumps(
            context,
            indent=4
        )
