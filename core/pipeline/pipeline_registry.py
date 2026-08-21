"""
File:
core/pipeline/pipeline_registry.py

Purpose:
Central registry for
all execution pipelines.

Architecture:

Pipeline Selector
        │
        ▼
Pipeline Registry
        │
        ├── Analysis
        ├── Generation
        ├── Repair
        ├── Review
        ├── Testing
        └── Documentation
"""


class PipelineRegistry:
    """
    Store all
    pipeline definitions.
    """

    def __init__(self):
        """
        Initialize registry.
        """

        self.pipelines = {

            "analysis": [

                "analyze",
                "analyse",
                "explain",
                "inspect",
                "summarize",
                "summary",
                "understand",
                "architecture",
                "technology stack",
                "tech stack",
                "review project",

            ],

            "generation": [

                "create",
                "build",
                "generate",
                "develop",
                "implement",
                "make",

            ],

            "repair": [

                "fix",
                "repair",
                "resolve",
                "debug",
                "bug",

            ],

            "review": [

                "review",
                "audit",
                "code review",

            ],

            "testing": [

                "test",
                "testing",
                "pytest",
                "unit test",

            ],

            "documentation": [

                "documentation",
                "document",
                "readme",
                "docs",

            ],

        }
    
    # ----------------------------------
    # Get Pipelines
    # ----------------------------------

    def get_pipelines(
        self
    ) -> dict:
        """
        Return all
        registered pipelines.
        """

        return (
            self.pipelines
        )

    # ----------------------------------
    # Register Pipeline
    # ----------------------------------

    def register(
        self,
        name: str,
        keywords: list[str]
    ) -> None:
        """
        Register a new
        execution pipeline.
        """

        self.pipelines[
            name
        ] = keywords
        
    
    # ----------------------------------
    # Find Pipeline
    # ----------------------------------

    def find_pipeline(
        self,
        command: str
    ) -> str | None:
        """
        Find the best matching
        pipeline.
        """

        prompt = command.lower()
        matches = []

        for pipeline, keywords in self.pipelines.items():

            count = sum(

                keyword in prompt

                for keyword in keywords

            )

            if count:
                matches.append(
                    (
                        count,
                        self._priority(pipeline),
                        pipeline,
                    )
                )

        if matches:
            matches.sort(
                reverse=True
            )

            return matches[0][2]

        return None

    def _priority(
        self,
        pipeline: str,
    ) -> int:
        priorities = {
            "generation": 6,
            "repair": 5,
            "testing": 4,
            "review": 3,
            "documentation": 2,
            "analysis": 1,
        }

        return priorities.get(
            pipeline,
            0,
        )
