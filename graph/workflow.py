from langgraph.graph import StateGraph
from langgraph.graph import END

from graph.state import ResearchState

from graph.nodes import (
    supervisor_node,
    foundation_node,
    graph_node,
    publication_node,
    report_node
)
def route_after_graph(state):

    agents = state["selected_agents"]

    if "publication" in agents:
        return "publication"
    return "report"
workflow = StateGraph(
    ResearchState
)

def route_after_supervisor(state):

    agents = state["selected_agents"]

    if "foundation" in agents:
        return "foundation"

    if "graph" in agents:
        return "graph"

    if "publication" in agents:
        return "publication"

    return "report"

def route_after_foundation(state):

    agents = state["selected_agents"]

    if "graph" in agents:
        return "graph"

    if "publication" in agents:
        return "publication"

    return "report"


workflow.add_node(
    "supervisor",
    supervisor_node
)


workflow.add_node(
    "foundation",
    foundation_node
)

workflow.add_node(
    "graph",
    graph_node
)

workflow.add_node(
    "publication",
    publication_node
)

workflow.add_node(
    "report",
    report_node
)

# NEW ENTRY POINT
workflow.set_entry_point(
    "supervisor"
)
workflow.add_conditional_edges(
    "supervisor",
    route_after_supervisor,
    {
        "foundation": "foundation",
        "graph": "graph",
        "publication": "publication",
        "report": "report"
    }
)

workflow.add_conditional_edges(
    "foundation",
    route_after_foundation,
    {
        "graph": "graph",
        "publication": "publication",
        "report": "report"
    }
)

workflow.add_conditional_edges(
    "graph",
    route_after_graph,
    {
        "publication": "publication",
        "report": "report"
    }
)

workflow.add_edge(
    "publication",
    "report"
)

workflow.add_edge(
    "report",
    END
)

graph = workflow.compile()
