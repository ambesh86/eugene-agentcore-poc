from utils.s3_client import read_json

class DrugRetriever:

    def search(self, query):

        data = read_json("data/drugs.json")

        query = query.lower()

        matches = []

        for record in data:

            searchable_text = " ".join(
                str(v)
                for v in record.values()
            ).lower()

            if query in searchable_text:
                matches.append(
                    record
                )

        return matches