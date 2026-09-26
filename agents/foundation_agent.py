from mcp.gateway import MCPGateway
from utils.entity_extractor import extract_entity

class FoundationAgent:
    def run(self, state):
        gateway = MCPGateway()

        entity = extract_entity(
            state["query"]
        )

        result = gateway.invoke_tool(
            "search_drug",
            entity
        )

        state["foundation_result"] = result
        return state