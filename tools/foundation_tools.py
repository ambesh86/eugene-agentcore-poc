from retrievers.drug_retriever import DrugRetriever

def search_drug(query):
    retriever = DrugRetriever()
    return retriever.search(query)


def search_gene(gene_name: str):

    return {
        "gene": gene_name,
        "pathway": "MAPK"
    }