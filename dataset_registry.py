import json

def load_datasets():
    with open("datasets.json", "r") as f:
        return json.load(f)

def get_dataset(dataset_id):
    datasets = load_datasets()

    for dataset in datasets:
        if dataset["dataset_id"] == dataset_id:
            return dataset

    return None