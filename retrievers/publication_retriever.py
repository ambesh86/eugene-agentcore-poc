from utils.s3_client import read_json


class PublicationRetriever:

    def search(self,
               query):

        data = read_json("data/publications.json")

        matches = []

        for article in data:

            if query.lower() in \
               str(article).lower():

                matches.append(
                    article
                )

        return matches