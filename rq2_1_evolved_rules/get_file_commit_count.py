"""
Script: Read rule_files_path.csv, get the commit count for each file, and write it to a CSV file.
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


def get_file_commit_count(repo_path, file_path):
    """
    Get the number of commits for a file in a Git repository.

    Args:
        repo_path: Root directory path of the repository
        file_path: Relative path of the file in the repository

    Returns:
        int: Commit count, or 0 on error
    """
    try:
        # Build the full file path
        full_file_path = os.path.join(repo_path, file_path)

        # Check whether the file exists
        if not os.path.exists(full_file_path):
            return 0

        # Switch to the repository directory
        original_dir = os.getcwd()
        os.chdir(repo_path)

        try:
            # Detect the default branch name
            main_branch = get_main_branch(repo_path)

            # Use git log --follow to track file renames
            # Search only the default branch (main or master)
            # --oneline prints one line per commit for easy counting
            # -- specifies the file path
            result = subprocess.run(
                ['git', 'log', main_branch, '--follow', '--oneline', '--', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                # Count non-empty lines (i.e. commits)
                commits = [line for line in result.stdout.strip().split('\n') if line.strip()]
                return len(commits)
            else:
                # If git log fails, the file may not be in Git history
                return 0

        finally:
            # Restore the original directory
            os.chdir(original_dir)

    except subprocess.TimeoutExpired:
        print(f"    ⚠️  超时: {file_path}")
        return 0
    except Exception as e:
        print(f"    ❌ 错误: {file_path} - {str(e)}")
        return 0


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

    print(f"📄 读取 CSV 文件: {csv_file}")
    print(f"📁 仓库目录: {cloned_repos_dir}\n")

    # Read all rows
    rows = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        print("❌ CSV 文件为空")
        sys.exit(1)

    # Check whether the commit_count column already exists
    header = rows[0]
    has_commit_count = len(header) > 4 and header[-1].strip().lower() == 'commit_count'

    # If commit_count is missing, add it
    if not has_commit_count:
        header.append('commit_count')
        # Add empty values for all data rows
        for i in range(1, len(rows)):
            if len(rows[i]) < len(header):
                rows[i].extend([''] * (len(header) - len(rows[i])))

    # Index of the commit_count column
    commit_count_idx = len(header) - 1

    # Statistics
    total_count = 0
    processed_count = 0
    success_count = 0
    skipped_count = 0

    # Process each row (skip header)
    for idx, row in enumerate(rows[1:], start=1):
        if len(row) < 4:
            continue

        project = row[0].strip()
        file_path = row[3].strip()  # Column 4 (index 3)

        # Skip empty or invalid rows
        if not project or not file_path:
            continue

        total_count += 1

        # Extract repository name
        repo_name = get_repo_name(project)
        repo_path = cloned_repos_dir / repo_name

        # Check whether the repository exists
        if not repo_path.exists():
            print(f"[{idx}/{len(rows)-1}] ⚠️  仓库不存在: {repo_name}")
            commit_count = 0
            skipped_count += 1
        else:
            print(f"[{idx}/{len(rows)-1}] 📝 处理: {repo_name}/{file_path}")
            commit_count = get_file_commit_count(str(repo_path), file_path)
            if commit_count > 0:
                success_count += 1
                print(f"    ✅ Commit 次数: {commit_count}")
            else:
                print(f"    ⚠️  Commit 次数: 0 (可能文件不在 Git 历史中)")

        # Update commit_count for this row
        # Ensure the row is long enough
        while len(row) <= commit_count_idx:
            row.append('')
        row[commit_count_idx] = str(commit_count)

        # Write CSV incrementally
        try:
            with open(csv_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            processed_count += 1
        except Exception as e:
            print(f"    ❌ 写入失败: {str(e)}")
            # Continue processing even if write fails
            continue

        print()  # Blank line separator

    # Print summary statistics
    print("="*60)
    print("📊 处理统计:")
    print(f"   总计: {total_count}")
    print(f"   已处理: {processed_count}")
    print(f"   成功获取: {success_count}")
    print(f"   跳过/失败: {skipped_count}")
    print("="*60)


if __name__ == '__main__':
    main()
