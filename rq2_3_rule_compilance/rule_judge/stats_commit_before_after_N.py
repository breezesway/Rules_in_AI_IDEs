"""
For each rule in detect_rules.json, find its commit in main_branch_commits.json,
compute how many commits are before (newer) and after (older) it.

If the number is greater than N, output N; otherwise output the real number (which is equal to min(count, N)).

Finally, count how many commits (per-rule entries) have either before < N or after < N.

This script prints results to console and does not write a JSON file.
"""

import json
from pathlib import Path

N = 5
RULE_JUDGE_DIR = Path(__file__).resolve().parent
MERGED_JSON = RULE_JUDGE_DIR / "detect_rules.json"
MAIN_COMMITS_JSON = RULE_JUDGE_DIR / "main_branch_commits.json"


def main() -> None:
    with open(MERGED_JSON, encoding="utf-8") as f:
        rules = json.load(f)
    with open(MAIN_COMMITS_JSON, encoding="utf-8") as f:
        main_commits = json.load(f)

    # commits list is newest-first: index 0 = HEAD, so "before" = newer commits = count = index
    # "after" = older commits = count = len - 1 - index
    before_lt_n_or_after_lt_n_count = 0
    error_count = 0

    for rule in rules:
        project = rule.get("project")
        commit_id = rule.get("commit_id")
        rule_id = rule.get("rule_id", "")

        if not project or not commit_id:
            error_count += 1
            print(f"{rule_id} | {project or ''} | {commit_id or ''} | ERROR: missing project/commit_id")
            continue

        proj_data = main_commits.get(project)
        if not proj_data:
            error_count += 1
            print(f"{rule_id} | {project} | {commit_id} | ERROR: project not found in main_branch_commits.json")
            continue

        commits = proj_data.get("commits") or []
        try:
            index = commits.index(commit_id)
        except ValueError:
            error_count += 1
            print(f"{rule_id} | {project} | {commit_id} | ERROR: commit_id not found in project main commits list")
            continue

        before = index  # commits newer than this one (listed before in the list)
        after = len(commits) - 1 - index  # commits older than this one (listed after)
        before_capped = min(before, N)
        after_capped = min(after, N)

        if before < N or after < N:
            before_lt_n_or_after_lt_n_count += 1

        print(f"{rule_id} | {project} | {commit_id} | before({N}-cap)={before_capped} | after({N}-cap)={after_capped}")

    print("-" * 80)
    print(f"N={N}")
    print(f"Count where before < N OR after < N: {before_lt_n_or_after_lt_n_count}")
    if error_count:
        print(f"Errors (missing/unknown project/commit): {error_count}")


if __name__ == "__main__":
    main()
