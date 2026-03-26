"""LLM client service for intent routing with tool calling."""

from __future__ import annotations

import httpx
import json
import sys
from typing import Any


class LLMClient:
    """Client for interacting with the LLM API with tool calling support."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str = "coder-model",
    ):
        """Initialize the LLM client.

        Args:
            base_url: Base URL of the LLM API (may include /v1 suffix).
            api_key: API key for authentication.
            model: Model name to use for completions.
        """
        # Normalize base_url: strip /v1 suffix if present (we add it in requests)
        self.base_url = base_url.rstrip("/")
        if self.base_url.endswith("/v1"):
            self.base_url = self.base_url[:-3]
        self.api_key = api_key
        self.model = model
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=60.0,
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    def _get_tool_definitions(
        self, api_client: Any
    ) -> list[dict[str, Any]]:
        """Get tool definitions for all 9 backend endpoints.

        Args:
            api_client: The LMS API client instance.

        Returns:
            List of tool definitions in OpenAI-compatible format.
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_items",
                    "description": "List of all labs and tasks available in the LMS",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_learners",
                    "description": "Get enrolled students and their groups",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_scores",
                    "description": "Get score distribution (4 buckets) for a specific lab",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lab": {
                                "type": "string",
                                "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                            }
                        },
                        "required": ["lab"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_pass_rates",
                    "description": "Get per-task average scores and attempt counts for a lab",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lab": {
                                "type": "string",
                                "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                            }
                        },
                        "required": ["lab"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_timeline",
                    "description": "Get submissions per day for a lab",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lab": {
                                "type": "string",
                                "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                            }
                        },
                        "required": ["lab"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_groups",
                    "description": "Get per-group scores and student counts for a lab",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lab": {
                                "type": "string",
                                "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                            }
                        },
                        "required": ["lab"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_top_learners",
                    "description": "Get top N learners by score for a lab",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lab": {
                                "type": "string",
                                "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of top learners to return (default 10)",
                                "default": 10,
                            },
                        },
                        "required": ["lab"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_completion_rate",
                    "description": "Get completion rate percentage for a lab",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lab": {
                                "type": "string",
                                "description": "Lab identifier, e.g. 'lab-01', 'lab-04'",
                            }
                        },
                        "required": ["lab"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "trigger_sync",
                    "description": "Refresh data from the autochecker pipeline",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
        ]

    async def _call_llm(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Make a call to the LLM API.

        Args:
            messages: List of conversation messages.
            tools: Optional list of tool definitions.

        Returns:
            The LLM response as a dict.

        Raises:
            httpx.HTTPError: If the API call fails.
        """
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        response = await self._client.post(
            "/v1/chat/completions",
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    async def generate_completion(
        self,
        user_message: str,
        api_client: Any,
        system_prompt: str | None = None,
        debug: bool = False,
    ) -> str:
        """Generate a completion using the LLM with tool calling.

        This implements the tool calling loop:
        1. Send user message + tool definitions to LLM
        2. LLM returns tool calls
        3. Execute tool calls via API client
        4. Feed results back to LLM
        5. LLM produces final answer

        Args:
            user_message: The user's input message.
            api_client: The LMS API client for executing tool calls.
            system_prompt: Optional custom system prompt.
            debug: If True, print debug output to stderr.

        Returns:
            The final response from the LLM.
        """
        if system_prompt is None:
            system_prompt = (
                "You are a helpful assistant for an LMS (Learning Management System). "
                "You have access to tools that can fetch data about labs, learners, scores, and analytics. "
                "When the user asks a question, use the available tools to get the data and provide accurate answers. "
                "Always use tools to get real data before answering. "
                "If you need to compare multiple labs, call the tool for each lab. "
                "After receiving tool results, summarize the data clearly and concisely. "
                "If the user's message is a greeting or casual message, respond naturally without using tools. "
                "If the user's message is unclear or ambiguous, ask for clarification about what they want to know."
            )

        messages: list[dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        tools = self._get_tool_definitions(api_client)

        max_iterations = 10
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            try:
                response = await self._call_llm(messages, tools)
            except httpx.HTTPError as e:
                return f"LLM error: {str(e)}"

            choice = response.get("choices", [{}])[0].get("message", {})

            # Check if LLM wants to call tools
            tool_calls = choice.get("tool_calls")

            if not tool_calls:
                # No tool calls - LLM has a final answer
                return choice.get("content", "I don't have information to answer that question.")

            # Add the assistant's message with tool calls to conversation
            messages.append({
                "role": "assistant",
                "content": choice.get("content"),
                "tool_calls": tool_calls,
            })

            # Execute each tool call
            for tool_call in tool_calls:
                function_name = tool_call.get("function", {}).get("name")
                function_args_str = tool_call.get("function", {}).get("arguments", "{}")
                tool_call_id = tool_call.get("id")

                try:
                    function_args = json.loads(function_args_str)
                except json.JSONDecodeError:
                    function_args = {}

                if debug:
                    print(
                        f"[tool] LLM called: {function_name}({function_args})",
                        file=sys.stderr,
                    )

                # Execute the tool via API client
                try:
                    result = await self._execute_tool(
                        function_name, function_args, api_client
                    )
                    result_str = json.dumps(result, default=str)
                    if debug:
                        print(f"[tool] Result: {result_str[:200]}...", file=sys.stderr)
                except Exception as e:
                    result_str = json.dumps({"error": str(e)})
                    if debug:
                        print(f"[tool] Error: {e}", file=sys.stderr)

                # Add tool result to conversation
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": result_str,
                })

            if debug and iteration > 1:
                print(
                    f"[summary] Feeding {len(tool_calls)} tool result(s) back to LLM",
                    file=sys.stderr,
                )

        return "I reached the maximum number of tool calls. Here's what I found so far: " + (
            messages[-1].get("content", "") if messages else ""
        )

    async def _execute_tool(
        self,
        function_name: str,
        function_args: dict[str, Any],
        api_client: Any,
    ) -> Any:
        """Execute a tool by calling the corresponding API client method.

        Args:
            function_name: Name of the tool/function to call.
            function_args: Arguments to pass to the function.
            api_client: The LMS API client instance.

        Returns:
            The result from the API call.

        Raises:
            ValueError: If the function name is unknown.
        """
        method = getattr(api_client, function_name, None)
        if method is None:
            raise ValueError(f"Unknown tool: {function_name}")
        return await method(**function_args)
