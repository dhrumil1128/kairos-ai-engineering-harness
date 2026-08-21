"""
File: core/mcp/docker_mcp.py

Purpose:
Real Docker MCP integration.

Uses the official Docker SDK.

Capabilities:

- Verify Docker connection
- List containers
- Inspect containers

Future Versions:

V2:
- Start containers

V3:
- Stop containers

V4:
- Create containers

V5:
- Agent sandbox execution
"""

# Official Docker SDK.
import docker


class DockerMCP:
    """
    Real Docker MCP.
    """

    def __init__(self):
        """
        Initialize Docker client.
        """

        # Connect to local Docker engine.
        self.client = docker.from_env()

    def is_connected(
        self
    ) -> bool:
        """
        Verify Docker connection.
        """

        try:

            # Ping Docker daemon.
            self.client.ping()

            return True

        except Exception:

            return False

    def list_containers(
        self
    ) -> list:
        """
        Return running containers.
        """

        # Fetch running containers.
        containers = (
            self.client.containers.list()
        )

        # Return container names.
        return [
            container.name
            for container in containers
        ]

    def get_container_info(
        self,
        container_name: str
    ) -> dict:
        """
        Retrieve container details.
        """

        # Get container.
        container = (
            self.client.containers.get(
                container_name
            )
        )

        return {
            "id": container.id,
            "name": container.name,
            "status": container.status,
            "image": (
                container.image.tags
            )
        }