import json
from analysis.acceptance import is_accepted
from analysis.post_merge import get_post_merge_commits
from analysis.bug_detection import detect_bug_commits
from analysis.churn import compute_churn
from analysis.effectiveness import compute_effectiveness

def run_analysis():
    with open("data/final_dataset.json") as f:
        data = json.load(f)

    for pr in data:
        pr["accepted"] = is_accepted(pr)

        post = get_post_merge_commits(pr)
        pr["post_merge_commits"] = post

        bugs = detect_bug_commits(pr["commits"])
        pr["bug_count"] = len(bugs)

        pr["churn"] = compute_churn(pr)
        pr["effectiveness_score"] = compute_effectiveness(pr)
    with open("data/analyzed_dataset.json", "w") as f:
        json.dump(data, f, indent=2)

    print("✅ Analysis complete + saved")

if __name__ == "__main__":
    run_analysis()