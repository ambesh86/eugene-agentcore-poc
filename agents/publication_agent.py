from mcp.gateway import MCPGateway

class PublicationAgent:
    def run(self, state):
        gateway = MCPGateway()
        publications = gateway.invoke_tool(
            "search_publications",
            state["query"]
        )

        state["publication_result"] = publications
        return state