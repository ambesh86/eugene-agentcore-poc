from typing import TypedDict
from typing import List
from typing import Dict


class ResearchState(TypedDict):

    query: str
    intent: str
    selected_agents: List[str]
    foundation_result: Dict
    graph_result: Dict
    graph_analytics: dict
    publication_result: Dict
    final_report: str
    current_agent: str
    memory: dict
    long_term_memory: dict