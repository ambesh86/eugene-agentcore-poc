from mcp.gateway import MCPGateway
from memory.long_term_memory import LongTermMemory


class GraphAgent:

    def run(self, state):
        gateway = MCPGateway()
        traversal = gateway.invoke_tool(
            "graph_traversal",
            "KRAS"
        )

        pagerank = gateway.invoke_tool("pagerank")
        centrality = gateway.invoke_tool("degree_centrality")
        betweenness = gateway.invoke_tool("betweenness")
        closeness = gateway.invoke_tool("closeness")

        state["graph_result"] = {
            "traversal": traversal
        }	

        state["graph_analytics"] = {
            "PageRank": pagerank,
            "Degree_Centrality": centrality,
            "Betweenness": betweenness,
            "Closeness": closeness,
        }	
        entity = "KRAS"   # replace with extracted entity

        ltm = LongTermMemory()

        ltm.save(
            entity,
            {
                "entity": entity,
                "last_query": state["query"],
                "graph_result": state.get("graph_result", {})               
            }
        )

        return state

    