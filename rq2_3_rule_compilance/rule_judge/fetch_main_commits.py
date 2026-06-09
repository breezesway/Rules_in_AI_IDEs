"""
Read detect_rules.json, extract unique projects, and for each project
in cloned_repositories, collect all commit IDs from the main branch. Write results
to a JSON file and print commit counts per project.
"""

import json
import subprocess
from pathlib import Path
from typing import Optional

# Paths relative to project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RULE_JUDGE_DIR = Path(__file__).resolve().parent
MERGED_JSON = RULE_JUDGE_DIR / "detect_rules.json"
CLONED_REPOS_DIR = PROJECT_ROOT / "cloned_repositories"
OUTPUT_FILE = RULE_JUDGE_DIR / "main_branch_commits.json"


def get_unique_projects() -> set[str]:
    """Load detect_rules.json and return unique project names."""
    with open(MERGED_JSON, encoding="utf-8") as f:
        data = json.load(f)
    return set(item["project"] for item in data if "project" in item)


def get_main_branch_commits(repo_path: Path) -> tuple[list[str], Optional[str]]:
    """
    Get all commit IDs from the primary branch. Tries 'main', then 'master', then 'develop'.
    Returns (list of commit hashes, branch_name_used or None on error).
    """
    for branch in ("main", "master", "develop"):
        try:
            result = subprocess.run(
                ["git", "rev-list", branch],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0 and result.stdout.strip():
                commits = [line.strip() for line in result.stdout.strip().splitlines()]
                return (commits, branch)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue
    return ([], None)


def main() -> None:
    projects = sorted(get_unique_projects())
    results = {}
    print("Project commit counts (main branch):")
    print("-" * 50)

    for project in projects:
        repo_path = CLONED_REPOS_DIR / project
        if not repo_path.is_dir():
            print(f"  {project}: (folder not found)")
            results[project] = {"commits": [], "branch": None, "count": 0, "error": "folder not found"}
            continue

        commits, branch = get_main_branch_commits(repo_path)
        if branch is None:
            print(f"  {project}: (no main/master/develop branch or error)")
            results[project] = {"commits": [], "branch": None, "count": 0, "error": "no main/master/develop branch"}
        else:
            count = len(commits)
            print(f"  {project}: {count} commits (branch: {branch})")
            results[project] = {"commits": commits, "branch": branch, "count": count}

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("-" * 50)
    print(f"Results written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
