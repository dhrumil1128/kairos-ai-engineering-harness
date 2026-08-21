"""
File: core/mcp/github_mcp.py

Purpose:
Real GitHub MCP integration.

Uses PyGithub to interact
with GitHub repositories.

Capabilities:

- Repository lookup
- Description retrieval
- Star count
- Language detection
- Default branch retrieval

Future Versions:

V2:
- Issue management

V3:
- Pull request management

V4:
- Commit operations

V5:
- Full GitHub automation
"""

# Load environment variables.
import os

# Load .env values.
from dotenv import load_dotenv

# GitHub SDK.
from github import Github
from github import Auth



# Load environment variables.
load_dotenv()


class GitHubMCP:
    """
    Real GitHub MCP.
    """

    def __init__(self):
        """
        Initialize GitHub client.
        """

        # Read token from environment.
        # Create GitHub client.
        # Create token authentication.
        # Read token from environment.
        self.token = os.getenv(
            "GITHUB_TOKEN"
        )


        # Verify token exists.
        if not self.token:
            raise ValueError(
                "GITHUB_TOKEN not configured."
            )

        # Create token authentication.
        auth = Auth.Token(
            self.token
        )

        # Create GitHub client.
        self.client = Github(
            auth=auth
        )

    def is_connected(
        self
    ) -> bool:
        """
        Verify GitHub connection.
        """

        try:

            # Fetch authenticated user.
            self.client.get_user()

            return True

        except Exception:

            return False

    def get_repository(
        self,
        repository_name: str
    ) -> dict:
        """
        Retrieve repository details.

        Example:
            microsoft/vscode
        """

        # Fetch repository.
        repo = self.client.get_repo(
            repository_name
        )

        # Return structured metadata.
        return {
            "name": repo.full_name,
            "description": repo.description,
            "stars": repo.stargazers_count,
            "language": repo.language,
            "default_branch": repo.default_branch
        }