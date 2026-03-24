def is_accepted(pr):
    comments = pr["comments"] + pr["review_comments"]

    if not comments:
        return False

    author = pr["author"]

    author_replied = any(c["author"] == author for c in comments)
    multiple_commits = len(pr["commits"]) > 1

    return author_replied or multiple_commits