from api.github_api import *
from extract.normalize import *
import json
import os
import pandas as pd
import time 

OWNER = "django"
REPO = "django"


def build_dataset():
    all_data = []
    prs = get_all_prs(OWNER, REPO)
    merged_prs = [pr for pr in prs if pr["merged_at"] is not None]
    prs = merged_prs[:20]
    
    for pr in prs:
        pr_number = pr["number"]

        print(f"Processing PR #{pr_number}, merged: {pr['merged_at']}")

        pr_data = normalize_pr(pr)

        comments = get_pr_comments(OWNER, REPO, pr_number)
        review_comments = get_review_comments(OWNER, REPO, pr_number)
        commits = get_commits(OWNER, REPO, pr_number)

        pr_data["comments"] = [normalize_comment(c) for c in comments]
        pr_data["review_comments"] = [normalize_comment(c) for c in review_comments]
        pr_data["commits"] = [normalize_commit(c) for c in commits]

        # basic acceptance logic
        pr_data["accepted"] = pr_data["merged_at"] is not None

        all_data.append(pr_data)

        time.sleep(0.5)

    os.makedirs("data", exist_ok=True)

    with open("data/final_dataset.json", "w") as f:
        json.dump(all_data, f, indent=2)

    print("✅ JSON File")

    flat_data = []
    for pr in all_data:
        flat_data.append({
        "pr_id": pr["pr_id"],
        "author": pr["author"],
        "created_at": pr["created_at"],
        "merged_at": pr["merged_at"],
        "num_comments": len(pr["comments"]),
        "num_review_comments": len(pr["review_comments"]),
        "num_commits": len(pr["commits"]),
        "accepted": pr["accepted"]
    })
    
    df = pd.DataFrame(flat_data)
    df.to_csv("data/final_dataset.csv", index=False)
    print("✅ CSV File")


if __name__ == "__main__":
    build_dataset()