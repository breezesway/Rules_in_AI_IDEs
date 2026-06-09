"""
LLM-as-a-judge for rule compliance on commit windows.
"""

from __future__ import annotations

import json
import random
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

try:
    from tqdm import tqdm
except Exception:
    def tqdm(iterable=None, total=None, desc=None, unit=None):  # type: ignore
        if iterable is None:
            class _Dummy:
                def __enter__(self):
                    return self

                def __exit__(self, exc_type, exc, tb):
                    return False

                def update(self, n=1):
                    return None

            return _Dummy()
        return iterable


# ==================== Configuration ====================
# OpenRouter API settings
API_URL = "https://openrouter.ai/api/v1/responses"
API_KEY = "<your-api-key>"
# Configure one or more models; the script runs each model sequentially
MODELS = ["google/gemini-3-flash-preview"]

# Commit window size (N commits before and after the rule commit)
WINDOW_N = 5

# Debug mode: random sample size (None = process all rules)
DEBUG_SAMPLE_SIZE = None

# If True, run filtering/stats only and write precheck_summary (skip prompts and LLM calls)
DRY_RUN = False

# Random seed (for debug sampling)
RANDOM_SEED = 23

# Concurrency and retries
MAX_WORKERS = 20
MAX_RETRIES = 10
# ==================================================

COMMIT_MAX_FILES = 50
COMMIT_MAX_CHANGED_LINES = 2000
FILE_MAX_CHANGED_LINES = 1000
P0_COMMIT_MAX_FILES = 80
P0_COMMIT_MAX_CHANGED_LINES = 3000


def get_model_name_identifier(model: str) -> str:
    if "/" in model:
        return model.split("/")[-1]
    return model.replace("/", "_").replace("\\", "_")


def get_unique_file_path(base_path: Path) -> Path:
    if not base_path.exists():
        return base_path
    stem = base_path.stem
    suffix = base_path.suffix
    counter = 2
    while True:
        candidate = base_path.parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def get_unique_dir_path(base_path: Path) -> Path:
    if not base_path.exists():
        return base_path
    counter = 2
    while True:
        candidate = base_path.parent / f"{base_path.name}_{counter}"
        if not candidate.exists():
            return candidate
        counter += 1


def read_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def parse_output_text(response_data: Dict[str, Any]) -> Optional[str]:
    try:
        output = response_data.get("output", [])
        if not isinstance(output, list):
            return None
        for item in output:
            if not isinstance(item, dict):
                continue
            if item.get("type") != "message":
                continue
            content = item.get("content", [])
            if not isinstance(content, list):
                continue
            for c in content:
                if isinstance(c, dict) and c.get("type") == "output_text":
                    text = c.get("text", "")
                    if text:
                        return text
        return None
    except Exception:
        return None


def parse_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    if not text:
        return None
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass

    try:
        m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, flags=re.DOTALL)
        if m:
            obj = json.loads(m.group(1))
            if isinstance(obj, dict):
                return obj
    except Exception:
        pass

    try:
        s = text.find("{")
        e = text.rfind("}")
        if s != -1 and e != -1 and e > s:
            obj = json.loads(text[s : e + 1])
            if isinstance(obj, dict):
                return obj
    except Exception:
        pass
    return None


def call_openrouter(system_prompt: str, user_prompt: str, model: str, api_key: str) -> Optional[Dict[str, Any]]:
    payload = {
        "input": [
            {
                "type": "message",
                "role": "system",
                "content": [{"type": "input_text", "text": system_prompt}],
            },
            {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": user_prompt}],
            },
        ],
        "model": model,
        "reasoning": {"effort": "high"},
        "response_format": {"type": "json_object"},
        "temperature": 1.0,
        "top_p": 0.95
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        resp = requests.post(API_URL, json=payload, headers=headers, timeout=120)
        if resp.status_code != 200:
            return None
        return resp.json()
    except Exception:
        return None


def parse_int(value: str) -> Optional[int]:
    try:
        return int(value)
    except Exception:
        return None


def parse_meta(meta_path: Path) -> Dict[str, Any]:
    text = meta_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    project = ""
    branch = ""
    commit = ""
    message_lines: List[str] = []
    in_message = False
    in_modified = False
    in_tree = False

    modified_entries: List[Dict[str, Any]] = []
    tree_lines: List[str] = []

    skipped_files_count = 0

    modified_re = re.compile(
        r"^(?P<path>.+?)\t\+(?P<add>\d+|-)\t-(?P<del>\d+|-)\tafter_lines=(?P<after>\S+)(?:\tskipped_reason=(?P<reason>.+))?$"
    )

    for ln in lines:
        if ln.startswith("project: "):
            project = ln[len("project: ") :].strip()
            continue
        if ln.startswith("branch: "):
            branch = ln[len("branch: ") :].strip()
            continue
        if ln.startswith("commit: "):
            commit = ln[len("commit: ") :].strip()
            continue
        if ln == "message:":
            in_message = True
            in_modified = False
            in_tree = False
            continue
        if ln == "modified files:":
            in_message = False
            in_modified = True
            in_tree = False
            continue
        if ln == "project_tree_after_this_commit:":
            in_message = False
            in_modified = False
            in_tree = True
            continue
        if ln.startswith("skipped_files_count:"):
            v = ln.split(":", 1)[1].strip()
            skipped_files_count = parse_int(v) or 0
            continue

        if in_message:
            message_lines.append(ln)
            continue
        if in_modified:
            if not ln.strip():
                continue
            m = modified_re.match(ln)
            if not m:
                continue
            p = m.group("path").strip()
            add_raw = m.group("add")
            del_raw = m.group("del")
            reason = m.group("reason")
            after_raw = m.group("after")
            add = parse_int(add_raw) if add_raw != "-" else None
            delete = parse_int(del_raw) if del_raw != "-" else None
            after_lines = parse_int(after_raw) if after_raw.isdigit() else None
            is_skipped = after_raw == "SKIPPED" or reason is not None or add is None or delete is None
            changed_lines = (add or 0) + (delete or 0)
            modified_entries.append(
                {
                    "path": p,
                    "additions": add,
                    "deletions": delete,
                    "changed_lines": changed_lines,
                    "after_lines": after_lines,
                    "is_skipped": is_skipped,
                    "skipped_reason": reason or "",
                    "raw_line": ln,
                }
            )
            continue
        if in_tree:
            tree_lines.append(ln)

    message = "\n".join(message_lines).strip()
    file_count = len(modified_entries)
    total_changed_lines = sum(x["changed_lines"] for x in modified_entries if not x["is_skipped"])

    return {
        "project": project,
        "branch": branch,
        "commit": commit,
        "message": message,
        "modified_entries": modified_entries,
        "skipped_files_count": skipped_files_count,
        "project_tree": "\n".join(tree_lines).rstrip(),
        "file_count": file_count,
        "total_changed_lines": total_changed_lines,
    }


def decode_diff_filename_to_path(name: str) -> Optional[str]:
    # e.g. 003__src__a.py.diff.patch -> src/a.py
    if not name.endswith(".diff.patch"):
        return None
    core = name[: -len(".diff.patch")]
    parts = core.split("__", 1)
    if len(parts) != 2:
        return None
    return parts[1].replace("__", "/")


def load_commit_diffs(commit_dir: Path) -> Dict[str, str]:
    files_dir = commit_dir / "files"
    if not files_dir.exists():
        return {}
    diffs: Dict[str, str] = {}
    for p in sorted(files_dir.glob("*.diff.patch")):
        fp = decode_diff_filename_to_path(p.name)
        if not fp:
            continue
        try:
            diffs[fp] = p.read_text(encoding="utf-8")
        except Exception:
            diffs[fp] = ""
    return diffs


def choose_nearest_boundary(target_idx: int, indices: List[int], side: str) -> Optional[int]:
    if not indices:
        return None
    if side == "before":
        candidates = [i for i in indices if i < target_idx]
        return max(candidates) if candidates else None
    candidates = [i for i in indices if i > target_idx]
    return min(candidates) if candidates else None


def build_relative_position_text(delta: int) -> str:
    # main_branch_commits matches git rev-list: smaller index = newer commit.
    # relative_delta = idx - target_idx, so positive = earlier in history, negative = later.
    if delta == 0:
        return "same_as_rule_commit (distance=0)"
    if delta > 0:
        return f"before_rule_commit (distance={delta})"
    return f"after_rule_commit (distance={abs(delta)})"


def build_changed_files_list(entries: List[Dict[str, Any]]) -> str:
    if not entries:
        return "(no changed files listed)"
    return "\n".join([x["raw_line"] for x in entries])


def build_diff_block(selected: List[Tuple[str, str]]) -> str:
    if not selected:
        return "(no diff content loaded)"
    chunks = []
    for path, content in selected:
        chunks.append(f"--- FILE: {path} ---\n{content}".rstrip())
    return "\n\n".join(chunks)


def render_user_prompt(template: str, values: Dict[str, str], dynamic_note: str) -> str:
    base = template.format(**values)
    if not dynamic_note:
        return base
    marker = f"- Changed Files List: \n{values['changed_files_list']}\n"
    insert = marker + dynamic_note + "\n"
    if marker in base:
        return base.replace(marker, insert, 1)
    return base


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def run_for_model(model: str) -> None:
    script_dir = Path(__file__).resolve().parent
    root_dir = script_dir.parent

    system_prompt_file = script_dir / "rule_compliance_system_prompt.txt"
    user_prompt_file = script_dir / "rule_compliance_user_prompt.txt"
    detect_rules_file = root_dir / "detect_rules.json"
    main_commits_file = root_dir / "main_branch_commits.json"
    before_after_file = root_dir / "rule_before_after_change" / "rule_before_after_change_results_kimi-k2.5.json"
    commit_windows_dir = root_dir / "commit_windows_info"

    system_prompt = load_text(system_prompt_file)
    user_prompt_template = load_text(user_prompt_file)
    rules: List[Dict[str, Any]] = read_json(detect_rules_file)
    main_commits = read_json(main_commits_file)
    if before_after_file.is_file():
        before_after_results: List[Dict[str, Any]] = read_json(before_after_file)
    else:
        print(
            f"Warning: before/after change file not found; skipping related filter: {before_after_file}"
        )
        before_after_results = []

    ba_map = {x.get("rule_id"): x for x in before_after_results if isinstance(x, dict) and x.get("rule_id")}
    random.seed(RANDOM_SEED)

    if DEBUG_SAMPLE_SIZE is not None and DEBUG_SAMPLE_SIZE < len(rules):
        rules = random.sample(rules, DEBUG_SAMPLE_SIZE)

    # rule -> candidate commit window
    prepared_rules: List[Dict[str, Any]] = []
    filtered_rule_count = 0
    filtered_reason_counter: Dict[str, int] = {}

    def inc_reason(k: str) -> None:
        filtered_reason_counter[k] = filtered_reason_counter.get(k, 0) + 1

    for rule in rules:
        rule_id = rule.get("rule_id", "unknown")
        project = rule.get("project", "")
        target_commit = rule.get("commit_id", "")

        project_data = main_commits.get(project, {})
        commits = project_data.get("commits", []) if isinstance(project_data, dict) else []
        if not commits or target_commit not in commits:
            filtered_rule_count += 1
            inc_reason("missing_main_branch_context")
            continue

        target_idx = commits.index(target_commit)
        start = max(0, target_idx - WINDOW_N)
        end = min(len(commits) - 1, target_idx + WINDOW_N)
        window_indices = list(range(start, end + 1))

        # rule_before_after_change filter
        ba_item = ba_map.get(rule_id)
        if ba_item and isinstance(ba_item, dict):
            llm = ba_item.get("llm", {}) if isinstance(ba_item.get("llm"), dict) else {}
            if llm.get("is_changed_before") is True or llm.get("is_changed_after") is True:
                filtered_rule_count += 1
                inc_reason("changed_before_after_flag_true")
                continue

            before_changes = llm.get("before_changes", []) if isinstance(llm.get("before_changes"), list) else []
            after_changes = llm.get("after_changes", []) if isinstance(llm.get("after_changes"), list) else []

            before_idxs: List[int] = []
            for x in before_changes:
                if isinstance(x, dict):
                    cid = x.get("commit_id")
                    if cid in commits:
                        before_idxs.append(commits.index(cid))
            after_idxs: List[int] = []
            for x in after_changes:
                if isinstance(x, dict):
                    cid = x.get("commit_id")
                    if cid in commits:
                        after_idxs.append(commits.index(cid))

            nearest_before = choose_nearest_boundary(target_idx, before_idxs, "before")
            nearest_after = choose_nearest_boundary(target_idx, after_idxs, "after")

            if nearest_before is not None:
                window_indices = [i for i in window_indices if i >= nearest_before]
            if nearest_after is not None:
                window_indices = [i for i in window_indices if i <= nearest_after]

        # Load commit metadata and apply commit-level filtering
        commit_jobs: List[Dict[str, Any]] = []
        for idx in window_indices:
            cid = commits[idx]
            commit_dir = commit_windows_dir / project / cid
            meta_path = commit_dir / "meta.txt"
            if not meta_path.exists():
                continue
            try:
                meta = parse_meta(meta_path)
            except Exception:
                continue

            # For commit-level filtering, exclude oversized single files (changed_lines > FILE_MAX_CHANGED_LINES)
            # so one huge file does not inflate commit size and trigger premature filtering.
            commit_effective_entries = [
                e
                for e in meta["modified_entries"]
                if (not e["is_skipped"]) and e["changed_lines"] <= FILE_MAX_CHANGED_LINES
            ]
            effective_file_count = len(commit_effective_entries)
            effective_total_changed_lines = sum(e["changed_lines"] for e in commit_effective_entries)

            is_p0_commit = idx == target_idx
            commit_file_threshold = P0_COMMIT_MAX_FILES if is_p0_commit else COMMIT_MAX_FILES
            commit_line_threshold = P0_COMMIT_MAX_CHANGED_LINES if is_p0_commit else COMMIT_MAX_CHANGED_LINES

            if effective_file_count > commit_file_threshold:
                continue
            if effective_total_changed_lines > commit_line_threshold:
                continue

            rel_delta = idx - target_idx
            relative_position = build_relative_position_text(rel_delta)

            if DRY_RUN:
                commit_jobs.append(
                    {
                        "rule_id": rule_id,
                        "project": project,
                        "target_commit": target_commit,
                        "commit_id": cid,
                        "relative_delta": rel_delta,
                        "relative_position": relative_position,
                        "rule": rule,
                    }
                )
                continue

            diff_map = load_commit_diffs(commit_dir)

            filtered_large_files: List[str] = []
            ignored_skipped_files: List[str] = []
            selected_diffs: List[Tuple[str, str]] = []

            for entry in meta["modified_entries"]:
                p = entry["path"]
                if entry["is_skipped"]:
                    ignored_skipped_files.append(p)
                    continue
                if entry["changed_lines"] > FILE_MAX_CHANGED_LINES:
                    filtered_large_files.append(p)
                    continue
                if p in diff_map:
                    selected_diffs.append((p, diff_map[p]))

            changed_files_list = build_changed_files_list(meta["modified_entries"])
            dynamic_lines = []
            if filtered_large_files:
                dynamic_lines.append(
                    "*(Note: The following files are filtered due to large per-file changes (>1000 lines): "
                    + ", ".join(filtered_large_files)
                    + ".)*"
                )
            if ignored_skipped_files:
                dynamic_lines.append(
                    "*(Note: The following files were modified but ignored because diff details are unavailable "
                    "(e.g., binary/skipped in meta): "
                    + ", ".join(ignored_skipped_files)
                    + ".)*"
                )
            dynamic_note = "\n".join(dynamic_lines).strip()

            values = {
                "first_level": str(rule.get("first_level", "")),
                "second_level": str(rule.get("second_level", "")),
                "rule_file_path": str(rule.get("file", "")),
                "change_type": str(rule.get("change_type", "")),
                "rule_content": str(rule.get("rule_content", "")),
                "detection_targets": str(rule.get("detection_targets", "")),
                "detection_logic": str(rule.get("detection_logic", "")),
                "relative_position": relative_position,
                "commit_message": str(meta.get("message", "")),
                "changed_files_list": changed_files_list,
                "project_tree_structure": str(meta.get("project_tree", "")),
                "file_diff_contents": build_diff_block(selected_diffs),
            }
            user_prompt = render_user_prompt(user_prompt_template, values, dynamic_note)

            commit_jobs.append(
                {
                    "rule_id": rule_id,
                    "project": project,
                    "target_commit": target_commit,
                    "commit_id": cid,
                    "relative_delta": rel_delta,
                    "relative_position": relative_position,
                    "user_prompt": user_prompt,
                    "rule": rule,
                }
            )

        before_count = sum(1 for x in commit_jobs if x["relative_delta"] < 0)
        after_count = sum(1 for x in commit_jobs if x["relative_delta"] > 0)
        if before_count == 0 or after_count == 0:
            filtered_rule_count += 1
            inc_reason("empty_before_or_after_after_filters")
            continue

        prepared_rules.append(
            {
                "rule": rule,
                "commit_jobs": commit_jobs,
                "before_count": before_count,
                "after_count": after_count,
            }
        )

    # Summary output
    total_rules = len(rules)
    final_rules = len(prepared_rules)
    print("\n========== Filter summary ==========")
    print(f"Total rules: {total_rules}")
    print(f"Filtered rules: {filtered_rule_count}")
    print(f"Rules used for compliance check: {final_rules}")
    print("Filter reason distribution:")
    for k, v in sorted(filtered_reason_counter.items(), key=lambda x: (-x[1], x[0])):
        print(f"  - {k}: {v}")

    dist_counter: Dict[str, int] = {}
    for item in prepared_rules:
        key = f"before={item['before_count']},after={item['after_count']}"
        dist_counter[key] = dist_counter.get(key, 0) + 1
    print("Before/after commit count distribution:")
    for k, v in sorted(dist_counter.items(), key=lambda x: x[0]):
        print(f"  - {k}: {v}")

    # Output directory
    model_name = get_model_name_identifier(model)
    base_output_dir = script_dir / f"rule_compliance_outputs_{model_name}"
    output_dir = get_unique_dir_path(base_output_dir)
    ensure_dir(output_dir)

    total_commit_jobs = sum(len(item["commit_jobs"]) for item in prepared_rules)
    precheck_path = output_dir / "precheck_summary.json"
    with open(precheck_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "total_rules": total_rules,
                "filtered_rules": filtered_rule_count,
                "final_rules": final_rules,
                "total_commit_jobs": total_commit_jobs,
                "filtered_reason_distribution": filtered_reason_counter,
                "before_after_distribution": dist_counter,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Precheck summary written to: {precheck_path}")
    print(f"Output directory: {output_dir}")

    if DRY_RUN:
        print(
            f"Dry-run mode: skipped prompt generation and LLM calls "
            f"({final_rules} rules, {total_commit_jobs} commit jobs)."
        )
        return

    prompts_dir = output_dir / "prompts"
    ensure_dir(prompts_dir)

    # Write one prompt file per rule/commit
    all_jobs: List[Dict[str, Any]] = []
    for item in prepared_rules:
        rule = item["rule"]
        rule_id = rule.get("rule_id", "unknown")
        rule_folder = prompts_dir / rule_id
        ensure_dir(rule_folder)
        for j in item["commit_jobs"]:
            rel = j["relative_delta"]
            rel_str = f"m{abs(rel)}" if rel < 0 else ("p0" if rel == 0 else f"p{rel}")
            prompt_file = rule_folder / f"{rel_str}__{j['commit_id']}.txt"
            with open(prompt_file, "w", encoding="utf-8") as pf:
                pf.write(j["user_prompt"])
            j["prompt_file"] = str(prompt_file)
            all_jobs.append(j)

    print(f"Prompt files written: {len(all_jobs)} commit jobs")

    api_key = API_KEY.strip()
    if not api_key or api_key == "<your-api-key>":
        raise RuntimeError("Missing API_KEY configuration; set it at the top of the script.")

    # Concurrent execution with retries
    result_lock = threading.Lock()
    pending = all_jobs[:]
    responses_all: List[Dict[str, Any]] = []
    results_all: List[Dict[str, Any]] = []
    failed_all: List[Dict[str, Any]] = []

    for round_idx in range(1, MAX_RETRIES + 1):
        if not pending:
            break
        print(f"\nRound {round_idx}: pending tasks = {len(pending)}")
        round_failed: List[Dict[str, Any]] = []

        def worker(job: Dict[str, Any]) -> Tuple[Dict[str, Any], bool, Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
            resp = call_openrouter(system_prompt, job["user_prompt"], model, api_key)
            if not resp:
                return job, False, None, None
            output_text = parse_output_text(resp)
            parsed = parse_json_from_text(output_text or "")
            if not output_text or not parsed:
                return job, False, resp, None
            compact = {
                "rule_id": job["rule_id"],
                "project": job["project"],
                "target_commit": job["target_commit"],
                "commit_id": job["commit_id"],
                "relative_delta": job["relative_delta"],
                "relative_position": job["relative_position"],
                "prompt_file": job["prompt_file"],
            }
            compact.update(parsed)
            return job, True, resp, compact

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
            futures = {ex.submit(worker, job): job for job in pending}
            with tqdm(total=len(pending), desc=f"round-{round_idx}", unit="commit") as pbar:
                for fut in as_completed(futures):
                    job, ok, raw_resp, compact = fut.result()
                    with result_lock:
                        if ok and compact is not None:
                            results_all.append(compact)
                            responses_all.append(
                                {
                                    "rule_id": job["rule_id"],
                                    "project": job["project"],
                                    "target_commit": job["target_commit"],
                                    "commit_id": job["commit_id"],
                                    "relative_delta": job["relative_delta"],
                                    "relative_position": job["relative_position"],
                                    "prompt_file": job["prompt_file"],
                                    "response": raw_resp,
                                }
                            )
                        else:
                            round_failed.append(job)
                    pbar.update(1)

        pending = round_failed
        print(
            f"Round {round_idx} complete: succeeded {len(all_jobs) - len(pending) - len(failed_all)}, "
            f"failed pending retry {len(pending)}"
        )

    failed_all = pending

    # Write results
    results_path = get_unique_file_path(output_dir / "rule_compliance_results.json")
    responses_path = get_unique_file_path(output_dir / "rule_compliance_all_responses.json")
    failed_path = get_unique_file_path(output_dir / "rule_compliance_failed_jobs.json")

    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results_all, f, ensure_ascii=False, indent=2)
    with open(responses_path, "w", encoding="utf-8") as f:
        json.dump(responses_all, f, ensure_ascii=False, indent=2)
    with open(failed_path, "w", encoding="utf-8") as f:
        json.dump(failed_all, f, ensure_ascii=False, indent=2)

    print("\n========== Run complete ==========")
    print(f"Total tasks: {len(all_jobs)}")
    print(f"Succeeded: {len(results_all)}")
    print(f"Failed: {len(failed_all)}")
    print(f"Results file: {results_path}")
    print(f"Full responses file: {responses_path}")
    print(f"Failed jobs file: {failed_path}")


def main() -> None:
    for model in MODELS:
        print("\n" + "=" * 80)
        print(f"Starting model: {model}")
        print("=" * 80)
        run_for_model(model)


if __name__ == "__main__":
    main()

