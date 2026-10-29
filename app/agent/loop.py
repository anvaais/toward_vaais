
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Message:
    role: str
    content: str


@dataclass
class ToolCall:
    name: str
    arguments: dict


@dataclass
class AgentResponse:
    message: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    done: bool = False


Tool = Callable[..., str]


class AgentLoop:
    def __init__(
        self,
        tools: dict[str, Tool],
        max_steps: int = 5,
    ):
        self.tools = tools
        self.max_steps = max_steps
        self.history: list[Message] = []

    def run(
        self,
        user_input: str,
        responder: Callable[[list[Message]], AgentResponse],
    ) -> str:
        self.history.append(
            Message(role="user", content=user_input)
        )

        for step in range(self.max_steps):
            # Ask the responder what the agent should do next.
            response = responder(self.history)

            self.history.append(
                Message(role="assistant", content=response.message)
            )

            # Stop when the responder says the task is complete.
            if response.done:
                return response.message

            # Execute requested tools.
            for tool_call in response.tool_calls:
                if tool_call.name not in self.tools:
                    result = f"Error: Unknown tool '{tool_call.name}'"
                else:
                    try:
                        result = self.tools[tool_call.name](
                            **tool_call.arguments
                        )
                    except (TypeError, ValueError) as exc:
                        result = f"Tool error: {exc}"

                self.history.append(
                    Message(
                        role="tool",
                        content=f"{tool_call.name}: {result}",
                    )
                )

        return "Stopped: maximum number of steps reached."
