import networkx as nx

from utils.s3_client import read_json


class GDSService:

    def build_graph(self):

        data = read_json("data/graph.json")

        G = nx.DiGraph()

        for node in data["nodes"]:

            G.add_node(
                node["id"]
            )

        for edge in data["edges"]:

            G.add_edge(
                edge["source"],
                edge["target"]
            )

        return G

    def pagerank(self):
        G = self.build_graph()
        return nx.pagerank(G)

    def degree_centrality(self):
        G = self.build_graph()
        return nx.degree_centrality(G)


    def betweenness(self):
        G = self.build_graph()

        return nx.betweenness_centrality(G)

    def closeness(self):
        G = self.build_graph()
        return nx.closeness_centrality(G)