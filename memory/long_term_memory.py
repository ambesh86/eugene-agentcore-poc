import json
import os


class LongTermMemory:

    FILE_PATH = "data/long_term_memory.json"

    def save(self, entity, data):

        memory = self.load_all()

        memory[entity] = data

        with open(
            self.FILE_PATH,
            "w"
        ) as file:
            json.dump(
                memory,
                file,
                indent=4
            )

    def load(self, entity):

        memory = self.load_all()

        return memory.get(entity)

    def load_all(self):

        if not os.path.exists(
            self.FILE_PATH
        ):
            return {}

        with open(
            self.FILE_PATH,
            "r"
        ) as file:
            return json.load(file)