KNOWN_ENTITIES = [
    "KRAS",
    "EGFR",
    "BRAF",
    "Sotorasib",
    "Adagrasib"
]


def extract_entity(query):

    query_upper = query.upper()

    for entity in KNOWN_ENTITIES:

        if entity.upper() in query_upper:
            return entity

    return query