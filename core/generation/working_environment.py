from __future__ import annotations

from collections import deque

from core.architecture.blueprint import ArchitectureBlueprint
from core.generation.symbol_extractor import SymbolExtractor
from core.generation.dependency_resolver import DependencyResolver
from core.generation.project_index import ProjectIndex


class WorkingEnvironment:
    """
    Runtime project state during code generation.
    """

    def __init__(
        self,
        blueprint: ArchitectureBlueprint,
    ) -> None:

        self.blueprint = blueprint

        self.project_name = blueprint.project_name

        self.pending_files = deque(blueprint.files)

        self.generated_files: dict[str, str] = {}

        self.current_file: str | None = None

        self.project_memory: dict = {
            "generated_order": [],
            "current_stage": "generation",
        }

        self.metadata: dict = {}
        
        
        self.symbol_extractor = SymbolExtractor()

        self.symbol_index: dict[str, dict] = {}
        
        self.project_index = ProjectIndex()
        
        self.dependency_resolver = DependencyResolver()
        
        

    def has_pending_files(self) -> bool:
        return len(self.pending_files) > 0

    def next_file(self) -> str:

        if not self.pending_files:
            raise StopIteration("No pending files remaining.")

        self.current_file = self.pending_files.popleft()

        return self.current_file

    def mark_generated(
        self,
        file_path: str,
        content: str,
    ) -> None:

        self.generated_files[file_path] = content

        self.symbol_index[file_path] = (
            self.symbol_extractor.extract(content)
        )


        self.project_index.index_file(file_path,self.symbol_index[file_path],
)
        
        
        self.project_memory["generated_order"].append(file_path)
        self.current_file = None
        
    
    def get_generation_history(
        self,
    ) -> list[str]:

        return list(
            self.project_memory["generated_order"]
        )

    def get_project_index(
        self,
    ) -> ProjectIndex:

        return self.project_index   
    
    
    
    def get_generated_files(self) -> dict[str, str]:

        return dict(self.generated_files)

    def get_current_file(self) -> str | None:

        return self.current_file

    def get_pending_files(self) -> list[str]:

        return list(self.pending_files)

    def get_blueprint(self) -> ArchitectureBlueprint:

        return self.blueprint

    def reset(self) -> None:

        self.pending_files = deque(self.blueprint.files)

        self.generated_files.clear()

        self.current_file = None

        self.project_memory.clear()

        self.metadata.clear()
    
    
    def get_generated_file(
        self,
        file_path: str,
    ) -> str | None:

        return self.generated_files.get(
            file_path
        )
        
    
    def is_generated(
        self,
        file_path: str,
    ) -> bool:

        return file_path in self.generated_files
    
    
    def file_count(self) -> int:

        return len(self.generated_files)
    
    
    def get_project_name(
        self,
    ) -> str:

        return self.project_name
    
    def get_metadata(
        self,
    ) -> dict:

        return self.metadata
    
    
    def update_memory(
        self,
        key: str,
        value,
    ) -> None:

        self.project_memory[key] = value
        
    
    def read_memory(
        self,
        key: str,
        default=None,
    ):

        return self.project_memory.get(
            key,
            default,
        )
        
        
#==================================================================== Symbol_executor integration =============================================================================================
    def get_symbol_index(
        self,
    ) -> dict:

        return self.symbol_index
    
    def get_symbols(
        self,
        file_path: str,
    ) -> dict:

        return self.symbol_index.get(
            file_path,
            {},
        )
        

#===================================================================== Dependency_ resolver integration ======================================================================================= 
    def get_relevant_files(self) -> dict[str, str]:

        if self.current_file is None:
            return {}

        return self.dependency_resolver.get_relevant_files(
            current_file=self.current_file,
            architecture=self.blueprint.to_dict(),
            generated_files=self.generated_files,
        )