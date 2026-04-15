# ============================================================
# CYCLOMATIC COMPLEXITY MODULE
# ------------------------------------------------------------
# Estimates cyclomatic complexity from PR diff/code patches.
# Complexity is derived by counting branching constructs
# (if, elif, else, for, while, case, except, and, or, &&, ||)
# across all file changes in the PR.
#
# Output per PR:
#   - total_complexity  : raw branch-point count
#   - complexity_label  : Low / Moderate / High / Very High
#   - complexity_score  : normalised 0–1 for pipeline use
#   - file_breakdown    : per-file detail
# ============================================================

import re

# ----------------------------------------------------------------
# Branch keywords (language-agnostic heuristic)
# ----------------------------------------------------------------
_BRANCH_PATTERNS = re.compile(
    r'\b(if|elif|else|for|while|case|except|catch|finally'
    r'|switch|unless|until|&&|\|\|)\b',
    re.IGNORECASE
)

# ----------------------------------------------------------------
# Thresholds (McCabe-inspired)
# ----------------------------------------------------------------
COMPLEXITY_THRESHOLDS = {
    "low":       (0,  10),
    "moderate":  (11, 20),
    "high":      (21, 40),
    "very_high": (41, float("inf")),
}


def _count_branches(code: str) -> int:
    """Count branch-point tokens in a block of code/diff text."""
    # Strip diff markers so we only analyse added/context lines
    lines = [
        line[1:] if line.startswith(("+", "-", " ")) else line
        for line in code.splitlines()
        if not line.startswith("---") and not line.startswith("+++")
    ]
    return len(_BRANCH_PATTERNS.findall("\n".join(lines)))


def _label_from_count(count: int) -> str:
    for label, (lo, hi) in COMPLEXITY_THRESHOLDS.items():
        if lo <= count <= hi:
            return label
    return "very_high"


def _normalise(count: int, ceiling: int = 50) -> float:
    """Map raw count to [0, 1]. Values above ceiling clamp to 1."""
    return min(count / ceiling, 1.0)


# ----------------------------------------------------------------
# Public API
# ----------------------------------------------------------------

def compute_cyclomatic_complexity(pr: dict) -> dict:
    """
    Analyse a PR dict and return a complexity summary.

    Expected PR fields (all optional – degrades gracefully):
        pr["files"]   : list of {"filename": str, "patch": str}
        pr["diff"]    : raw unified diff string (fallback)
        pr["commits"] : list of {"message": str}  (last resort)

    Returns:
        {
            "total_complexity": int,
            "complexity_label": str,
            "complexity_score": float,   # 0–1, higher = more complex
            "file_breakdown":  list[dict]
        }
    """
    file_breakdown = []
    total = 0

    # ── Strategy 1: per-file patches (richest signal) ──────────
    files = pr.get("files", [])
    if files:
        for f in files:
            patch = f.get("patch", "") or ""
            count = _count_branches(patch)
            total += count
            file_breakdown.append({
                "filename":   f.get("filename", "unknown"),
                "complexity": count,
                "label":      _label_from_count(count),
            })

    # ── Strategy 2: raw unified diff ───────────────────────────
    elif pr.get("diff"):
        count = _count_branches(pr["diff"])
        total = count
        file_breakdown.append({
            "filename":   "diff",
            "complexity": count,
            "label":      _label_from_count(count),
        })

    # ── Strategy 3: commit messages (coarse proxy) ─────────────
    elif pr.get("commits"):
        messages = " ".join(c.get("message", "") for c in pr["commits"])
        count = _count_branches(messages)
        total = count
        file_breakdown.append({
            "filename":   "commit_messages",
            "complexity": count,
            "label":      _label_from_count(count),
        })

    label = _label_from_count(total)
    score = _normalise(total)

    return {
        "total_complexity": total,
        "complexity_label": label,
        "complexity_score": round(score, 3),
        "file_breakdown":   file_breakdown,
    }
