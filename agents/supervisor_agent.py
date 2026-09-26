KNOWN_ENTITIES = [
    "KRAS",
    "EGFR",
    "BRAF",
    "MAPK"
]

from memory.memory_store import MemoryStore
from memory.long_term_memory import LongTermMemory

class SupervisorAgent:
    def __init__(self):
        self.memory_store = MemoryStore()

    def extract_entity(
        self,
        query
    ):
        query_upper = query.upper()

        for entity in KNOWN_ENTITIES:

            if entity in query_upper:
                return entity

        return None

    def classify_intent(
        self,
        query
    ):

        query = query.lower()
        agents = []

        if any(
            word in query
            for word in [
                "drug",
                "inhibitor",
                "target",
                "kras"
            ]
        ):
            agents.append("foundation")
            agents.append("graph")

        if any(
            word in query
            for word in [
                "publication",
                "paper",
                "evidence"
            ]
        ):
            agents.append("publication")

        if any(
            word in query
            for word in [
                "pagerank",
                "centrality",
                "importance",
                "influential",
                "graph analysis"
            ]
        ):
            agents.append("graph")

        return list(set(agents))

    def run(self, state):

        query = state["query"]

        last_entity = self.memory_store.get_context(
            "last_entity"
        )

        entity = self.extract_entity(
            query
        )

        ltm = LongTermMemory()

        historical_data = None

        if entity:
            historical_data = ltm.load(entity)

        state["long_term_memory"] = historical_data

        # Save latest entity
        if entity:
            self.memory_store.save_context(
                "last_entity",
                entity
            )

        # Resolve query using memory
        resolved_query = query

        if last_entity and not entity:
            resolved_query = (
                f"{query} for {last_entity}"
            )

        state["resolved_query"] = resolved_query

        # ADD THESE PRINTS HERE
        print(
            f"Original Query: "
            f"{state['query']}"
        )

        print(
            f"Resolved Query: "
            f"{state['resolved_query']}"
        )

        state["memory"] = {
            "last_entity": last_entity
        }

        agents = self.classify_intent(
            resolved_query
        )

        state["selected_agents"] = agents

        print(
            f"Selected Agents: {agents}"
        )

        return state
