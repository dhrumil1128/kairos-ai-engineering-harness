"""
File: core/architecture/templates.py

Purpose:
Deterministic, framework-specific project structure definitions.

Registering a new framework (FastAPI, Django, React, Next.js,
Express, CLI, Library, ...) requires ONLY adding a new
FrameworkTemplate entry to this file - no changes to
ArchitectAgent, detector.py, or builder.py.

Templates MUST be generic. Never hardcode project-specific names
here (e.g. student_api.py, hospital.py, inventory.py). Only
reusable framework structure, parameterized by package_name.
"""

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class FrameworkTemplate:
    """
    A deterministic, reusable project skeleton for a framework.
    """

    # Canonical internal name, e.g. "flask", "generic_python".
    name: str

    # Strings the LLM might return for `framework` / `project_type`
    # that should resolve to this template. Matching is normalized
    # (lowercased, non-alnum -> "_") - see detector.py.
    aliases: tuple[str, ...]

    # (package_name) -> list of directories, relative paths.
    directories: Callable[[str], list[str]]

    # (package_name) -> list of files, relative paths.
    files: Callable[[str], list[str]]

    # Dependencies this framework always needs, regardless of what
    # the LLM suggests (e.g. ("flask",)).
    mandatory_requirements: tuple[str, ...] = field(default_factory=tuple)
    entry_module: str = "main.py"

    entry_function: str | None = None

    code_style: str = "standard"

    supports_dependency_injection: bool = False

    supports_blueprints: bool = False
    
    metadata: dict = field(default_factory=dict)
    
    generation_rules: dict = field(default_factory=dict)
    
    validation_rules: dict = field(default_factory=dict)
    
    coding_conventions: dict = field(default_factory=dict)
    
    import_rules: dict = field(default_factory=dict)
    
    file_responsibilities: dict[str, str] = field(default_factory=dict)

    # Whether to also emit a self-named module: package/package.py
    # (or package/<self_named_module_filename> if set). Frameworks
    # with their own canonical entry surface (routes.py, app.py,
    # manage.py, ...) typically set this to False.
    include_self_named_module: bool = True
    self_named_module_filename: str | None = None  # e.g. "app.py"


# ---------------------------------------------------------------------------
# Generic (fallback) template
#
# Used for CLI tools, libraries, or any framework the LLM names that
# has no registered template. This preserves today's baseline
# behavior exactly.
# ---------------------------------------------------------------------------

def _generic_directories(package_name: str) -> list[str]:
    return ["src", "tests", "docs", package_name]


def _generic_files(package_name: str) -> list[str]:
    return [
        "src/main.py",
        f"{package_name}/__init__.py",
        "tests/test_main.py",
        "docs/README.md",
    ]


GENERIC_TEMPLATE = FrameworkTemplate(
    name="generic_python",
    aliases=(),
    directories=_generic_directories,
    files=_generic_files,
    mandatory_requirements=(),
    include_self_named_module=True,

    entry_module="main.py",
    entry_function="main",
    code_style="standard",
    supports_dependency_injection=False,
    supports_blueprints=False,
    metadata={
    "architecture": "generic",
},
    generation_rules={
    "generate_tests": True,
    "generate_docs": True,
    "generate_type_hints": False,
},
    validation_rules={
    "require_init_file": True,
    "require_entry_point": True,
    "require_tests": True,
},
    
    coding_conventions={
    "class_naming": "PascalCase",
    "function_naming": "snake_case",
    "variable_naming": "snake_case",
    "constant_naming": "UPPER_CASE",
},
    
    import_rules={
    "prefer_absolute_imports": True,
    "allow_relative_imports": False,
}
)


# ---------------------------------------------------------------------------
# Single-file Python script
# ---------------------------------------------------------------------------

def _single_file_directories(package_name: str) -> list[str]:
    return []


def _single_file_files(package_name: str) -> list[str]:
    return ["main.py"]


SINGLE_FILE_PYTHON_TEMPLATE = FrameworkTemplate(
    name="single_file_python",
    aliases=(
        "single_file",
        "single_file_script",
        "one_file",
        "one_file_script",
        "python_file",
        "python_script",
        "script",
        "hello_world",
    ),
    directories=_single_file_directories,
    files=_single_file_files,
    mandatory_requirements=(),
    include_self_named_module=False,
    entry_module="main.py",
    entry_function=None,
    code_style="script",
    supports_dependency_injection=False,
    supports_blueprints=False,
    metadata={
        "architecture": "single_file",
    },
    generation_rules={
        "generate_tests": False,
        "generate_docs": False,
        "generate_type_hints": False,
    },
    validation_rules={
        "require_entry_point": True,
        "require_tests": False,
    },
    coding_conventions={
        "function_naming": "snake_case",
        "variable_naming": "snake_case",
        "constant_naming": "UPPER_CASE",
    },
    import_rules={
        "prefer_absolute_imports": True,
        "allow_relative_imports": False,
    },
)


# ---------------------------------------------------------------------------
# Flask
# ---------------------------------------------------------------------------

def _flask_directories(package_name: str) -> list[str]:
    return ["src", "tests", "docs", package_name]


def _flask_files(package_name: str) -> list[str]:
    return [
        f"{package_name}/__init__.py",
        f"{package_name}/config.py",
        f"{package_name}/database.py",
        f"{package_name}/models.py",
        f"{package_name}/schemas.py",
        f"{package_name}/services.py",
        f"{package_name}/routes.py",
        "src/main.py",
        "tests/test_main.py",
        "docs/README.md",
    ]


FLASK_TEMPLATE = FrameworkTemplate(
    name="flask",
    aliases=("flask", "flask-restful", "flask-restx", "flask_api", "flask_rest"),
    directories=_flask_directories,
    files=_flask_files,
    mandatory_requirements=("flask",),
    include_self_named_module=False,

    entry_module="app.py",
    entry_function="create_app",
    code_style="flask",
    supports_dependency_injection=False,
    supports_blueprints=True,

    metadata={
        "architecture": "mvc",
        "router_file": "routes.py",
        "model_file": "models.py",
        "service_file": "services.py",
        "schema_file": "schemas.py",
        "database_file": "database.py",
        "config_file": "config.py",
        
    },
    
    generation_rules={
    "generate_tests": True,
    "generate_docs": True,
    "generate_type_hints": True,
    "use_application_factory": True,
},
    
    validation_rules={
    "require_init_file": True,
    "require_entry_point": True,
    "require_tests": True,
    "require_routes": True,
    "require_models": True,
    "require_services": True,
    "require_schemas": True,
},
    
    coding_conventions={
    "class_naming": "PascalCase",
    "function_naming": "snake_case",
    "variable_naming": "snake_case",
    "constant_naming": "UPPER_CASE",
    "route_style": "blueprint",
},
    import_rules={
    "prefer_absolute_imports": True,
    "allow_relative_imports": False,
    "blueprint_import_style": "package",
},
    file_responsibilities={
        "src/main.py": (
            "Application entry point. Create the Flask app, register the "
            "route blueprint, initialize the database on startup, and keep "
            "business logic out of this file."
        ),
        "{package}/__init__.py": (
            "Package initialization only. Expose public application APIs with "
            "explicit imports when needed."
        ),
        "{package}/config.py": (
            "Define typed configuration values, including the SQLite database "
            "path and runtime settings. Do not perform I/O here."
        ),
        "{package}/database.py": (
            "Own database connection and initialization. Create all required "
            "SQLite tables automatically on first run and expose reusable "
            "connection helpers."
        ),
        "{package}/models.py": (
            "Define persistence models or repository data structures only. "
            "Do not implement route handlers or HTTP behavior."
        ),
        "{package}/schemas.py": (
            "Define request and response validation/serialization helpers "
            "used by routes and services. Do not access Flask globals here."
        ),
        "{package}/services.py": (
            "Implement complete business logic. Use models, schemas, config, "
            "and database helpers. Do not define Flask routes here."
        ),
        "{package}/routes.py": (
            "Define Flask blueprint routes only. Validate request/response "
            "payloads with schemas and delegate all business operations to "
            "services."
        ),
        "tests/test_main.py": (
            "Create executable tests for route behavior, service delegation, "
            "schema validation, and database initialization."
        ),
        "docs/README.md": (
            "Generate complete documentation covering overview, architecture, "
            "installation, requirements, database initialization, usage "
            "examples, testing, and project structure."
        ),
    },
)

# ---------------------------------------------------------------------------
# Click
# ---------------------------------------------------------------------------

CLICK_TEMPLATE = FrameworkTemplate(
    name="click",
    aliases=(
        "click",
        "cli",
        "cli_calculator",
        "cli_application",
    ),
    directories=_generic_directories,
    files=_generic_files,
    mandatory_requirements=("click",),
    include_self_named_module=True,

    entry_module="main.py",
    entry_function="main",
    code_style="click",
    supports_dependency_injection=False,
    supports_blueprints=False,

    metadata={
        "architecture": "cli",
    },

    generation_rules={
        "generate_tests": True,
        "generate_docs": True,
        "generate_type_hints": False,
    },

    validation_rules={
        "require_init_file": True,
        "require_entry_point": True,
        "require_tests": True,
    },

    coding_conventions={
        "class_naming": "PascalCase",
        "function_naming": "snake_case",
        "variable_naming": "snake_case",
        "constant_naming": "UPPER_CASE",
    },

    import_rules={
        "prefer_absolute_imports": True,
        "allow_relative_imports": False,
    },
    
    file_responsibilities={
    "src/main.py": (
        "Application entry point. Register all Click commands, "
        "validate user input, delegate work to the package module, "
        "and keep business logic out of this file."
    ),

    "__init__.py": (
        "Package initialization only. Do not place business logic here."
    ),

    "{package}.py": (
        "Implement the complete business logic for the application. "
        "Do not perform CLI interaction. "
        "Expose reusable functions used by the CLI."
    ),

    "tests/test_main.py": (
        "Create executable tests covering all public CLI commands, "
        "successful cases, invalid input, edge cases, and expected failures."
    ),

    "docs/README.md": (
        "Generate complete documentation including installation, "
        "requirements, usage, examples, testing instructions, "
        "and project structure."
    ),
},
    
)


# ---------------------------------------------------------------------------
# FastAPI
# ---------------------------------------------------------------------------

def _fastapi_directories(package_name: str) -> list[str]:
    return [
        "app",
        "app/routes",
        "app/services",
        "app/models",
        "app/schemas",
        "app/database",
        "app/config",
        "app/utils",
        "tests",
        "docs",
    ]


def _fastapi_files(package_name: str) -> list[str]:
    return [
        "app/__init__.py",
        "app/database/__init__.py",
        "app/database/session.py",
        "app/config/__init__.py",
        "app/config/settings.py",
        "app/models/__init__.py",
        "app/models/task.py",
        "app/schemas/__init__.py",
        "app/schemas/task.py",
        "app/services/__init__.py",
        "app/services/task_service.py",
        "app/routes/__init__.py",
        "app/routes/task_routes.py",
        "app/utils/__init__.py",
        "main.py",
        "tests/test_main.py",
        "requirements.txt",
        ".gitignore",
        "README.md",
    ]


FASTAPI_TEMPLATE = FrameworkTemplate(
    name="fastapi",
    aliases=(
        "fastapi",
        "fast_api",
        "fastapi_api",
        "fastapi_rest",
        "fastapi_rest_api",
        "rest_api",
        "python_rest_api",
        "api",
    ),
    directories=_fastapi_directories,
    files=_fastapi_files,
    mandatory_requirements=(
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "pydantic-settings",
    ),
    include_self_named_module=False,
    entry_module="main.py",
    entry_function="app",
    code_style="fastapi",
    supports_dependency_injection=True,
    supports_blueprints=True,
    metadata={
        "architecture": "clean",
        "router_file": "app/routes",
        "model_file": "app/models",
        "service_file": "app/services",
        "schema_file": "app/schemas",
        "database_file": "app/database",
        "config_file": "app/config",
    },
    generation_rules={
        "generate_tests": True,
        "generate_docs": True,
        "generate_type_hints": True,
        "use_dependency_injection": True,
        "use_openapi": True,
    },
    validation_rules={
        "require_entry_point": True,
        "require_routes": True,
        "require_models": True,
        "require_schemas": True,
        "require_services": True,
        "require_tests": True,
    },
    coding_conventions={
        "class_naming": "PascalCase",
        "function_naming": "snake_case",
        "variable_naming": "snake_case",
        "constant_naming": "UPPER_CASE",
        "route_style": "apirouter",
    },
    import_rules={
        "prefer_absolute_imports": True,
        "allow_relative_imports": False,
    },
    file_responsibilities={
        "main.py": (
            "FastAPI entry point. Create the app, include routers, initialize "
            "the database on startup, and keep business logic out of this file."
        ),
        "app/database/session.py": (
            "Own database engine/session creation and initialization. Create "
            "all required SQLite tables automatically on first run."
        ),
        "app/config/settings.py": (
            "Define typed application settings, including database URL/path. "
            "Do not perform database I/O here."
        ),
        "app/models/task.py": (
            "Define database models only. Do not implement API route logic."
        ),
        "app/schemas/task.py": (
            "Define Pydantic request and response schemas used by routes and "
            "services."
        ),
        "app/services/task_service.py": (
            "Implement business logic and persistence operations. Use database "
            "helpers, models, and schemas. Do not define API routes here."
        ),
        "app/routes/task_routes.py": (
            "Define APIRouter endpoints only. Use schemas for request/response "
            "contracts and delegate all business operations to services."
        ),
        "tests/test_main.py": (
            "Create executable tests for API behavior, service delegation, "
            "schema usage, and database initialization."
        ),
        "README.md": (
            "Generate complete documentation covering overview, architecture, "
            "installation, requirements, database initialization, usage "
            "examples, testing, and project structure."
        ),
    },
)


# ---------------------------------------------------------------------------
# Django
# ---------------------------------------------------------------------------

def _django_directories(package_name: str) -> list[str]:
    return [
        package_name,
        "apps",
        "apps/core",
        "apps/core/migrations",
        "templates",
        "static",
        "tests",
        "docs",
    ]


def _django_files(package_name: str) -> list[str]:
    return [
        "manage.py",
        f"{package_name}/__init__.py",
        f"{package_name}/settings.py",
        f"{package_name}/urls.py",
        f"{package_name}/asgi.py",
        f"{package_name}/wsgi.py",
        "apps/__init__.py",
        "apps/core/__init__.py",
        "apps/core/admin.py",
        "apps/core/apps.py",
        "apps/core/models.py",
        "apps/core/serializers.py",
        "apps/core/services.py",
        "apps/core/views.py",
        "apps/core/urls.py",
        "apps/core/migrations/__init__.py",
        "tests/test_main.py",
        "requirements.txt",
        ".gitignore",
        "README.md",
    ]


DJANGO_TEMPLATE = FrameworkTemplate(
    name="django",
    aliases=("django", "django_rest", "django_rest_framework", "drf"),
    directories=_django_directories,
    files=_django_files,
    mandatory_requirements=("django", "djangorestframework"),
    include_self_named_module=False,
    entry_module="manage.py",
    entry_function=None,
    code_style="django",
    supports_dependency_injection=False,
    supports_blueprints=True,
    metadata={"architecture": "django_mvt"},
    generation_rules={
        "generate_tests": True,
        "generate_docs": True,
        "generate_type_hints": True,
    },
    validation_rules={
        "require_entry_point": True,
        "require_models": True,
        "require_routes": True,
        "require_tests": True,
    },
    coding_conventions={
        "class_naming": "PascalCase",
        "function_naming": "snake_case",
        "variable_naming": "snake_case",
        "constant_naming": "UPPER_CASE",
    },
    import_rules={
        "prefer_absolute_imports": True,
        "allow_relative_imports": False,
    },
)


# ---------------------------------------------------------------------------
# Typer
# ---------------------------------------------------------------------------

TYPER_TEMPLATE = FrameworkTemplate(
    name="typer",
    aliases=("typer", "typer_cli", "python_cli"),
    directories=_generic_directories,
    files=_generic_files,
    mandatory_requirements=("typer",),
    include_self_named_module=True,
    entry_module="main.py",
    entry_function="app",
    code_style="typer",
    supports_dependency_injection=False,
    supports_blueprints=False,
    metadata={"architecture": "cli"},
    generation_rules={
        "generate_tests": True,
        "generate_docs": True,
        "generate_type_hints": True,
    },
    validation_rules={
        "require_init_file": True,
        "require_entry_point": True,
        "require_tests": True,
    },
    coding_conventions={
        "class_naming": "PascalCase",
        "function_naming": "snake_case",
        "variable_naming": "snake_case",
        "constant_naming": "UPPER_CASE",
    },
    import_rules={
        "prefer_absolute_imports": True,
        "allow_relative_imports": False,
    },
)


# ---------------------------------------------------------------------------
# Frontend and Node.js frameworks
# ---------------------------------------------------------------------------

def _frontend_directories(package_name: str) -> list[str]:
    return [
        "src",
        "src/components",
        "src/pages",
        "src/hooks",
        "src/services",
        "src/styles",
        "public",
        "tests",
        "docs",
    ]


def _react_files(package_name: str) -> list[str]:
    return [
        "index.html",
        "src/main.jsx",
        "src/App.jsx",
        "src/components/.gitkeep",
        "src/pages/Home.jsx",
        "src/hooks/.gitkeep",
        "src/services/.gitkeep",
        "src/styles/global.css",
        "public/.gitkeep",
        "tests/App.test.jsx",
        "package.json",
        ".gitignore",
        "README.md",
    ]


REACT_TEMPLATE = FrameworkTemplate(
    name="react",
    aliases=("react", "reactjs", "react_app", "vite_react", "spa"),
    directories=_frontend_directories,
    files=_react_files,
    mandatory_requirements=("react", "react-dom", "vite"),
    include_self_named_module=False,
    entry_module="src/main.jsx",
    entry_function=None,
    code_style="react",
    supports_dependency_injection=False,
    supports_blueprints=False,
    metadata={"architecture": "component_based"},
    generation_rules={
        "generate_tests": True,
        "generate_docs": True,
        "generate_type_hints": False,
    },
    validation_rules={
        "require_entry_point": True,
        "require_tests": True,
    },
    coding_conventions={
        "class_naming": "PascalCase",
        "function_naming": "camelCase",
        "variable_naming": "camelCase",
        "constant_naming": "UPPER_CASE",
        "component_naming": "PascalCase",
    },
    import_rules={
        "prefer_absolute_imports": False,
        "allow_relative_imports": True,
    },
)


def _nextjs_directories(package_name: str) -> list[str]:
    return [
        "app",
        "app/api",
        "components",
        "lib",
        "public",
        "styles",
        "tests",
        "docs",
    ]


def _nextjs_files(package_name: str) -> list[str]:
    return [
        "app/layout.jsx",
        "app/page.jsx",
        "app/api/health/route.js",
        "components/.gitkeep",
        "lib/.gitkeep",
        "public/.gitkeep",
        "styles/globals.css",
        "tests/page.test.jsx",
        "package.json",
        "next.config.js",
        ".gitignore",
        "README.md",
    ]


NEXTJS_TEMPLATE = FrameworkTemplate(
    name="nextjs",
    aliases=("next", "nextjs", "next.js", "next_app", "nextjs_app"),
    directories=_nextjs_directories,
    files=_nextjs_files,
    mandatory_requirements=("next", "react", "react-dom"),
    include_self_named_module=False,
    entry_module="app/page.jsx",
    entry_function=None,
    code_style="nextjs",
    supports_dependency_injection=False,
    supports_blueprints=True,
    metadata={"architecture": "app_router"},
    generation_rules={
        "generate_tests": True,
        "generate_docs": True,
        "generate_type_hints": False,
    },
    validation_rules={
        "require_entry_point": True,
        "require_routes": True,
        "require_tests": True,
    },
    coding_conventions={
        "class_naming": "PascalCase",
        "function_naming": "camelCase",
        "variable_naming": "camelCase",
        "constant_naming": "UPPER_CASE",
        "component_naming": "PascalCase",
    },
    import_rules={
        "prefer_absolute_imports": True,
        "allow_relative_imports": True,
    },
)


def _express_directories(package_name: str) -> list[str]:
    return [
        "src",
        "src/routes",
        "src/controllers",
        "src/services",
        "src/models",
        "src/middleware",
        "src/config",
        "src/utils",
        "tests",
        "docs",
    ]


def _express_files(package_name: str) -> list[str]:
    return [
        "src/server.js",
        "src/app.js",
        "src/routes/index.js",
        "src/controllers/.gitkeep",
        "src/services/.gitkeep",
        "src/models/.gitkeep",
        "src/middleware/.gitkeep",
        "src/config/index.js",
        "src/utils/.gitkeep",
        "tests/app.test.js",
        "package.json",
        ".gitignore",
        "README.md",
    ]


EXPRESS_TEMPLATE = FrameworkTemplate(
    name="express",
    aliases=("express", "expressjs", "node", "nodejs", "node_api", "express_api"),
    directories=_express_directories,
    files=_express_files,
    mandatory_requirements=("express",),
    include_self_named_module=False,
    entry_module="src/server.js",
    entry_function=None,
    code_style="express",
    supports_dependency_injection=False,
    supports_blueprints=True,
    metadata={"architecture": "mvc"},
    generation_rules={
        "generate_tests": True,
        "generate_docs": True,
        "generate_type_hints": False,
    },
    validation_rules={
        "require_entry_point": True,
        "require_routes": True,
        "require_tests": True,
    },
    coding_conventions={
        "class_naming": "PascalCase",
        "function_naming": "camelCase",
        "variable_naming": "camelCase",
        "constant_naming": "UPPER_CASE",
    },
    import_rules={
        "prefer_absolute_imports": False,
        "allow_relative_imports": True,
    },
)


def _nestjs_directories(package_name: str) -> list[str]:
    return [
        "src",
        "src/modules",
        "src/common",
        "src/config",
        "test",
        "docs",
    ]


def _nestjs_files(package_name: str) -> list[str]:
    return [
        "src/main.ts",
        "src/app.module.ts",
        "src/app.controller.ts",
        "src/app.service.ts",
        "src/modules/.gitkeep",
        "src/common/.gitkeep",
        "src/config/.gitkeep",
        "test/app.e2e-spec.ts",
        "package.json",
        "tsconfig.json",
        ".gitignore",
        "README.md",
    ]


NESTJS_TEMPLATE = FrameworkTemplate(
    name="nestjs",
    aliases=("nestjs", "nest", "nest.js", "node_typescript_api"),
    directories=_nestjs_directories,
    files=_nestjs_files,
    mandatory_requirements=("@nestjs/common", "@nestjs/core", "@nestjs/platform-express"),
    include_self_named_module=False,
    entry_module="src/main.ts",
    entry_function="bootstrap",
    code_style="nestjs",
    supports_dependency_injection=True,
    supports_blueprints=True,
    metadata={"architecture": "modular"},
    generation_rules={
        "generate_tests": True,
        "generate_docs": True,
        "generate_type_hints": True,
    },
    validation_rules={
        "require_entry_point": True,
        "require_routes": True,
        "require_tests": True,
    },
    coding_conventions={
        "class_naming": "PascalCase",
        "function_naming": "camelCase",
        "variable_naming": "camelCase",
        "constant_naming": "UPPER_CASE",
    },
    import_rules={
        "prefer_absolute_imports": True,
        "allow_relative_imports": True,
    },
)


def _vue_files(package_name: str) -> list[str]:
    return [
        "index.html",
        "src/main.js",
        "src/App.vue",
        "src/components/.gitkeep",
        "src/pages/Home.vue",
        "src/services/.gitkeep",
        "src/styles/global.css",
        "public/.gitkeep",
        "tests/App.test.js",
        "package.json",
        ".gitignore",
        "README.md",
    ]


VUE_TEMPLATE = FrameworkTemplate(
    name="vue",
    aliases=("vue", "vuejs", "vue_app", "vite_vue"),
    directories=_frontend_directories,
    files=_vue_files,
    mandatory_requirements=("vue", "vite"),
    include_self_named_module=False,
    entry_module="src/main.js",
    entry_function=None,
    code_style="vue",
    supports_dependency_injection=False,
    supports_blueprints=False,
    metadata={"architecture": "component_based"},
    generation_rules={
        "generate_tests": True,
        "generate_docs": True,
        "generate_type_hints": False,
    },
    validation_rules={
        "require_entry_point": True,
        "require_tests": True,
    },
    coding_conventions={
        "class_naming": "PascalCase",
        "function_naming": "camelCase",
        "variable_naming": "camelCase",
        "constant_naming": "UPPER_CASE",
        "component_naming": "PascalCase",
    },
    import_rules={
        "prefer_absolute_imports": False,
        "allow_relative_imports": True,
    },
)


def _svelte_files(package_name: str) -> list[str]:
    return [
        "src/main.js",
        "src/App.svelte",
        "src/components/.gitkeep",
        "src/pages/Home.svelte",
        "src/services/.gitkeep",
        "src/styles/global.css",
        "public/.gitkeep",
        "tests/App.test.js",
        "package.json",
        "vite.config.js",
        ".gitignore",
        "README.md",
    ]


SVELTE_TEMPLATE = FrameworkTemplate(
    name="svelte",
    aliases=("svelte", "sveltekit", "svelte_app", "vite_svelte"),
    directories=_frontend_directories,
    files=_svelte_files,
    mandatory_requirements=("svelte", "vite"),
    include_self_named_module=False,
    entry_module="src/main.js",
    entry_function=None,
    code_style="svelte",
    supports_dependency_injection=False,
    supports_blueprints=False,
    metadata={"architecture": "component_based"},
    generation_rules={
        "generate_tests": True,
        "generate_docs": True,
        "generate_type_hints": False,
    },
    validation_rules={
        "require_entry_point": True,
        "require_tests": True,
    },
    coding_conventions={
        "class_naming": "PascalCase",
        "function_naming": "camelCase",
        "variable_naming": "camelCase",
        "constant_naming": "UPPER_CASE",
        "component_naming": "PascalCase",
    },
    import_rules={
        "prefer_absolute_imports": False,
        "allow_relative_imports": True,
    },
)


# ---------------------------------------------------------------------------
# Common backend frameworks
# ---------------------------------------------------------------------------

def _spring_boot_directories(package_name: str) -> list[str]:
    package_path = package_name.replace("_", "/")
    return [
        f"src/main/java/{package_path}",
        f"src/main/java/{package_path}/controller",
        f"src/main/java/{package_path}/service",
        f"src/main/java/{package_path}/model",
        f"src/main/java/{package_path}/repository",
        "src/main/resources",
        "src/test/java",
        "docs",
    ]


def _spring_boot_files(package_name: str) -> list[str]:
    package_path = package_name.replace("_", "/")
    class_name = "".join(part.title() for part in package_name.split("_"))
    return [
        f"src/main/java/{package_path}/{class_name}Application.java",
        f"src/main/java/{package_path}/controller/.gitkeep",
        f"src/main/java/{package_path}/service/.gitkeep",
        f"src/main/java/{package_path}/model/.gitkeep",
        f"src/main/java/{package_path}/repository/.gitkeep",
        "src/main/resources/application.properties",
        "src/test/java/.gitkeep",
        "pom.xml",
        ".gitignore",
        "README.md",
    ]


SPRING_BOOT_TEMPLATE = FrameworkTemplate(
    name="spring_boot",
    aliases=("spring", "spring_boot", "springboot", "java_api"),
    directories=_spring_boot_directories,
    files=_spring_boot_files,
    mandatory_requirements=("spring-boot-starter-web",),
    include_self_named_module=False,
    entry_module="src/main/java",
    entry_function="main",
    code_style="spring_boot",
    supports_dependency_injection=True,
    supports_blueprints=True,
    metadata={"architecture": "layered"},
    generation_rules={
        "generate_tests": True,
        "generate_docs": True,
        "generate_type_hints": True,
    },
    validation_rules={
        "require_entry_point": True,
        "require_routes": True,
        "require_tests": True,
    },
    coding_conventions={
        "class_naming": "PascalCase",
        "function_naming": "camelCase",
        "variable_naming": "camelCase",
        "constant_naming": "UPPER_CASE",
    },
    import_rules={
        "prefer_absolute_imports": True,
        "allow_relative_imports": False,
    },
)


def _laravel_directories(package_name: str) -> list[str]:
    return [
        "app/Http/Controllers",
        "app/Models",
        "app/Services",
        "database/migrations",
        "routes",
        "tests/Feature",
        "tests/Unit",
        "docs",
    ]


def _laravel_files(package_name: str) -> list[str]:
    return [
        "app/Http/Controllers/.gitkeep",
        "app/Models/.gitkeep",
        "app/Services/.gitkeep",
        "database/migrations/.gitkeep",
        "routes/api.php",
        "routes/web.php",
        "tests/Feature/.gitkeep",
        "tests/Unit/.gitkeep",
        "composer.json",
        ".env.example",
        ".gitignore",
        "README.md",
    ]


LARAVEL_TEMPLATE = FrameworkTemplate(
    name="laravel",
    aliases=("laravel", "php_laravel", "laravel_api", "php_api"),
    directories=_laravel_directories,
    files=_laravel_files,
    mandatory_requirements=("laravel/framework",),
    include_self_named_module=False,
    entry_module="public/index.php",
    entry_function=None,
    code_style="laravel",
    supports_dependency_injection=True,
    supports_blueprints=True,
    metadata={"architecture": "mvc"},
    generation_rules={
        "generate_tests": True,
        "generate_docs": True,
        "generate_type_hints": True,
    },
    validation_rules={
        "require_entry_point": True,
        "require_routes": True,
        "require_tests": True,
    },
    coding_conventions={
        "class_naming": "PascalCase",
        "function_naming": "camelCase",
        "variable_naming": "camelCase",
        "constant_naming": "UPPER_CASE",
    },
    import_rules={
        "prefer_absolute_imports": True,
        "allow_relative_imports": False,
    },
)



# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_TEMPLATES: dict[str, FrameworkTemplate] = {}


def register_template(template: FrameworkTemplate) -> None:
    """
    Register a FrameworkTemplate. Adding support for a new
    framework is: define directories()/files(), call this.
    """
    _TEMPLATES[template.name] = template


def all_templates() -> list[FrameworkTemplate]:
    return list(_TEMPLATES.values())


def get_template(name: str) -> FrameworkTemplate | None:
    return _TEMPLATES.get(name)


register_template(GENERIC_TEMPLATE)
register_template(SINGLE_FILE_PYTHON_TEMPLATE)
register_template(FLASK_TEMPLATE)
register_template(CLICK_TEMPLATE)
register_template(FASTAPI_TEMPLATE)
register_template(DJANGO_TEMPLATE)
register_template(TYPER_TEMPLATE)
register_template(REACT_TEMPLATE)
register_template(NEXTJS_TEMPLATE)
register_template(EXPRESS_TEMPLATE)
register_template(NESTJS_TEMPLATE)
register_template(VUE_TEMPLATE)
register_template(SVELTE_TEMPLATE)
register_template(SPRING_BOOT_TEMPLATE)
register_template(LARAVEL_TEMPLATE)







# To add a new framework, e.g. FastAPI:
#
# def _fastapi_files(package_name: str) -> list[str]:
#     return [
#         "src/main.py",
#         f"{package_name}/__init__.py",
#         f"{package_name}/config.py",
#         f"{package_name}/routers.py",
#         f"{package_name}/models.py",
#         f"{package_name}/schemas.py",
#         f"{package_name}/dependencies.py",
#         "tests/test_main.py",
#         "docs/README.md",
#     ]
#
# register_template(FrameworkTemplate(
#     name="fastapi",
#     aliases=("fastapi", "fast_api"),
#     directories=_flask_directories,   # same shape, reuse helpers freely
#     files=_fastapi_files,
#     mandatory_requirements=("fastapi", "uvicorn"),
#     include_self_named_module=False,
# ))
