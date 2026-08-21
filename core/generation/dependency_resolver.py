from pathlib import Path


class DependencyResolver:
    """
    Resolves which previously generated files
    should be included as context for the current file.
    """

    def classify_file(self, file_path: str) -> str:
        """
        Classify a file into a logical role.
        """

        path = file_path.replace("\\", "/").lower()
        filename = Path(path).name

        if filename == "__init__.py":
            return "package"

        if filename in ("main.py", "app.py", "run.py"):
            return "entry"

        if filename == "routes.py" or "/routes/" in path:
            return "route"

        if filename == "services.py" or "/services/" in path:
            return "service"

        if filename == "models.py" or "/models/" in path:
            return "model"

        if filename == "schemas.py" or "/schemas/" in path:
            return "schema"

        if (
            filename in ("database.py", "db.py", "session.py")
            or "/database/" in path
        ):
            return "database"

        if filename == "config.py" or "/config/" in path:
            return "config"

        if filename == "requirements.txt":
            return "requirements"

        if filename.endswith(".md"):
            return "documentation"

        if filename.endswith(".sql"):
            return "database"

        if "/tests/" in path or filename.startswith("test_"):
            return "test"

        return "source"

    def resolve_dependencies(self, role: str) -> list[str]:
        """
        Return the file roles required to generate
        the current file role.
        """

        dependency_map = {

            "entry": [
                "route",
                "config",
                "database",
            ],

            "route": [
                "service",
                "schema",
                "model",
                "config",
            ],

            "service": [
                "model",
                "schema",
                "database",
                "config",
            ],

            "model": [
                "database",
                "config",
            ],

            "schema": [
                "model",
                "config",
            ],

            "test": [
                "entry",
                "route",
                "service",
                "schema",
                "model",
                "database",
                "config",
                "source",
            ],

            "package": [],

            "documentation": [
                "all",
            ],

            "database": [],

            "requirements": [],

            "source": [],
        }

        return dependency_map.get(role, [])

    def get_relevant_files(
        self,
        current_file: str,
        architecture: dict,
        generated_files: dict[str, str],
    ) -> dict[str, str]:
        """
        Return previously generated files that are
        relevant to the current file.
        """

        current_role = self.classify_file(current_file)

        required_roles = self.resolve_dependencies(current_role)

        relevant = {}

        for file_path, content in generated_files.items():

            # Never include the file currently being generated.
            if file_path == current_file:
                continue

            file_role = self.classify_file(file_path)

            if "all" in required_roles or file_role in required_roles:
                relevant[file_path] = content

        return relevant
