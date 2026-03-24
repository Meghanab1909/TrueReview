from api.github_api import *
from extract.normalize import *
from analysis.acceptance import is_accepted
from analysis.post_merge import get_post_merge_commits
from analysis.bug_detection import detect_bug_commits
from analysis.churn import compute_churn
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
    prs = merged_prs[:100]
    
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
        # Acceptance
        pr_data["accepted"] = is_accepted(pr_data)

        # Post-merge commits
        post_commits = get_post_merge_commits(pr_data)
        pr_data["post_merge_commits"] = post_commits

        # Bug detection
        bug_commits = detect_bug_commits(post_commits)
        pr_data["bug_count"] = len(bug_commits)

        # Churn
        pr_data["churn"] = compute_churn(pr_data)

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
            "accepted": pr["accepted"],
            "num_commits": len(pr["commits"]),
            "bug_count": pr["bug_count"],
            "churn": pr["churn"]
})

    
    df = pd.DataFrame(flat_data)
    df.to_csv("data/final_dataset.csv", index=False)
    print("✅ CSV File")


if __name__ == "__main__":
    build_dataset()