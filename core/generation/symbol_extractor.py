from __future__ import annotations

import ast


class SymbolExtractor:

    def extract(
        self,
        content: str,
    ) -> dict:

        try:
            tree = ast.parse(content)
        except Exception:
            return {
                "classes": [],
                "functions": [],
                "variables": [],
                "imports": [],
            }

        classes = []
        functions = []
        variables = []
        imports = []

        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):
                classes.append(node.name)

            elif isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                functions.append(node.name)

            elif isinstance(node, ast.Assign):

                for target in node.targets:

                    if isinstance(
                        target,
                        ast.Name,
                    ):
                        variables.append(
                            target.id
                        )

            elif isinstance(node, ast.Import):

                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(
                node,
                ast.ImportFrom,
            ):

                module = node.module or ""

                for alias in node.names:
                    imports.append(
                        f"{module}.{alias.name}"
                    )

        return {
            "classes": sorted(set(classes)),
            "functions": sorted(set(functions)),
            "variables": sorted(set(variables)),
            "imports": sorted(set(imports)),
        }