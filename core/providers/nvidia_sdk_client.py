"""
File: core/providers/nvidia_sdk_client.py

Purpose:
NVIDIA SDK client wrapper.
"""

import os
import time
from pathlib import Path

from openai import OpenAI


SYSTEM_PROMPT = """
You are KAIROS, a high-agency autonomous AI system.

Your responsibilities include:
- Planning software solutions.
- Designing software architecture.
- Generating production-ready code.
- Reviewing and improving code.
- Assisting with desktop automation tasks.
- Following user instructions accurately.
- Never fabricate APIs, libraries, or functionality.
- When generating code, never return placeholder implementations, TODO comments, or stub methods.
- Preserve consistency with the provided project architecture and existing codebase.
- Return complete, high-quality outputs.
- Do not wrap code inside markdown unless explicitly requested.
""".strip()


class NvidiaSDKClient:
    """
    NVIDIA SDK wrapper.
    """

    DEFAULT_MODEL = "nvidia/llama-3.3-nemotron-super-49b-v1.5"

    def __init__(
        self,
        api_key: str = "",
    ):
        """
        Initialize NVIDIA client.
        """

        self.api_key = api_key or os.getenv("NVIDIA_API_KEY")

        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_key,
        )

    def generate(
        self,
        prompt: str,
        model: str = DEFAULT_MODEL,
        system_prompt: str = SYSTEM_PROMPT,
        max_tokens: int = 8192,
        max_continuations: int = 2,
    ) -> str:
        """
        Generate a response using the NVIDIA API.

        If the model runs out of tokens mid-generation (finish_reason == "length"),
        automatically asks it to continue from where it left off, up to
        `max_continuations` times, instead of silently returning a truncated file.
        """

        last_error = None

        for attempt in range(3):

            try:

                messages = [
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ]

                full_content = ""

                for _ in range(max_continuations + 1):

                    response = self.client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=0.2,
                        top_p=0.95,
                        max_tokens=max_tokens,
                        stream=False,
                    )
                    

                    choice = response.choices[0]
                    content = choice.message.content or ""
                    full_content += content
                    self._log_raw_response(content)

                    if choice.finish_reason != "length":
                        break

                    # Response was cut off due to token limit — continue it.
                    messages.append(
                        {
                            "role": "assistant",
                            "content": content,
                        }
                    )
                    messages.append(
                        {
                            "role": "user",
                            "content": (
                                "Continue exactly where you left off. "
                                "Do not repeat any previous content, do not "
                                "restart the file, and do not add explanations."
                            ),
                        }
                    )

                full_content = full_content.strip()

                if not full_content:
                    raise RuntimeError(
                        "NVIDIA API returned an empty response."
                    )

                return full_content

            except Exception as error:

                last_error = error

                if attempt < 2:
                    time.sleep(2 * (attempt + 1))
                    continue

        raise RuntimeError(
            f"NVIDIA API failed after 3 attempts: {last_error}"
        )

    def _log_raw_response(
        self,
        content: str,
    ) -> None:
        log_path = (
            Path(".kairos")
            / "logs"
            / "raw_llm_output.txt"
        )
        log_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with log_path.open(
            "a",
            encoding="utf-8",
        ) as file:
            file.write(
                "===== NVIDIA RAW LLM RESPONSE =====\n"
            )
            file.write(
                content or ""
            )
            file.write(
                "\n"
            )

    def configured(self) -> bool:
        """
        Check whether the client is configured.
        """

        return bool(self.api_key)
