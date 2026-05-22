import requests
import os
import time
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple
import csv
from collections import defaultdict

class QoderRulesContributorsSurvey:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = "https://api.github.com"
        self.output_dir = os.path.dirname(os.path.abspath(__file__))
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Store results: repo_url -> contributors info
        self.results: Dict[str, List[Dict]] = defaultdict(list)

    def _check_rate_limit(self, response) -> bool:
        """Check GitHub API rate limit and wait if necessary."""
        rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
        rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', 0))
        
        if rate_limit_remaining <= 1:
            wait_time = max(rate_limit_reset - int(time.time()), 0) + 10
            print(f"\nRate limit reached. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            return True
        return False

    def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Make a request with rate limit handling."""
        max_retries = 3
        retry_delay = 5
        
        if params is None:
            params = {}
            
        for retry_count in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                if response.status_code == 403:
                    wait_time = max(int(response.headers.get('X-RateLimit-Reset', 0)) - int(time.time()), 0) + 10
                    print(f"Rate limit reached. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                
                response.raise_for_status()
                
                if not self._check_rate_limit(response):
                    return response.json()
                    
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    return None
                if retry_count < max_retries - 1:
                    print(f"HTTP error occurred (attempt {retry_count + 1}/{max_retries}): {e}")
                    time.sleep(retry_delay)
                else:
                    print(f"Max retries exceeded for {url}")
                    return None
            except requests.exceptions.RequestException as e:
                if retry_count < max_retries - 1:
                    print(f"Request error occurred (attempt {retry_count + 1}/{max_retries}): {e}")
                    time.sleep(retry_delay)
                else:
                    print(f"Max retries exceeded for {url}")
                    return None
        
        return None

    def _extract_repo_info(self, repo_url: str) -> Optional[Tuple[str, str]]:
        """Extract owner and repo name from GitHub URL."""
        if 'github.com' not in repo_url:
            return None
        
        parts = repo_url.strip('/').split('/')
        if len(parts) < 5:
            return None
        
        owner = parts[-2]
        repo = parts[-1]
        return owner, repo

    def _check_qoder_rules_folder(self, owner: str, repo: str) -> bool:
        """Check if repository contains .qoder/rules folder."""
        qoder_rules_folder_url = f"{self.base_url}/repos/{owner}/{repo}/contents/.qoder/rules"
        data = self._make_request(qoder_rules_folder_url)
        return data is not None

    def _get_repo_created_date(self, owner: str, repo: str) -> Optional[str]:
        """Get repository creation date."""
        repo_url = f"{self.base_url}/repos/{owner}/{repo}"
        data = self._make_request(repo_url)
        if data:
            return data.get('created_at', '')
        return None

    def _is_date_in_range(self, date_input, start_date: str, end_date: str) -> bool:
        """Check if date is within the specified range.
        date_input can be a datetime object or a date string."""
        if not date_input:
            return False
        try:
            # Handle both datetime objects and strings
            if isinstance(date_input, datetime):
                date_obj = date_input
            else:
                # Parse date string (format: 2025-10-01T00:00:00Z)
                date_obj = datetime.strptime(date_input.split('T')[0], '%Y-%m-%d')
            
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            return start <= date_obj <= end
        except:
            return False

    def _get_file_commits(self, owner: str, repo: str, file_path: str) -> List[Dict]:
        """Get commit history for a specific file or folder."""
        commits_url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        params = {'path': file_path, 'per_page': 100}
        
        all_commits = []
        page = 1
        
        while True:
            params['page'] = page
            data = self._make_request(commits_url, params)
            
            if not data or not isinstance(data, list):
                break
            
            if len(data) == 0:
                break
            
            all_commits.extend(data)
            
            # Check if there are more pages
            if len(data) < 100:
                break
            
            page += 1
            time.sleep(0.5)  # Rate limiting
        
        return all_commits

    def _is_valid_email(self, email: str) -> bool:
        """Check if email is a valid (non-placeholder) email."""
        if not email or not isinstance(email, str):
            return False
        
        email = email.strip().lower()
        
        # Basic format check: must contain @
        if '@' not in email:
            return False
        
        # Filter placeholder domains
        placeholder_domains = [
            'example.com',
            'example.org',
            'example.net',
            'localhost',
            'test.local',
            'local'
        ]
        
        # Check domain part
        domain = email.split('@')[-1]
        
        # Filter GitHub noreply emails
        if domain == 'users.noreply.github.com':
            return False
        
        # Check if domain is a placeholder
        if domain in placeholder_domains:
            return False
        
        # Check if ends with .local (local email)
        if domain.endswith('.local'):
            return False
        
        # Check if subdomain is related to example
        if 'example' in domain:
            return False
        
        # Filter common placeholder username patterns (but allow real noreply emails)
        placeholder_usernames = [
            'user',
            'test',
            'example',
        ]
        
        username = email.split('@')[0]
        
        # Filter if both username and domain are placeholders
        if username in placeholder_usernames:
            # Filter if domain contains example or localhost
            if any(placeholder in domain for placeholder in ['example', 'localhost', 'local']):
                return False
        
        return True

    def _extract_contributors_from_commits(self, commits: List[Dict]) -> Set[Tuple[str, str, str]]:
        """Extract unique contributors (name, email, login) from commits."""
        contributors = set()
        
        for commit in commits:
            author = commit.get('author')
            commit_info = commit.get('commit', {})
            commit_author = commit_info.get('author', {})
            
            # Get email from commit author (most reliable)
            email = commit_author.get('email', '')
            name = commit_author.get('name', '')
            login = author.get('login', '') if author else ''
            
            # Only add valid emails
            if email and self._is_valid_email(email):
                contributors.add((name, email, login))
        
        return contributors

    def search_repositories(self, start_date: str = "2025-10-01", end_date: str = "2026-01-10"):
        """Search repositories with .qoder/rules folder in the specified date range."""
        print(f"Searching for repositories containing .qoder/rules folder")
        print(f"Date range: {start_date} to {end_date}")
        print("=" * 60)
        
        # Step 0: Get total count of matching repositories (first page only, for total_count)
        url = f"{self.base_url}/search/code"
        query = 'path:.qoder/rules'
        params = {
            'q': query,
            'per_page': 1  # Only need total count, not actual data
        }
        
        print("\nStep 0: Fetching total count of matching repositories...")
        data = self._make_request(url, params)
        
        if not data or 'total_count' not in data:
            print("  Warning: Unable to get total count")
            total_code_results = 0
        else:
            total_code_results = data.get('total_count', 0)
            print(f"  Total results from code search API: {total_code_results}")
            if total_code_results > 1000:
                print("  Note: GitHub API limits results to 1000 maximum")
        
        if total_code_results == 0:
            print("  No matching repositories found")
            return []
        
        # Step 1: Fetch all code results containing .qoder/rules (up to 1000)
        print("\nStep 1: Fetching all code results containing .qoder/rules...")
        params = {
            'q': query,
            'per_page': 100
        }
        
        all_code_items = []  # Store all code search results
        page = 1
        max_pages = 10  # GitHub code search API returns at most 1000 results
        
        while page <= max_pages:
            params['page'] = page
            data = self._make_request(url, params)
            
            if not data or 'items' not in data:
                break
            
            items = data.get('items', [])
            if not items:
                break
            
            print(f"  Processing page {page}, found {len(items)} code results...")
            all_code_items.extend(items)
            
            if len(items) < 100:
                break
            
            page += 1
            time.sleep(1)  # Rate limiting
        
        print(f"  Retrieved {len(all_code_items)} code results in total")
        
        # Step 2: Check commit dates for each code file and filter repositories within the date range
        print(f"\nStep 2: Checking commit dates for each code file...")
        valid_repos = []
        checked_repos = set()  # Avoid re-checking the same repository
        
        for idx, item in enumerate(all_code_items, 1):
            if idx % 50 == 0:
                print(f"  Processed {idx}/{len(all_code_items)} code results, found {len(valid_repos)} matching repositories...")
            
            repo_url = item['repository']['html_url']
            if repo_url in checked_repos:
                continue
            
            repo_info = self._extract_repo_info(repo_url)
            if not repo_info:
                continue
            
            owner, repo = repo_info
            
            # Get commit history for .qoder/rules
            commits = self._get_file_commits(owner, repo, '.qoder/rules')
            if not commits:
                checked_repos.add(repo_url)
                time.sleep(0.2)
                continue
            
            # Check if there are commits within the date range
            has_valid_commit = False
            for commit in commits:
                commit_date_str = commit.get('commit', {}).get('author', {}).get('date', '')
                if not commit_date_str:
                    continue
                
                try:
                    commit_date = datetime.strptime(commit_date_str.split('T')[0], '%Y-%m-%d')
                    # Check if within date range
                    if self._is_date_in_range(commit_date, start_date, end_date):
                        has_valid_commit = True
                        break
                except:
                    continue
            
            if has_valid_commit:
                valid_repos.append(repo_url)
            
            checked_repos.add(repo_url)
            time.sleep(0.3)  # Rate limiting
        
        print(f"\nStep 3: Verifying each repository contains .qoder/rules folder...")
        # Step 3: Verify each repository contains .qoder/rules folder
        final_valid_repos = []
        for idx, repo_url in enumerate(valid_repos, 1):
            if idx % 10 == 0:
                print(f"  Processed {idx}/{len(valid_repos)} repositories, found {len(final_valid_repos)} matching...")
            
            repo_info = self._extract_repo_info(repo_url)
            if not repo_info:
                continue
            
            owner, repo = repo_info
            
            # Check if repository contains .qoder/rules folder
            if self._check_qoder_rules_folder(owner, repo):
                final_valid_repos.append(repo_url)
                print(f"  ✓ [{len(final_valid_repos)}] {repo_url}")
            
            time.sleep(0.3)  # Rate limiting
        
        print(f"\nVerification complete: found {len(final_valid_repos)} matching repositories")
        return final_valid_repos

    def process_repositories(self, repo_urls: List[str]):
        """Process repositories: extract contributors from .qoder/rules folder."""
        print(f"\nProcessing {len(repo_urls)} repositories...")
        
        for idx, repo_url in enumerate(repo_urls, 1):
            print(f"\n[{idx}/{len(repo_urls)}] Processing: {repo_url}")
            
            # Extract owner and repo
            repo_info = self._extract_repo_info(repo_url)
            if not repo_info:
                print(f"  Skipped: Invalid URL format")
                continue
            
            owner, repo = repo_info
            
            # Confirm repository contains .qoder/rules folder
            if not self._check_qoder_rules_folder(owner, repo):
                print(f"  Skipped: No .qoder/rules folder found")
                continue
            
            print(f"  Found .qoder/rules folder, fetching commit history...")
            
            # Get commit history for the .qoder/rules folder
            commits = self._get_file_commits(owner, repo, ".qoder/rules")
            if not commits:
                print(f"  Warning: No commits found for .qoder/rules")
                continue
            
            print(f"  Found {len(commits)} commits")
            
            # Extract contributors
            contributors = self._extract_contributors_from_commits(commits)
            print(f"  Found {len(contributors)} unique contributors")
            
            # Get additional repo info
            repo_data = self._make_request(f"{self.base_url}/repos/{owner}/{repo}")
            repo_name = f"{owner}/{repo}"
            repo_description = repo_data.get('description', '') if repo_data else ''
            repo_stars = repo_data.get('stargazers_count', 0) if repo_data else 0
            repo_created = repo_data.get('created_at', '') if repo_data else ''
            
            # Store results
            for name, email, login in contributors:
                self.results[repo_url].append({
                    'repo_name': repo_name,
                    'repo_url': repo_url,
                    'repo_description': repo_description,
                    'repo_stars': repo_stars,
                    'repo_created': repo_created,
                    'qoder_file_path': '.qoder/rules',
                    'contributor_name': name,
                    'contributor_email': email,
                    'contributor_login': login,
                    'total_commits': len(commits)
                })
            
            time.sleep(1)  # Rate limiting

    def save_to_csv(self, filename: str = None):
        """Save results to CSV file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.output_dir, f'qoder_rules_contributors_{timestamp}.csv')
        
        # Flatten results
        rows = []
        for repo_url, contributors in self.results.items():
            for contrib in contributors:
                rows.append(contrib)
        
        if not rows:
            print("\nNo results to save.")
            return
        
        # Write to CSV
        fieldnames = [
            'repo_name', 'repo_url', 'repo_description', 'repo_stars', 
            'repo_created', 'qoder_file_path', 'contributor_name', 
            'contributor_email', 'contributor_login', 'total_commits'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"\nResults saved to: {filename}")
        print(f"Total repositories: {len(self.results)}")
        print(f"Total contributor entries: {len(rows)}")
        print(f"Unique contributors: {len(set(row['contributor_email'] for row in rows))}")

def main():
    # Get GitHub token from environment variable
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN environment variable is not set")
        print("Please set your GitHub token as an environment variable:")
        print("export GITHUB_TOKEN='your_token_here'")
        return
    
    # Initialize survey
    survey = QoderRulesContributorsSurvey(token)
    
    # Search repositories from 2025-10-01 to 2026-01-10
    start_date = "2025-10-01"
    end_date = "2026-01-10"
    
    print("=" * 60)
    print("Qoder Rules Contributors Survey")
    print("=" * 60)
    print(f"Date range: {start_date} to {end_date}")
    print("Criteria: Repository must contain .qoder/rules folder")
    print("=" * 60)
    
    # Search repositories
    repo_urls = survey.search_repositories(start_date, end_date)
    
    if not repo_urls:
        print("\nNo repositories found matching the criteria.")
        return
    
    # Process repositories
    survey.process_repositories(repo_urls)
    
    # Save results
    survey.save_to_csv()

if __name__ == "__main__":
    main()

