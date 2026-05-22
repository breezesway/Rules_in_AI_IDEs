import pandas as pd
import os
import glob
import csv
import requests
from tqdm import tqdm
import time

def get_github_stats(repo_url, github_token=None):
    """
    Get repository statistics from GitHub API
    """
    # Convert GitHub URL to API URL
    if 'github.com' not in repo_url:
        return None
    
    # Extract owner and repo name from URL
    parts = repo_url.strip('/').split('/')
    if len(parts) < 5:
        return None
    
    owner = parts[-2]
    repo = parts[-1]
    
    # Prepare headers with token if provided
    headers = {}
    if github_token:
        headers['Authorization'] = f'token {github_token}'
    
    try:
        # Get basic repo info
        repo_url = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.get(repo_url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching {repo_url}: {response.status_code}")
            if response.status_code == 403:
                print("Rate limit exceeded. Please provide a GitHub token to increase the limit.")
            if response.status_code == 409:
                print(f"Repository {repo_url} is empty or in conflict (Status 409)")
            return None, response.status_code
        
        repo_data = response.json()
        stars = repo_data.get('stargazers_count', 0)
        
        # Get commit count
        commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=1"
        response = requests.get(commits_url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching commits for {repo_url}: {response.status_code}")
            return None, response.status_code
        
        # Get total commit count from the Link header
        commit_count = 0
        if 'Link' in response.headers:
            links = response.headers['Link'].split(',')
            for link in links:
                if 'rel="last"' in link:
                    # Extract the page number from the URL
                    try:
                        last_page_url = link.split(';')[0].strip('<>')
                        last_page = int(last_page_url.split('page=')[2].split('&')[0])
                        commit_count = last_page
                    except (IndexError, ValueError):
                        print(f"Warning: Could not parse commit count from {link}")
                        commit_count = 0
        
        return {
            'stars': stars,
            'commit_count': commit_count
        }, response.status_code
    except Exception as e:
        print(f"Error processing {repo_url}: {str(e)}")
        return None, None

def check_windsurf_files(repo_url, github_token=None):
    """
    Check if repository contains .windsurfrules file or .windsurf folder
    """
    # Convert GitHub URL to API URL
    if 'github.com' not in repo_url:
        return False
    
    # Extract owner and repo name from URL
    parts = repo_url.strip('/').split('/')
    if len(parts) < 5:
        return False
    
    owner = parts[-2]
    repo = parts[-1]
    
    # Prepare headers with token if provided
    headers = {}
    if github_token:
        headers['Authorization'] = f'token {github_token}'
    
    try:
        # Check for .windsurfrules file
        windsurfrules_url = f"https://api.github.com/repos/{owner}/{repo}/contents/.windsurfrules"
        response = requests.get(windsurfrules_url, headers=headers)
        has_windsurfrules = response.status_code == 200
        
        # Check for .windsurf folder
        windsurf_folder_url = f"https://api.github.com/repos/{owner}/{repo}/contents/.windsurf"
        response = requests.get(windsurf_folder_url, headers=headers)
        has_windsurf_folder = response.status_code == 200
        
        return has_windsurfrules or has_windsurf_folder
        
    except Exception as e:
        print(f"Error checking Windsurf files for {repo_url}: {str(e)}")
        return False

def analyze_repo_stats(df):
    """
    Analyze repository statistics and print distributions
    """
    print("\nRepository Statistics Analysis:")
    print("=" * 50)
    
    # Stars distribution
    if 'stars' in df.columns:
        print("\nStars Distribution:")
        print(df['stars'].describe())
        print("\nStars Range Counts:")
        bins = [0, 10, 100, 1000, 10000, float('inf')]
        labels = ['0-10', '11-100', '101-1000', '1001-10000', '10000+']
        print(pd.cut(df['stars'], bins=bins, labels=labels).value_counts().sort_index())
    
    # Commit count distribution
    if 'commit_count' in df.columns:
        print("\nCommit Count Distribution:")
        print(df['commit_count'].describe())
        print("\nCommit Count Range Counts:")
        bins = [0, 10, 100, 1000, 10000, float('inf')]
        labels = ['0-10', '11-100', '101-1000', '1001-10000', '10000+']
        print(pd.cut(df['commit_count'], bins=bins, labels=labels).value_counts().sort_index())

def filter_csv_by_keywords():
    # Define the keywords to match
    keywords = [
        "Windsurf IDE", "Windsurf AI", 
        "using Windsurf", "Windsurf Agent", "use Windsurf", "with Windsurf", "by Windsurf", "in Windsurf", "through Windsurf", "via Windsurf",
        "claude", "sonnet 3.7", "deepseek", 
        "制作", "实现", "编写", "生成", "创建", "开发", 
        "built", "build", 
        "基于Windsurf", "通过Windsurf", "借助Windsurf", "用windsurf", "由windsurf"
    ]
    
    # Define the exclusion keywords
    exclusion_keywords = [
        "test", "demo", "learn", "practice", "practical", "rule", "rules", "mouse", "pagination", 
        "a Windsurf", "重置", "无限试用", "curse", "3D Windsurf", "your Windsurf", 
        "custom Windsurf", "教程", "Windsurf navigation", "navigation", "Windsurf move", "学习", 
        "资源", "会员", "付费", "订阅", "example", "教学", "课程", "指南", "练习", 
        "awesome", "示例", "movement", "keyboard", "custom", "position", "animat", "pointer", 
        "theme", "attempt", "moving", "move", "Paginate", "Trying", "try", "simple", "quick", 
        "oracle", "store procedure", "mysql", "sql server", "Windsurf library", "Drawing", "draw", 
        "prompt", "collection", "hand gesture", "canvas", "click", "Windsurf array", "SQL", 
        "experiment", "scrollbar", "Portfolio", "template", "course", "tutorial", "toy", "玩具", 
        "实验", "live cursor", "guideline", "quiz", "small", "exploring", "realtime", "real-time",
        "window", "测试", "first", "homework"
    ]
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Discover input file: the only .xlsx that starts with 'windsurf_all_repo'
    candidates = [
        os.path.join(script_dir, f)
        for f in os.listdir(script_dir)
        if f.startswith("windsurf_all_repo") and f.endswith(".xlsx")
    ]
    if len(candidates) != 1:
        print("Error: Expected exactly one input file starting with 'windsurf_all_repo' and ending with '.xlsx'.")
        print(f"Found {len(candidates)} candidates: {candidates}")
        print(f"Looking in directory: {script_dir}")
        return
    input_file = candidates[0]
    
    print(f"Processing file: {input_file}")
    
    # Read the Excel file
    df = pd.read_excel(input_file)
    
    # Check if the required columns exist
    if len(df.columns) < 2:
        print("Error: Excel file does not have enough columns!")
        return
    
    # Get the description column (third column)
    description_col = df.columns[2]
    
    # Create a function to check if any keyword exists in the description
    def contains_keyword(text):
        if pd.isna(text):
            return False
        return any(keyword.lower() in str(text).lower() for keyword in keywords)
    
    # Create a function to check if any exclusion keyword exists in the description
    def contains_exclusion_keyword(text):
        if pd.isna(text):
            return False
        return any(keyword.lower() in str(text).lower() for keyword in exclusion_keywords)
    
    # Filter the dataframe - first include records with keywords, then exclude records with exclusion keywords
    filtered_df = df[df[description_col].apply(contains_keyword)]
    filtered_df = filtered_df[~filtered_df[description_col].apply(contains_exclusion_keyword)]
    
    # Get GitHub token from environment variable
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("\nWarning: No GitHub token found. API requests will be limited.")
        print("To increase the rate limit, set the GITHUB_TOKEN environment variable.")
        print("You can create a token at: https://github.com/settings/tokens")
    
    # Get GitHub statistics for each repository
    print("\nFetching GitHub statistics and checking Windsurf files for repositories...")
    stats_data = []
    status_codes = []  # 用于存储每个仓库的状态码
    windsurf_files_data = []  # 用于存储Windsurf文件检查结果
    valid_indices = []  # 用于存储有效的索引
    
    for idx, url in enumerate(tqdm(filtered_df['url'])):
        # Check for Windsurf files first
        has_windsurf_files = check_windsurf_files(url, github_token)
        windsurf_files_data.append(has_windsurf_files)
        
        # Only process repositories that have Windsurf files
        if has_windsurf_files:
            valid_indices.append(idx)
            stats, status_code = get_github_stats(url, github_token)
            if stats:
                stats_data.append(stats)
            else:
                stats_data.append({'stars': None, 'commit_count': None})  # 添加空数据
            status_codes.append(status_code)  # 记录状态码
        else:
            # Skip repositories without Windsurf files
            print(f"\nSkipping {url} - no .windsurfrules file or .windsurf folder found")
        
        time.sleep(1)  # Rate limiting
    
    # Filter the dataframe to only include repositories with Windsurf files
    filtered_df = filtered_df.iloc[valid_indices].reset_index(drop=True)
    
    # 添加状态码列
    filtered_df['status_code'] = status_codes
    filtered_df['has_windsurf_files'] = [windsurf_files_data[i] for i in valid_indices]
    
    # Add statistics to the dataframe
    if stats_data:
        stats_df = pd.DataFrame(stats_data)
        # 检查行数是否匹配
        if len(stats_df) != len(filtered_df):
            print(f"\nError: Number of rows mismatch!")
            print(f"Filtered DataFrame rows: {len(filtered_df)}")
            print(f"Stats DataFrame rows: {len(stats_df)}")
            print("Please check the data consistency.")
            return
        filtered_df = pd.concat([filtered_df.reset_index(drop=True), stats_df], axis=1)
    
    # Apply additional filter: remove repos with commit_count < 10 and stars == 0
    if 'commit_count' in filtered_df.columns and 'stars' in filtered_df.columns:
        before_count = len(filtered_df)
        mask_low_commit_zero_star = ~(
            filtered_df['commit_count'].notna() & (filtered_df['commit_count'] < 10) &
            filtered_df['stars'].notna() & (filtered_df['stars'] == 0)
        )
        filtered_df = filtered_df[mask_low_commit_zero_star].reset_index(drop=True)
        after_count = len(filtered_df)
        print(f"\nFiltered out {before_count - after_count} repositories with commits < 10 and stars == 0")
    
    # Analyze and print statistics
    analyze_repo_stats(filtered_df)
    
    # Generate output filename
    output_file = os.path.join(script_dir, f"filtered_{os.path.basename(input_file)}")
    
    # Save the filtered results
    filtered_df.to_excel(output_file, index=False)
    print(f"\nFiltered results saved to: {output_file}")
    print(f"Original records: {len(df)}")
    print(f"After keyword filtering: {len(df[df[description_col].apply(contains_keyword)])}")
    print(f"After exclusion keyword filtering: {len(df[df[description_col].apply(contains_keyword)][~df[df[description_col].apply(contains_keyword)][description_col].apply(contains_exclusion_keyword)])}")
    print(f"After Windsurf files filtering: {len(filtered_df)}")

if __name__ == "__main__":
    filter_csv_by_keywords()
