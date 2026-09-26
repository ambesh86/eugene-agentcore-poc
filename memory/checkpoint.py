import json


def save_checkpoint(state):

    with open(
            "checkpoint.json",
            "w"
    ) as fp:

        json.dump(
            state,
            fp,
            indent=4
        )