"""
Export commit windows for detect_rules.json.

For each unique (project, commit_id) in detect_rules.json:
- find N commits before and after it on main/master (including itself),
- de-duplicate commits per project,
- export per-commit metadata, per-file diff, and post-commit full file content.

Skip binary/dependency-heavy artifacts and very large file snapshots.
"""

import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

N = 5
MAX_TEXT_FILE_BYTES = 2 * 1024 * 1024  # 2MB guardrail for "after" file content

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RULE_JUDGE_DIR = Path(__file__).resolve().parent
CLONED_REPOS_DIR = PROJECT_ROOT / "cloned_repositories"
DETECT_RULES_JSON = RULE_JUDGE_DIR / "detect_rules.json"
OUTPUT_ROOT = RULE_JUDGE_DIR / "commit_windows_info"
LEGACY_OUTPUT_ROOT = RULE_JUDGE_DIR / "commit_windows_export"

SKIP_PATH_PARTS = {
    "node_modules",
    ".venv",
    "venv",
    ".git",
    "vendor",
    "third_party",
    "target",
    ".next",
    ".turbo",
    "coverage",
    "test-results",
}

SKIP_EXTENSIONS = {
    ".zip", ".jar",
    ".so", ".dll", ".dylib", ".exe", ".class", ".ttf", ".woff", ".woff2",
    ".mp3", ".mp4", ".mov", ".avi", ".webm", ".wasm",
    # ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", 
}


def run_git(repo_path: Path, args: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git"] + args,
        cwd=repo_path,
        capture_output=True,
        text=False,
        timeout=120,
    )


def to_text(raw: bytes) -> str:
    if not raw:
        return ""
    return raw.decode("utf-8", errors="replace")


def choose_branch(repo_path: Path) -> Optional[str]:
    for branch in ("main", "master", "develop"):
        res = run_git(repo_path, ["rev-parse", "--verify", branch])
        if res.returncode == 0:
            return branch
    return None


def sanitize_filename(file_path: str) -> str:
    safe = []
    for ch in file_path:
        if ch.isalnum() or ch in ("-", "_", "."):
            safe.append(ch)
        elif ch == "/":
            safe.append("__")
        else:
            safe.append("_")
    return "".join(safe)


def should_skip_file(file_path: str, ins: str, dele: str) -> Tuple[bool, str]:
    # git numstat uses '-' for binary files
    if ins == "-" or dele == "-":
        return True, "binary (numstat=-)"

    suffix = Path(file_path).suffix.lower()
    if suffix in SKIP_EXTENSIONS:
        return True, f"binary/dependency extension {suffix}"

    parts = set(Path(file_path).parts)
    hit_parts = sorted(parts.intersection(SKIP_PATH_PARTS))
    if hit_parts:
        return True, f"dependency/build path part: {','.join(hit_parts)}"

    return False, ""


def load_detect_rules() -> Dict[str, Set[str]]:
    with open(DETECT_RULES_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    project_to_commits: Dict[str, Set[str]] = {}
    for item in data:
        project = item.get("project")
        commit_id = item.get("commit_id")
        if not project or not commit_id:
            continue
        project_to_commits.setdefault(project, set()).add(commit_id)
    return project_to_commits


def get_commit_window_ids(rev_list: List[str], center_commit: str, n: int) -> List[str]:
    idx = rev_list.index(center_commit)
    start = max(0, idx - n)
    end = min(len(rev_list) - 1, idx + n)
    return rev_list[start : end + 1]


def get_numstat(repo_path: Path, commit_id: str) -> List[Tuple[str, str, str]]:
    res = run_git(repo_path, ["show", "--numstat", "--format=", "--no-renames", commit_id])
    if res.returncode != 0:
        return []
    stdout_text = to_text(res.stdout)
    out: List[Tuple[str, str, str]] = []
    for line in stdout_text.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        out.append((parts[0], parts[1], parts[2]))
    return out


def file_exists_at_commit(repo_path: Path, commit_id: str, file_path: str) -> bool:
    res = run_git(repo_path, ["cat-file", "-e", f"{commit_id}:{file_path}"])
    return res.returncode == 0


def get_file_content_at_commit(repo_path: Path, commit_id: str, file_path: str) -> str:
    res = run_git(repo_path, ["show", f"{commit_id}:{file_path}"])
    if res.returncode != 0:
        return ""
    return to_text(res.stdout)


def get_file_diff_for_commit(repo_path: Path, commit_id: str, file_path: str) -> str:
    res = run_git(repo_path, ["show", "--format=", "--no-renames", commit_id, "--", file_path])
    if res.returncode != 0:
        return ""
    return to_text(res.stdout)


def count_lines(content: str) -> int:
    if not content:
        return 0
    return len(content.splitlines())


def build_repo_tree_text(repo_path: Path, commit_id: str) -> str:
    """
    Build a tree-like text from tracked file paths at a given commit.
    """
    res = run_git(repo_path, ["ls-tree", "-r", "--name-only", commit_id])
    if res.returncode != 0:
        return "[failed to read tree]"

    paths = [p.strip() for p in to_text(res.stdout).splitlines() if p.strip()]
    root: Dict[str, dict] = {}

    for p in paths:
        cur = root
        for part in p.split("/"):
            cur = cur.setdefault(part, {})

    lines: List[str] = []

    def walk(node: Dict[str, dict], prefix: str) -> None:
        names = sorted(node.keys())
        for i, name in enumerate(names):
            is_last = i == len(names) - 1
            connector = "└── " if is_last else "├── "
            lines.append(prefix + connector + name)
            child_prefix = prefix + ("    " if is_last else "│   ")
            walk(node[name], child_prefix)

    walk(root, "")
    return "\n".join(lines)


def export_project(repo: str, target_commits: Set[str]) -> None:
    repo_path = CLONED_REPOS_DIR / repo
    if not repo_path.is_dir():
        print(f"[SKIP] {repo}: repository folder not found")
        return

    branch = choose_branch(repo_path)
    if not branch:
        print(f"[SKIP] {repo}: no main/master/develop branch")
        return

    rev_res = run_git(repo_path, ["rev-list", branch])
    if rev_res.returncode != 0:
        print(f"[SKIP] {repo}: cannot read rev-list {branch}")
        return
    rev_list = [x.strip() for x in to_text(rev_res.stdout).splitlines() if x.strip()]
    rev_set = set(rev_list)

    needed: Set[str] = set()
    missing_targets = 0
    for commit_id in target_commits:
        if commit_id not in rev_set:
            missing_targets += 1
            continue
        for c in get_commit_window_ids(rev_list, commit_id, N):
            needed.add(c)

    project_out = OUTPUT_ROOT / repo
    project_out.mkdir(parents=True, exist_ok=True)

    exported = 0
    for commit_id in rev_list:
        if commit_id not in needed:
            continue
        commit_out = project_out / commit_id
        commit_out.mkdir(parents=True, exist_ok=True)

        msg_res = run_git(repo_path, ["log", "-1", "--format=%B", commit_id])
        message = to_text(msg_res.stdout).strip() if msg_res.returncode == 0 else ""

        numstat = get_numstat(repo_path, commit_id)
        files_dir = commit_out / "files"
        files_dir.mkdir(parents=True, exist_ok=True)

        meta_lines: List[str] = []
        meta_lines.append(f"project: {repo}")
        meta_lines.append(f"branch: {branch}")
        meta_lines.append(f"commit: {commit_id}")
        meta_lines.append("message:")
        meta_lines.append(message)
        meta_lines.append("")
        meta_lines.append("modified files:")
        skipped_count = 0

        for idx, (ins, dele, file_path) in enumerate(numstat, start=1):
            skip, reason = should_skip_file(file_path, ins, dele)
            if skip:
                skipped_count += 1
                meta_lines.append(
                    f"{file_path}\t+{ins}\t-{dele}\tafter_lines=SKIPPED\tskipped_reason={reason}"
                )
                continue

            exists_after = file_exists_at_commit(repo_path, commit_id, file_path)
            if exists_after:
                size_res = run_git(repo_path, ["cat-file", "-s", f"{commit_id}:{file_path}"])
                size_text = to_text(size_res.stdout).strip() if size_res.returncode == 0 else "0"
                try:
                    file_bytes = int(size_text)
                except ValueError:
                    file_bytes = 0

                if file_bytes > MAX_TEXT_FILE_BYTES:
                    content_after = (
                        f"[skipped: file content too large ({file_bytes} bytes), "
                        f"threshold={MAX_TEXT_FILE_BYTES} bytes]"
                    )
                    after_lines = 0
                    diff_text = get_file_diff_for_commit(repo_path, commit_id, file_path)
                    safe = sanitize_filename(file_path)
                    diff_file = files_dir / f"{idx:03d}__{safe}.diff.patch"
                    after_file = files_dir / f"{idx:03d}__{safe}.after.txt"
                    with open(diff_file, "w", encoding="utf-8") as f:
                        f.write(diff_text)
                    with open(after_file, "w", encoding="utf-8") as f:
                        f.write(content_after)
                    meta_lines.append(
                        f"{file_path}\t+{ins}\t-{dele}\tafter_lines=SKIPPED\tskipped_reason=too_large({file_bytes} bytes)"
                    )
                    continue

                content_after = get_file_content_at_commit(repo_path, commit_id, file_path)
                after_lines = count_lines(content_after)
            else:
                content_after = ""
                after_lines = 0

            diff_text = get_file_diff_for_commit(repo_path, commit_id, file_path)

            safe = sanitize_filename(file_path)
            diff_file = files_dir / f"{idx:03d}__{safe}.diff.patch"
            after_file = files_dir / f"{idx:03d}__{safe}.after.txt"

            with open(diff_file, "w", encoding="utf-8") as f:
                f.write(diff_text)
            with open(after_file, "w", encoding="utf-8") as f:
                if exists_after:
                    f.write(content_after)
                else:
                    f.write("[file not present after this commit]")

            meta_lines.append(f"{file_path}\t+{ins}\t-{dele}\tafter_lines={after_lines}")

        meta_lines.append("")
        meta_lines.append(f"skipped_files_count: {skipped_count}")
        meta_lines.append("")
        meta_lines.append("project_tree_after_this_commit:")
        meta_lines.append(build_repo_tree_text(repo_path, commit_id))

        with open(commit_out / "meta.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(meta_lines) + "\n")

        exported += 1

    print(
        f"[DONE] {repo}: targets={len(target_commits)}, missing_targets={missing_targets}, "
        f"exported_commits={exported}"
    )


def main() -> None:
    project_to_commits = load_detect_rules()
    if LEGACY_OUTPUT_ROOT.exists():
        shutil.rmtree(LEGACY_OUTPUT_ROOT)
    if OUTPUT_ROOT.exists():
        shutil.rmtree(OUTPUT_ROOT)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    print(f"Projects in detect_rules.json: {len(project_to_commits)}")
    print(f"N = {N}")
    print(f"Output root: {OUTPUT_ROOT}")

    for project, commits in sorted(project_to_commits.items()):
        export_project(project, commits)


if __name__ == "__main__":
    main()
