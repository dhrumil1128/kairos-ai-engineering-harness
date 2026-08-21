from __future__ import annotations

from collections import defaultdict


class ProjectIndex:

    def __init__(self):

        self.classes = defaultdict(list)

        self.functions = defaultdict(list)

        self.imports = defaultdict(list)

        self.variables = defaultdict(list)
        
    
    def index_file(
        self,
        file_path: str,
        symbols: dict,
    ) -> None:

        self.classes[file_path] = symbols.get(
            "classes",
            [],
        )

        self.functions[file_path] = symbols.get(
            "functions",
            [],
        )

        self.imports[file_path] = symbols.get(
            "imports",
            [],
        )

        self.variables[file_path] = symbols.get(
            "variables",
            [],
        )
        
    
    def all_classes(self) -> dict:

        return dict(self.classes)
    
    
    def all_functions(self) -> dict:

        return dict(self.functions)
    
    
    def all_imports(self) -> dict:

        return dict(self.imports)
    
    
    def all_variables(self) -> dict:

        return dict(self.variables)