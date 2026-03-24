import pandas as pd

def compute_dataset_metrics():
    df = pd.read_csv("data/final_dataset.csv")

    metrics = {
        "acceptance_rate": df["accepted"].mean(),
        "avg_churn": df["churn"].mean(),
        "bug_rate": (df["bug_count"] > 0).mean()
    }

    print(metrics)
    return metrics