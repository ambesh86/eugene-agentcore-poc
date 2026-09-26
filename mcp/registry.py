from tools.foundation_tools import search_drug
from tools.foundation_tools import search_gene

from tools.graph_tools import graph_traversal
from tools.graph_tools import similarity_search

from tools.publication_tools import search_publications
from tools.gds_tools import (
run_pagerank,
run_centrality,
run_betweenness,
run_closeness,
)


TOOLS = {
    "search_drug": search_drug,
    "search_gene": search_gene,
    "graph_traversal": graph_traversal,
    "similarity_search": similarity_search,
    "search_publications": search_publications,
    "pagerank": run_pagerank,
    "degree_centrality": run_centrality,
    "betweenness": run_betweenness,
    "closeness": run_closeness
}
