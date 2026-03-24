BUG_KEYWORDS = [
    "fix", "fixed", "bug", "error",
    "issue", "patch", "resolve"
]

def detect_bug_commits(commits):
    return [
        c for c in commits
        if any(k in c["message"].lower() for k in BUG_KEYWORDS)
    ]