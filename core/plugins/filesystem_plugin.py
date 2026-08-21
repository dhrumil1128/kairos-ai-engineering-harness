"""
File: core/plugins/filesystem_plugin.py

Purpose:
Filesystem plugin for KAIROS.

Uses FileTool to perform
file operations.

Future Versions:

V2:
- Directory listing

V3:
- Recursive search

V4:
- File metadata

V5:
- Workspace sandboxing
"""

from core.plugins.plugin_base import (
    PluginBase
)

from core.tools.file_tool import (
    FileTool
)


class FilesystemPlugin(
    PluginBase
):
    """
    Filesystem plugin.
    """

    def __init__(self):
        """
        Initialize plugin.
        """

        super().__init__(
            name="FilesystemPlugin"
        )

        self.file_tool = FileTool()

    def execute(
        self,
        action: str,
        *args
    ):
        """
        Execute file action.
        """

        if action == "read":
            return self.file_tool.read_file(
                args[0]
            )

        if action == "write":
            self.file_tool.write_file(
                args[0],
                args[1]
            )

            return True

        if action == "exists":
            return self.file_tool.exists(
                args[0]
            )

        if action == "delete":
            self.file_tool.delete_path(
                args[0]
            )

            return True
        
       
        # Prepare project directory.
        if action == "prepare_project":

            return self.file_tool.prepare_project_directory(
                args[0]
            )
    
            
        # Create directory.
        if action == "create_directory":

            self.file_tool.create_directory(
                args[0]
            )

            return True

        if action == "delete_directory":

            self.file_tool.delete_directory(
                args[0]
            )

            return True

        if action == "create_file":

            self.file_tool.create_file(
                args[0],
                args[1] if len(args) > 1 else ""
            )

            return True

        if action == "delete_file":

            self.file_tool.delete_file(
                args[0]
            )

            return True

        if action == "move_file":

            self.file_tool.move_file(
                args[0],
                args[1]
            )

            return True

        if action == "copy_file":

            self.file_tool.copy_file(
                args[0],
                args[1]
            )

            return True

        if action == "rename_file":

            self.file_tool.rename_file(
                args[0],
                args[1]
            )

            return True
        
         # List directory.
        if action == "list_directory":

            return (
                self.file_tool
                .list_directory(
                    args[0]
                )
            )
            
            
        # Initialize KAIROS project.
        if action == "init_project":

            self.file_tool.create_kairos_project(
                args[0]
            )

            return True

        
        
         # Check file exists.
        if action == "exists":

            return (
                self.file_tool.exists(
                    args[0]
                )
            )
            
        
        
        # Delete file.
        if action == "delete":

            self.file_tool.delete_path(
                args[0]
            )

            return True
            
        raise ValueError(
            f"Unknown action: {action}"
        )


    
       
