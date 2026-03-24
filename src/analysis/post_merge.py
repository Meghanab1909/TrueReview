from datetime import datetime

def get_post_merge_commits(pr):
    if not pr["merged_at"]:
        return []

    merged_time = datetime.fromisoformat(pr["merged_at"].replace("Z", ""))

    return [
        c for c in pr["commits"]
        if datetime.fromisoformat(c["timestamp"].replace("Z", "")) > merged_time
    ]