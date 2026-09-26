"""Bedrock-backed Supervisor Agent (Claude Sonnet/Haiku) for intent classification."""
import json
import os

from langchain_aws import ChatBedrock

VALID_AGENTS = ["foundation", "graph", "publication"]

_PROMPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "prompt",
    "supervisor.txt"
)


def _load_system_prompt():
    with open(_PROMPT_PATH, "r") as fp:
        return fp.read()


class BedrockSupervisorAgent:

    def __init__(self):
        self.llm = ChatBedrock(
            model_id=os.getenv(
                "BEDROCK_MODEL_ID",
                "us.anthropic.claude-haiku-4-5-20251001-v1:0"
            ),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            model_kwargs={"temperature": 0}
        )
        self.system_prompt = _load_system_prompt()

    def classify_intent(self, query):
        response = self.llm.invoke([
            ("system", self.system_prompt),
            ("human", query)
        ])

        agents = json.loads(response.content)
        return [agent for agent in agents if agent in VALID_AGENTS]

    def run(self, state):
        try:
            agents = self.classify_intent(state["query"])
        except Exception:
            agents = []

        # Fall back to the deterministic rule-based supervisor on any Bedrock/parse failure
        if not agents:
            from agents.supervisor_agent import SupervisorAgent
            return SupervisorAgent().run(state)

        state["selected_agents"] = agents
        return state
