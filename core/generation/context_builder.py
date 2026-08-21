from __future__ import annotations

from core.generation.generation_context import GenerationContext
from core.generation.working_environment import WorkingEnvironment


class ContextBuilder:

    def build(
        self,
        environment: WorkingEnvironment,
    ) -> GenerationContext:

        return GenerationContext(
            architecture=environment.get_blueprint(),
            user_request=str(
                environment.get_blueprint().metadata.get(
                    "user_request",
                    "",
                )
            ),
            current_file=environment.get_current_file(),
            generated_files=environment.get_generated_files(),
            pending_files=environment.get_pending_files(),
            generation_history=environment.get_generation_history(),
            symbol_index=environment.get_symbol_index(),
            project_index=environment.get_project_index(),
            project_memory=environment.project_memory,
        )
