"""
File: core/context/document_parser.py

Purpose:
Parse project documents
into structured context
for the KAIROS Context
Intelligence Engine.

Why:

Project documents contain
valuable architectural and
development knowledge.

Instead of sending entire
documents to the LLM,
KAIROS extracts structured
sections that can later be
ranked, compressed, and
loaded into context.

Architecture:

Raw Documents
      │
      ▼
Document Parser
      │
      ├── Header Detection
      ├── Section Extraction
      ├── Metadata Extraction
      ├── Cleaning
      │
      ▼
Knowledge Manager

V2:
- Markdown AST

V3:
- Semantic Sections

V4:
- Entity Extraction

V5:
- Knowledge Graph
"""

from __future__ import annotations

import re

from core.logging.kairos_logger import (
    KairosLogger,
)


class DocumentParser:
    """
    Enterprise document parser.
    """

    def __init__(
        self
    ):
        """
        Initialize parser.
        """

        self.logger = (
            KairosLogger(
                "context"
            )
        )

    # ---------------------------------- #
    # Parse Document
    # ---------------------------------- #

    def parse(
        self,
        content: str
    ) -> dict:
        """
        Parse markdown
        document.
        """

        self.logger.info(
            "Parsing document."
        )

        if (
            not content
        ):

            return {

                "title": "",

                "sections": [],

                "metadata": {},

            }

        cleaned = (
            self._clean_document(
                content
            )
        )

        title = (
            self._extract_title(
                cleaned
            )
        )

        sections = (
            self._extract_sections(
                cleaned
            )
        )

        metadata = (
            self._extract_metadata(
                cleaned
            )
        )

        self.logger.success(
            "Document parsed."
        )

        return {

            "title": title,

            "sections": sections,

            "metadata": metadata,

        }

    # ---------------------------------- #
    # Clean Document
    # ---------------------------------- #

    def _clean_document(
        self,
        content: str
    ) -> str:
        """
        Remove unnecessary
        whitespace.
        """

        return "\n".join(

            line.rstrip()

            for line
            in content.splitlines()

        ).strip()

    # ---------------------------------- #
    # Extract Title
    # ---------------------------------- #

    def _extract_title(
        self,
        content: str
    ) -> str:
        """
        Return first
        markdown heading.
        """

        for line in content.splitlines():

            if (
                line.startswith("#")
            ):

                return (
                    line.lstrip("#").strip()
                )

        return ""
    
    
        # ---------------------------------- #
    # Extract Sections
    # ---------------------------------- #

    def _extract_sections(
        self,
        content: str
    ) -> list[dict]:
        """
        Extract markdown
        sections.
        """

        sections = []

        current_title = "Introduction"

        current_content = []

        for line in content.splitlines():

            if re.match(
                r"^#{1,6}\s+",
                line
            ):

                if current_content:

                    sections.append({

                        "title":
                        current_title,

                        "content":
                        "\n".join(
                            current_content
                        ).strip(),

                    })

                current_title = (
                    line.lstrip("#").strip()
                )

                current_content = []

                continue

            current_content.append(
                line
            )

        if current_content:

            sections.append({

                "title":
                current_title,

                "content":
                "\n".join(
                    current_content
                ).strip(),

            })

        return sections

    # ---------------------------------- #
    # Extract Metadata
    # ---------------------------------- #

    def _extract_metadata(
        self,
        content: str
    ) -> dict:
        """
        Extract document
        metadata.
        """

        metadata = {

            "lines": len(
                content.splitlines()
            ),

            "characters": len(
                content
            ),

            "words": len(
                content.split()
            ),

            "headings": len(

                re.findall(

                    r"^#{1,6}\s+",

                    content,

                    re.MULTILINE,

                )

            ),

            "code_blocks": len(

                re.findall(

                    r"```",

                    content,

                )

            ) // 2,

            "bullet_points": len(

                re.findall(

                    r"^\s*[-*]\s",

                    content,

                    re.MULTILINE,

                )

            ),

        }

        return metadata
    
        # ---------------------------------- #
    # Public Utilities
    # ---------------------------------- #

    def section_count(
        self,
        content: str
    ) -> int:
        """
        Return total
        section count.
        """

        parsed = (
            self.parse(
                content
            )
        )

        return len(
            parsed[
                "sections"
            ]
        )

    def headings(
        self,
        content: str
    ) -> list[str]:
        """
        Return all
        section headings.
        """

        parsed = (
            self.parse(
                content
            )
        )

        return [

            section["title"]

            for section
            in parsed["sections"]

        ]

    def summary(
        self,
        content: str
    ) -> dict:
        """
        Return document
        summary.
        """

        parsed = (
            self.parse(
                content
            )
        )

        return {

            "title":
            parsed["title"],

            "sections":
            len(
                parsed[
                    "sections"
                ]
            ),

            "metadata":
            parsed[
                "metadata"
            ],

        }
        
        