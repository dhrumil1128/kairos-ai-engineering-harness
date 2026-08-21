from dataclasses import dataclass, field


@dataclass(slots=True)
class ArchitectureBlueprint:
    """
    Immutable architecture contract shared between
    Architect, Coder, Validator and Documentation agents.
    """

    project_name: str
    project_type: str
    framework: str
    language: str

    package_name: str

    entry_point: str
    entry_module: str
    entry_function: str | None

    directories: list[str]
    files: list[str]
    requirements: list[str]

    framework_template: str

    code_style: str

    capabilities: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    generation_rules: dict = field(default_factory=dict)
    validation_rules: dict = field(default_factory=dict)
    coding_conventions: dict = field(default_factory=dict)
    import_rules: dict = field(default_factory=dict)
    file_responsibilities: dict = field(default_factory=dict)


    def to_dict(self) -> dict:
        """
        Convert blueprint into a dictionary for compatibility
        with existing agents.
        """

        return {
            "project_name": self.project_name,
            "project_type": self.project_type,
            "framework": self.framework,
            "language": self.language,

            "package_name": self.package_name,

            "entry_point": self.entry_point,
            "entry_module": self.entry_module,
            "entry_function": self.entry_function,

            "directories": self.directories,
            "files": self.files,
            "requirements": self.requirements,

            "framework_template": self.framework_template,

            "code_style": self.code_style,

            "capabilities": self.capabilities,
            "metadata": self.metadata,
            "generation_rules": self.generation_rules,
            "validation_rules": self.validation_rules,
            "coding_conventions": self.coding_conventions,
            "import_rules": self.import_rules,
            "file_responsibilities": self.file_responsibilities,
        }


    def get(self, key: str, default=None):
        """
        Dictionary compatibility helper.

        Allows existing code using architecture.get(...)
        to work while migrating to ArchitectureBlueprint.
        """

        return getattr(self, key, default)


    def __getitem__(self, key: str):
        """
        Dictionary compatibility.

        Allows:
            blueprint["files"]
            blueprint["framework"]
        """

        return getattr(self, key)


    @property
    def project_root(self) -> str:
        """
        Root package/module name for generated projects.
        """

        return self.package_name