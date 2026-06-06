import json
import pandas as pd

def load_data(limit=1000):
    data = []

    with open(
        "data/arxiv-metadata-oai-snapshot.json",
        "r",
        encoding="utf-8"
    ) as f:

        for i, line in enumerate(f):

            if i >= limit:
                break

            paper = json.loads(line)

            data.append({
                "title": paper.get("title", ""),
                "summary": paper.get("abstract", "")
            })

    return pd.DataFrame(data)