import json


def load_datasets():
    try:
        with open("datasets.json", "r") as f:
            return json.load(f) ा
    except FileNotFoundError:
        print("ERROR: datasets.json file not found")
        return {}


def get_dataset(dataset_id):
    datasets = load_datasets()

    return datasets.get(dataset_id)   # ✅ DIRECT ACCESS
