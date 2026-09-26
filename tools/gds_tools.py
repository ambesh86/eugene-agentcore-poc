from graph.gds_service import GDSService


def run_pagerank():
    return GDSService().pagerank()

def run_centrality():
    return GDSService().degree_centrality()

def run_betweenness():
    return GDSService().betweenness()

def run_closeness():
    return GDSService().closeness()

print("Running PageRank")
run_pagerank()

print("Running Degree Centrality")
run_centrality()

print("Running Betweenness")
run_betweenness()

print("Running Closeness")
run_closeness()
