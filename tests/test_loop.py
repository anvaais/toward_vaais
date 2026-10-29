
from app.agent.loop import (
    AgentLoop,
    AgentResponse,
    ToolCall,
)


def add(a: int, b: int) -> str:
    return str(a + b)


def fake_responder(history):
    # First call: request the add tool.
    if not any(message.role == "tool" for message in history):
        return AgentResponse(
            message="I will add the two numbers.",
            tool_calls=[
                ToolCall(
                    name="add",
                    arguments={"a": 10, "b": 20},
                )
            ],
        )

    # Second call: finish after receiving the tool result.
    tool_result = history[-1].content

    return AgentResponse(
        message=f"The result is {tool_result.split(': ', 1)[1]}.",
        done=True,
    )


tools = {"add": add}

agent = AgentLoop(tools=tools, max_steps=5)

result = agent.run(
    user_input="What is 10 + 20?",
    responder=fake_responder,
)

print(result)
