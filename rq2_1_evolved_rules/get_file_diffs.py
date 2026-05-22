"""
Script: Read rule_files_path.csv and save all commit diffs for files with commit_count > 1.
"""

import csv
import os
import subprocess
import sys
from pathlib import Path


def get_repo_name(project_name):
    """
    Extract repo_name from a project name.
    Format: {user_name}_{repo_name}, split on the first underscore.

    Args:
        project_name: Project name, e.g. "3sztof_k8s-virtual-coffee"

    Returns:
        str: Repository name, e.g. "k8s-virtual-coffee"
    """
    # Split on the first underscore
    parts = project_name.split('_', 1)
    if len(parts) == 2:
        return parts[1]  # Return the repo_name portion
    else:
        # If there is no underscore, return the original name
        return project_name


def get_diff_filename(file_path):
    """
    Extract the filename from a file path and append a .diff suffix.

    Args:
        file_path: File path, e.g. ".kiro/steering/auto-commit-tasks.md"

    Returns:
        str: Diff filename, e.g. "auto-commit-tasks.md.diff"
    """
    # Get filename (strip path)
    filename = os.path.basename(file_path)
    # Append .diff suffix
    return f"{filename}.diff"


def get_main_branch(repo_path):
    """
    Detect the repository's default branch name (main or master).

    Args:
        repo_path: Root directory path of the repository

    Returns:
        str: Default branch name, defaults to 'main'
    """
    try:
        original_dir = os.getcwd()
        os.chdir(repo_path)

        try:
            # Method 1: Check the remote default branch
            result = subprocess.run(
                ['git', 'symbolic-ref', 'refs/remotes/origin/HEAD'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                ref = result.stdout.strip()
                # Extract branch name, e.g. refs/remotes/origin/main -> main
                if 'origin/' in ref:
                    branch = ref.split('origin/')[-1]
                    return branch

            # Method 2: Check whether the main branch exists
            result = subprocess.run(
                ['git', 'show-ref', '--verify', '--quiet', 'refs/heads/main'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                return 'main'

            # Method 3: Check whether the master branch exists
            result = subprocess.run(
                ['git', 'show-ref', '--verify', '--quiet', 'refs/heads/master'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                return 'master'

            # Method 4: Check remote branches
            result = subprocess.run(
                ['git', 'branch', '-r'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                branches = result.stdout
                if 'origin/main' in branches:
                    return 'main'
                elif 'origin/master' in branches:
                    return 'master'

            # Default to main
            return 'main'

        finally:
            os.chdir(original_dir)

    except Exception:
        # On error, default to main
        return 'main'


def get_file_diff(repo_path, file_path, output_path):
    """
    Get all commit diffs for a file and save them to a file.
    Includes full history before and after renames.

    Args:
        repo_path: Root directory path of the repository
        file_path: Relative path of the file in the repository
        output_path: Full path of the output diff file

    Returns:
        bool: Whether the operation succeeded
    """
    try:
        # Check whether the file exists
        full_file_path = os.path.join(repo_path, file_path)
        if not os.path.exists(full_file_path):
            print(f"    ⚠️  文件不存在: {file_path}")
            return False

        # Ensure the output directory exists
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)

        # Switch to the repository directory
        original_dir = os.getcwd()
        os.chdir(repo_path)

        try:
            # Detect the default branch name
            main_branch = get_main_branch(repo_path)

            # Step 1: Find all historical paths for the file (including pre-rename paths)
            # Use git log --name-status to find all commits involving this file
            file_basename = os.path.basename(file_path)
            all_file_paths = {file_path}  # Include the current path

            # Find all commits involving this file and extract file paths
            # Search only the default branch (main or master)
            # Use --follow to include history across renames (align with commit-count script)
            name_status_result = subprocess.run(
                ['git', 'log', main_branch, '--follow', '--name-status', '--pretty=format:', '--', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )

            if name_status_result.returncode == 0:
                for line in name_status_result.stdout.split('\n'):
                    line = line.strip()
                    if line.startswith('R') and '\t' in line:
                        # Rename operation, format: R100    old_path    new_path
                        # Track both old and new paths regardless of basename changes
                        parts = line.split('\t')
                        if len(parts) >= 3:
                            old_path = parts[1]
                            new_path = parts[2]
                            all_file_paths.add(old_path)
                            all_file_paths.add(new_path)
                    elif line.startswith('C') and '\t' in line:
                        # Copy operation: only when the new path matches the target file,
                        # add the old path to track source history
                        parts = line.split('\t')
                        if len(parts) >= 3:
                            old_path = parts[1]
                            new_path = parts[2]
                            if new_path == file_path:
                                all_file_paths.add(old_path)
                    elif (line.startswith('A') or line.startswith('M')) and '\t' in line:
                        # Add or modify operation
                        parts = line.split('\t')
                        if len(parts) >= 2:
                            path = parts[1]
                            if file_basename in path:
                                all_file_paths.add(path)

            # Step 2: For each historical path, collect all commit hashes
            all_commit_hashes = set()
            commit_timestamps = {}  # Map commit hash to timestamp

            for path in all_file_paths:
                # Search only the default branch (main or master)
                # Use --follow here as well so commit enumeration matches name-status lookup.
                # Avoid --reverse with --follow because Git may truncate history around renames;
                # we sort by timestamp in Python instead.
                result = subprocess.run(
                    ['git', 'log', main_branch, '--follow', '--pretty=format:%H%n%at', '--', path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    i = 0
                    while i < len(lines):
                        if i + 1 < len(lines):
                            commit_hash = lines[i].strip()
                            timestamp = lines[i + 1].strip()
                            if commit_hash and timestamp:
                                all_commit_hashes.add(commit_hash)
                                if commit_hash not in commit_timestamps:
                                    commit_timestamps[commit_hash] = int(timestamp)
                            i += 2

            # Sort commit hashes by timestamp
            commit_hashes = sorted(all_commit_hashes, key=lambda h: commit_timestamps.get(h, 0))

            if not commit_hashes:
                print(f"    ⚠️  未找到任何 commit")
                return False

            # Step 2: Iterate over each commit and get full commit info (including diff)
            all_commits = []

            tracked_basenames = {os.path.basename(p) for p in all_file_paths}

            for commit_hash in commit_hashes:
                # First try to get the diff using the current file path
                show_result = subprocess.run(
                    ['git', 'show', '--format=fuller', '--patch', '--find-renames', commit_hash, '--', file_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if show_result.returncode == 0 and show_result.stdout.strip():
                    commit_info = show_result.stdout
                    all_commits.append(commit_info)
                else:
                    # If the file path fails, the file may have had a different path in that commit
                    # Get the full commit diff and filter the file-related portion
                    show_result_all = subprocess.run(
                        ['git', 'show', '--format=fuller', '--patch', '--find-renames', commit_hash],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )

                    if show_result_all.returncode == 0:
                        # Parse output and extract commit info plus file-related diff
                        lines = show_result_all.stdout.split('\n')
                        commit_header = []
                        file_diff_lines = []
                        in_file_diff = False
                        file_basename = os.path.basename(file_path)

                        # Extract commit header (hash, author, date, message)
                        for i, line in enumerate(lines):
                            if line.startswith('commit '):
                                commit_header.append(line)
                            elif line.startswith('Author:') or line.startswith('Commit:'):
                                commit_header.append(line)
                            elif line.startswith('Date:'):
                                commit_header.append(line)
                            elif line.startswith('diff --git'):
                                # Check whether this diff is related to our file
                                # by checking whether any tracked basename appears in the diff line
                                if any(basename in line for basename in tracked_basenames):
                                    in_file_diff = True
                                    file_diff_lines.append(line)
                                elif in_file_diff:
                                    # Already in file diff; stop at the next file's diff
                                    break
                            elif in_file_diff:
                                if line.startswith('diff --git'):
                                    # Stop at the next file's diff
                                    break
                                file_diff_lines.append(line)
                            elif not in_file_diff:
                                # Still in commit header; keep collecting (skip blank/indented message lines)
                                if line.strip() and not line.startswith('    '):
                                    commit_header.append(line)
                                elif line.strip() == '' and commit_header:
                                    # Blank line separator
                                    commit_header.append(line)

                        # If file-related diff was found, add it to the results
                        if file_diff_lines:
                            commit_info = '\n'.join(commit_header) + '\n' + '\n'.join(file_diff_lines)
                            all_commits.append(commit_info)

            # Step 3: Write all commit info to file in chronological order
            if all_commits:
                with open(output_path, 'w', encoding='utf-8') as f:
                    for commit_info in all_commits:
                        f.write(commit_info)
                        f.write('\n\n')

                # Check whether the generated file has content
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    return True
                else:
                    print(f"    ⚠️  生成的 diff 文件为空")
                    return False
            else:
                print(f"    ⚠️  未找到任何 commit diff")
                return False

        finally:
            # Restore the original directory
            os.chdir(original_dir)

    except subprocess.TimeoutExpired:
        print(f"    ⚠️  超时: {file_path}")
        # Clean up any incomplete file
        if os.path.exists(output_path):
            os.remove(output_path)
        return False
    except Exception as e:
        print(f"    ❌ 错误: {file_path} - {str(e)}")
        # Clean up any incomplete file
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
        return False


def main():
    # Script directory
    script_dir = Path(__file__).parent.absolute()
    repo_root = script_dir.parent

    # CSV file path
    csv_file = script_dir / 'rule_files_path.csv'

    # Check whether the CSV file exists
    if not csv_file.exists():
        print(f"❌ 错误: 找不到文件 {csv_file}")
        sys.exit(1)

    # Cloned repositories directory (at repo root)
    cloned_repos_dir = repo_root / 'cloned_repositories'

    if not cloned_repos_dir.exists():
        print(f"❌ 错误: 找不到目录 {cloned_repos_dir}")
        sys.exit(1)

    # Directory for diff output files
    diff_output_dir = script_dir / 'file_diffs'
    diff_output_dir.mkdir(exist_ok=True)

    print(f"📄 读取 CSV 文件: {csv_file}")
    print(f"📁 仓库目录: {cloned_repos_dir}")
    print(f"📁 Diff 输出目录: {diff_output_dir}\n")

    # Read all rows
    rows = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        print("❌ CSV 文件为空")
        sys.exit(1)

    header = rows[0]

    # Check column indices
    if len(header) < 5:
        print("❌ CSV 文件格式错误：缺少必要的列")
        sys.exit(1)

    # Statistics
    total_count = 0
    processed_count = 0
    success_count = 0
    skipped_count = 0

    # Process each row (skip header)
    for idx, row in enumerate(rows[1:], start=1):
        if len(row) < 5:
            continue

        project = row[0].strip()
        file_path = row[3].strip()  # Column 4 (index 3)
        commit_count_str = row[4].strip()  # Column 5 (index 4)

        # Skip empty or invalid rows
        if not project or not file_path:
            continue

        # Skip rows with empty file_path
        if not file_path or file_path == '':
            continue

        # Parse commit_count
        try:
            commit_count = int(commit_count_str) if commit_count_str else 0
        except ValueError:
            commit_count = 0

        # Process only files with commit_count > 1
        if commit_count <= 1:
            continue

        total_count += 1

        # Extract repository name
        repo_name = get_repo_name(project)
        repo_path = cloned_repos_dir / repo_name

        # Check whether the repository exists
        if not repo_path.exists():
            print(f"[{idx}/{len(rows)-1}] ⚠️  仓库不存在: {repo_name}")
            skipped_count += 1
            continue

        # Get diff filename
        diff_filename = get_diff_filename(file_path)

        # Output path: file_diffs/{repo_name}/{diff_filename}
        project_diff_dir = diff_output_dir / repo_name
        output_path = project_diff_dir / diff_filename

        print(f"[{idx}/{len(rows)-1}] 📝 处理: {repo_name}/{file_path}")
        print(f"    Commit 次数: {commit_count}")
        print(f"    输出文件: {output_path}")

        # Get diff
        if get_file_diff(str(repo_path), file_path, str(output_path)):
            success_count += 1
            file_size = os.path.getsize(output_path)
            print(f"    ✅ 成功生成 diff 文件 ({file_size} 字节)")
        else:
            skipped_count += 1

        processed_count += 1
        print()  # Blank line separator

    # Print summary statistics
    print("="*60)
    print("📊 处理统计:")
    print(f"   总计 (commit_count > 1): {total_count}")
    print(f"   已处理: {processed_count}")
    print(f"   成功生成: {success_count}")
    print(f"   跳过/失败: {skipped_count}")
    print("="*60)


if __name__ == '__main__':
    main()
