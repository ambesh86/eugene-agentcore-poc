from graph.workflow import graph


# query = (
#     "Find emerging KRAS inhibitors "   
#     "and supporting evidence" 
# )

query = input(
    "\nEnter your research query: "
)


state = {

    "query": query,
    "intent": "",
    "selected_agents": [],
    "foundation_result": {},
    "graph_result": {},
    "publication_result": {},
    "final_report": ""
}

result = graph.invoke( state)

print(result["final_report"])