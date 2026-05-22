"""
Extract commit message, commit id, and project name from all .diff files under
rq2_1_evolved_rules/file_diffs, then use git commands to fetch file change info for each commit.
"""

import os
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Optional


def parse_diff_file(diff_file_path: Path) -> List[Dict]:
    """
    Parse a diff file and extract commit information (commit message only).

    Args:
        diff_file_path: Path to the diff file

    Returns:
        A list of commit info dicts, each containing:
        - commit_id: commit hash
        - commit_message: commit message (may span multiple lines)
        - project_name: project name extracted from the path
        - file_name: diff filename
    """
    commits = []

    try:
        with open(diff_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Failed to read file {diff_file_path}: {e}")
        return commits

    # Extract project name (first-level folder under file_diffs)
    parts = diff_file_path.parts
    file_diffs_index = None
    for i, part in enumerate(parts):
        if part == 'file_diffs':
            file_diffs_index = i
            break

    if file_diffs_index is None or file_diffs_index + 1 >= len(parts):
        project_name = "unknown"
    else:
        project_name = parts[file_diffs_index + 1]

    # Match all commit blocks with regex
    # Commit format:
    # commit <commit_id>
    # Author: ...
    # AuthorDate: ...
    # Commit: ...
    # CommitDate: ...
    #
    # <commit message> (may be empty or indented)
    #
    # diff --git ...

    # Find positions of all commit lines first
    commit_line_pattern = re.compile(r'^commit\s+([a-f0-9]+)', re.MULTILINE)
    commit_matches = list(commit_line_pattern.finditer(content))

    for i, commit_match in enumerate(commit_matches):
        # Skip the first commit (i == 0)
        if i == 0:
            continue

        commit_id = commit_match.group(1)
        start_pos = commit_match.start()

        # Find the next commit or end of file
        if i + 1 < len(commit_matches):
            end_pos = commit_matches[i + 1].start()
        else:
            end_pos = len(content)

        commit_block = content[start_pos:end_pos]

        # Extract commit message
        # Look for a blank line after CommitDate, then the message until diff --git
        # or similarity index. Message may be empty, multi-line, and/or indented.
        # Empty message: CommitDate is immediately followed by diff --git or similarity index.

        # Check for empty message (only whitespace between CommitDate and diff --git
        # or similarity index). Use \s* so .*? does not skip real message text.
        empty_message_pattern1 = re.compile(
            r'CommitDate:\s+[^\n]*\n\n\s*(diff\s+--git)',
            re.DOTALL
        )
        empty_message_pattern2 = re.compile(
            r'CommitDate:\s+[^\n]*\n\n\s*(similarity\s+index)',
            re.DOTALL
        )

        if empty_message_pattern1.search(commit_block) or empty_message_pattern2.search(commit_block):
            commit_message = ""
        else:
            # Try extracting a non-empty message between CommitDate and diff --git
            # or similarity index
            message_pattern = re.compile(
                r'CommitDate:\s+.*?\n'
                r'\n'
                r'(.*?)'  # commit message (may be multi-line and indented)
                r'\n(?:diff\s+--git|similarity\s+index)',
                re.DOTALL
            )

            message_match = message_pattern.search(commit_block)
            if message_match:
                commit_message = message_match.group(1)
                # Remove leading whitespace on each line (often 4-space indent)
                lines = commit_message.split('\n')
                cleaned_lines = [line.lstrip() for line in lines]
                commit_message = '\n'.join(cleaned_lines)
                # Collapse consecutive blank lines to a single newline
                commit_message = re.sub(r'\n\s*\n+', '\n', commit_message)
                commit_message = commit_message.strip()
            else:
                # Default to empty message (no warning; empty messages are valid)
                commit_message = ""

        commits.append({
            'commit_id': commit_id,
            'commit_message': commit_message,
            'project_name': project_name,
            'file_name': diff_file_path.name
        })

    return commits


def get_file_changes_from_git(project_path: Path, commit_id: str) -> Optional[List[Dict]]:
    """
    Use git commands to fetch file change information for a commit.

    Args:
        project_path: Repository path
        commit_id: Commit hash

    Returns:
        A list of file change dicts, each containing:
        - file_path: full file path (new path when renamed)
        - old_path: old path (only for renames)
        - change_type: added/modified/deleted/renamed
        - lines_added: number of added lines
        - lines_deleted: number of deleted lines
        Returns None on failure
    """
    if not project_path.exists():
        return None

    file_changes = []

    try:
        # Use git diff to fetch file change info
        # First fetch file status
        status_result = subprocess.run(
            ['git', 'diff', '--name-status', f'{commit_id}^..{commit_id}'],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Then fetch line counts
        numstat_result = subprocess.run(
            ['git', 'diff', '--numstat', f'{commit_id}^..{commit_id}'],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        if status_result.returncode != 0 or numstat_result.returncode != 0:
            print(f"  Warning: unable to fetch file info for commit {commit_id}: {status_result.stderr.strip() or numstat_result.stderr.strip()}")
            return None

        # Parse status output and map file paths to change types
        # For renames, keep both old and new path mappings
        status_map = {}
        rename_map = {}  # new path -> old path

        for line in status_result.stdout.strip().split('\n'):
            if not line.strip():
                continue
            parts = line.split('\t')

            if len(parts) >= 2:
                status = parts[0]

                # Rename: R100 old_path new_path (3 fields)
                if status.startswith('R'):
                    if len(parts) >= 3:
                        old_path = parts[1]
                        new_path = parts[2]
                        rename_map[new_path] = old_path
                        file_path = new_path
                    else:
                        # Fallback when format is unexpected
                        file_path = parts[1]
                        if ' => ' in file_path:
                            old_path, new_path = file_path.split(' => ', 1)
                            rename_map[new_path] = old_path
                            file_path = new_path
                else:
                    file_path = parts[1]
                    # Handle other => formats
                    if ' => ' in file_path:
                        file_path = file_path.split(' => ', 1)[-1]

                # Map status codes
                if status.startswith('A'):
                    change_type = 'added'
                elif status.startswith('D'):
                    change_type = 'deleted'
                elif status.startswith('R'):
                    change_type = 'renamed'
                else:
                    change_type = 'modified'

                status_map[file_path] = change_type

        # Parse numstat output
        for line in numstat_result.stdout.strip().split('\n'):
            if not line.strip():
                continue
            parts = line.split('\t')
            if len(parts) >= 3:
                try:
                    lines_added = int(parts[0]) if parts[0] != '-' else 0
                    lines_deleted = int(parts[1]) if parts[1] != '-' else 0
                    file_path = parts[2]

                    # Handle git rename path formats
                    # Format 1: path/{ => new_dir}/filename
                    #   e.g. .cursor/rules/{ => design}/site.mdc
                    #   becomes .cursor/rules/design/site.mdc
                    # Format 2: prefix{old => new}suffix (prefix may be empty)
                    #   e.g. scripts/{deployment => maintenance}/auto-deploy.sh
                    #   becomes scripts/maintenance/auto-deploy.sh
                    #   e.g. {app/panel/src/__tests__/ui-improvements => docs}/ACCESSIBILITY_VALIDATION_SUMMARY.md
                    #   becomes docs/ACCESSIBILITY_VALIDATION_SUMMARY.md
                    #   e.g. {docs => .kiro/steering}/clean-work-etiquette.md
                    #   becomes .kiro/steering/clean-work-etiquette.md
                    if ' => ' in file_path and '{' in file_path and '}' in file_path:
                        rename_pattern1 = re.compile(r'(.+?)\{ => ([^}]+)\}(.+)')
                        match1 = rename_pattern1.match(file_path)
                        if match1:
                            prefix = match1.group(1)
                            new_part = match1.group(2)
                            suffix = match1.group(3)
                            file_path = prefix + new_part + suffix
                        else:
                            # Format 2: prefix{old => new}suffix (prefix/new may be empty)
                            # e.g. docs/{maintenance => }/system-fixes-reference.md
                            rename_pattern2 = re.compile(r'(.*?)\{([^}]+) => ([^}]*)\}(.*)')
                            match2 = rename_pattern2.match(file_path)
                            if match2:
                                prefix = match2.group(1) or ''
                                new_part = match2.group(3) or ''
                                suffix = match2.group(4) or ''
                                file_path = prefix + new_part + suffix
                                # Normalize double slashes when new_part is empty
                                file_path = re.sub(r'/+', '/', file_path)
                            else:
                                # Fallback: strip { => } portion without leaving stray }
                                file_path = re.sub(r'\{[^}]* => ([^}]+)\}', r'\1', file_path)
                    elif ' => ' in file_path:
                        file_path = file_path.split(' => ', 1)[-1]

                    change_type = status_map.get(file_path, 'modified')

                    file_info = {
                        'file_path': file_path,
                        'change_type': change_type,
                        'lines_added': lines_added,
                        'lines_deleted': lines_deleted
                    }

                    if change_type == 'renamed' and file_path in rename_map:
                        file_info['old_path'] = rename_map[file_path]

                    file_changes.append(file_info)
                except (ValueError, IndexError):
                    continue

    except subprocess.TimeoutExpired:
        print(f"  Warning: timed out fetching file info for commit {commit_id}")
        return None
    except Exception as e:
        print(f"  Warning: error fetching file info for commit {commit_id}: {e}")
        return None

    return file_changes


def extract_all_commits(repo_root: Path) -> List[Dict]:
    """
    Extract commit information from all .diff files under rq2_1_evolved_rules/file_diffs.

    Args:
        repo_root: Repository root directory

    Returns:
        List of all commit info dicts
    """
    file_diffs_dir = repo_root / "rq2_1_evolved_rules" / "file_diffs"

    if not file_diffs_dir.exists():
        print(f"Directory not found: {file_diffs_dir}")
        return []

    all_commits = []

    # Walk all .diff files
    for diff_file in file_diffs_dir.rglob('*.diff'):
        commits = parse_diff_file(diff_file)
        all_commits.extend(commits)
        print(f"Processed: {diff_file.relative_to(file_diffs_dir)} - found {len(commits)} commit(s)")

    return all_commits


def enrich_commits_with_file_changes(commits: List[Dict], repo_root: Path) -> List[Dict]:
    """
    Add file change information to each commit via git commands.

    Args:
        commits: List of commit info dicts
        repo_root: Repository root directory

    Returns:
        Commits enriched with file change information
    """
    cloned_repos_dir = repo_root / 'cloned_repositories'

    if not cloned_repos_dir.exists():
        print(f"Warning: cloned_repositories directory not found: {cloned_repos_dir}")
        return commits

    enriched_commits = []

    for i, commit in enumerate(commits, 1):
        project_name = commit['project_name']
        commit_id = commit['commit_id']

        # Locate the matching project directory
        project_path = cloned_repos_dir / project_name

        print(f"[{i}/{len(commits)}] Processing commit {commit_id} (project: {project_name})...")

        file_changes = get_file_changes_from_git(project_path, commit_id)

        if file_changes is not None:
            commit['file_changes'] = file_changes
            print(f"  Found {len(file_changes)} changed file(s)")
        else:
            commit['file_changes'] = []
            print(f"  No file change info found")

        enriched_commits.append(commit)

    return enriched_commits


def output_results(commits: List[Dict]):
    """
    Write results to a txt file.

    Args:
        commits: List of commit info dicts
    """
    script_dir = Path(__file__).parent
    output_file = script_dir / 'commit_info.txt'

    with open(output_file, 'w', encoding='utf-8') as f:
        for i, commit in enumerate(commits, 1):
            f.write(f"{'='*80}\n")
            f.write(f"Commit #{i}\n")
            f.write(f"{'='*80}\n")
            f.write(f"Commit ID: {commit['commit_id']}\n")
            f.write(f"Project: {commit['project_name']}\n")
            f.write(f"File: {commit['file_name']}\n")
            f.write(f"Commit Message:\n{commit['commit_message']}\n")
            f.write(f"\n")

            # Write file change information
            file_changes = commit.get('file_changes', [])
            if file_changes:
                f.write(f"Changed Files:\n")
                for file_change in file_changes:
                    change_type = file_change['change_type']
                    lines_added = file_change['lines_added']
                    lines_deleted = file_change['lines_deleted']

                    if change_type == 'renamed' and 'old_path' in file_change:
                        # Rename format: renamed <old_path> <new_path> <added> <deleted>
                        old_path = file_change['old_path']
                        new_path = file_change['file_path']
                        f.write(f"renamed {old_path} {new_path} {lines_added} {lines_deleted}\n")
                    else:
                        # Other types: <change_type> <file_path> <added> <deleted>
                        file_path = file_change['file_path']
                        f.write(f"{change_type} {file_path} {lines_added} {lines_deleted}\n")
            else:
                f.write(f"Changed Files:\n")

            f.write(f"\n")

    print(f"\nResults saved to: {output_file}")
    print(f"Extracted {len(commits)} commit(s)")


def main():
    """Main entry point."""
    repo_root = Path(__file__).parent.parent

    print("Extracting commit information...")
    print(f"Search directory: {repo_root / 'rq2_1_evolved_rules' / 'file_diffs'}\n")

    # Step 1: extract commit messages from diff files
    commits = extract_all_commits(repo_root)

    if not commits:
        print("No commit information found")
        return

    print(f"\nFound {len(commits)} commit(s)")
    print("\nFetching file change info via git...\n")

    # Step 2: fetch file change info via git
    commits = enrich_commits_with_file_changes(commits, repo_root)

    # Write txt output
    print("\n" + "="*80)
    output_results(commits)

    # Summary statistics
    print("\n" + "="*80)
    print("Summary:")
    project_counts = {}
    for commit in commits:
        project = commit['project_name']
        project_counts[project] = project_counts.get(project, 0) + 1

    print(f"Total commits: {len(commits)}")
    print(f"Projects involved: {len(project_counts)}")
    print(f"\nCommits per project:")
    for project, count in sorted(project_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {project}: {count}")


if __name__ == '__main__':
    main()
