import os

from agents.supervisor_agent import SupervisorAgent
from agents.foundation_agent import FoundationAgent
from agents.graph_agent import GraphAgent
from agents.publication_agent import PublicationAgent


def supervisor_node(state):
    if os.getenv("USE_BEDROCK_SUPERVISOR", "false").lower() == "true":
        from agents.bedrock_supervisor_agent import BedrockSupervisorAgent
        return BedrockSupervisorAgent().run(state)

    return SupervisorAgent().run(state)


def foundation_node(state):
    return FoundationAgent().run(state )


def graph_node(state):
    return GraphAgent().run(state)


def publication_node(state):
    return PublicationAgent().run(state)


def report_node(state):
    report = f"""

FOUNDATION RESULT
-----------------
{state["foundation_result"]}


GRAPH RESULT
------------
{state["graph_result"]}


PUBLICATIONS
------------
{state["publication_result"]}

"""

    state["final_report"] = report

    return state