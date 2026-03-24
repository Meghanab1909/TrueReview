def compute_effectiveness(pr):
    score = 0

    # Acceptance (most important)
    if pr["accepted"]:
        score += 2   # weighted higher

    # Bug detection
    if pr["bug_count"] == 0:
        score += 1

    # Churn (less rework = better)
    if pr["churn"] <= 2:
        score += 1

    return score / 4   # normalize (0 to 1)