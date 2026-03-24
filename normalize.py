def normalize_pr(pr):
    return {
        "pr_id": pr["number"],
        "author": pr["user"]["login"],
        "created_at": pr["created_at"],
        "merged_at": pr["merged_at"],
        "state": pr["state"]
    }


def normalize_comment(comment):
    return {
        "author": comment["user"]["login"],
        "text": comment["body"],
        "timestamp": comment["created_at"]
    }


def normalize_commit(commit):
    return {
        "author": commit["commit"]["author"]["name"],
        "message": commit["commit"]["message"],
        "timestamp": commit["commit"]["author"]["date"]
    }