import pandas as pd
import matplotlib.pyplot as plt

def visualize():
    df = pd.read_json("data/analyzed_dataset.json")

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # 1. Acceptance
    df["accepted"].value_counts().plot(kind="bar", ax=axs[0, 0])
    axs[0, 0].set_title("Acceptance Distribution")

    # 2. Bug count
    df["bug_count"].plot(kind="hist", ax=axs[0, 1])
    axs[0, 1].set_title("Bug Distribution")

    # 3. Churn
    df["churn"].plot(kind="hist", ax=axs[1, 0])
    axs[1, 0].set_title("Churn Distribution")

    # 4. Effectiveness Score
    df["effectiveness_score"].plot(kind="hist", ax=axs[1, 1])
    axs[1, 1].set_title("Effectiveness Score")
    plt.suptitle("Code Review Effectiveness Dashboard", fontsize=16)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    visualize()