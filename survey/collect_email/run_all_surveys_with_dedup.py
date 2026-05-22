import os
import csv
import glob
from datetime import datetime
from typing import Dict, List, Set

# Import survey classes from all 5 contributor scripts
from cursor_rules_contributors_survey import CursorRulesContributorsSurvey
from windsurf_rules_contributors_survey import WindsurfRulesContributorsSurvey
from kiro_steering_contributors_survey import KiroSteeringContributorsSurvey
from qoder_rules_contributors_survey import QoderRulesContributorsSurvey
from trae_rules_contributors_survey import TraeRulesContributorsSurvey


def load_existing_contributors(csv_file_path: str) -> Set[tuple]:
    """
    Load existing contributor records from CSV files.
    Returns a set of (contributor_name, contributor_email) tuples.
    """
    existing_contributors = set()
    
    if not os.path.exists(csv_file_path):
        return existing_contributors
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get('contributor_name', '').strip()
                email = row.get('contributor_email', '').strip()
                # Add to set if name or email exists
                if name or email:
                    existing_contributors.add((name, email))
    except Exception as e:
        print(f"  Warning: error reading file {csv_file_path}: {e}")
    
    return existing_contributors


def find_existing_csv_files(output_dir: str, prefix: str) -> List[str]:
    """
    Find all CSV files with the given prefix.
    
    Args:
        output_dir: Output directory
        prefix: CSV filename prefix (e.g. 'windsurf', 'cursor')
    
    Returns:
        List of matching CSV file paths
    """
    pattern = os.path.join(output_dir, f'{prefix}_*.csv')
    csv_files = glob.glob(pattern)
    return csv_files


def deduplicate_results(new_rows: List[Dict], existing_csv_files: List[str]) -> List[Dict]:
    """
    Deduplicate new results against contributors already in existing CSV files.
    Matches on contributor_name or contributor_email: if either field matches
    an existing record, the row is treated as a duplicate.
    
    Args:
        new_rows: List of new result rows
        existing_csv_files: List of existing CSV file paths
    
    Returns:
        Deduplicated result rows
    """
    # Collect existing contributor names and emails
    existing_names = set()
    existing_emails = set()
    
    for csv_file in existing_csv_files:
        print(f"  Reading existing file: {os.path.basename(csv_file)}")
        existing = load_existing_contributors(csv_file)
        for name, email in existing:
            if name:
                existing_names.add(name.lower().strip())
            if email:
                existing_emails.add(email.lower().strip())
        print(f"    Loaded {len(existing)} contributor records from this file")
    
    print(f"  Loaded {len(existing_names)} unique names and {len(existing_emails)} unique emails in total")
    
    # Filter new results
    deduplicated_rows = []
    skipped_count = 0
    
    for row in new_rows:
        name = row.get('contributor_name', '').strip()
        email = row.get('contributor_email', '').strip()
        
        # Treat as duplicate if name or email matches an existing record
        is_duplicate = False
        
        if name:
            name_lower = name.lower()
            if name_lower in existing_names:
                is_duplicate = True
        
        if not is_duplicate and email:
            email_lower = email.lower()
            if email_lower in existing_emails:
                is_duplicate = True
        
        if not is_duplicate:
            deduplicated_rows.append(row)
            # Track new records to avoid duplicates within the batch
            if name:
                existing_names.add(name.lower())
            if email:
                existing_emails.add(email.lower())
        else:
            skipped_count += 1
    
    print(f"  Deduplication: {len(new_rows)} original rows, {len(deduplicated_rows)} after dedup, skipped {skipped_count} duplicates")
    
    return deduplicated_rows


def run_survey_with_dedup(survey_class, survey_name: str, csv_prefix: str, 
                          start_date: str, end_date: str, output_dir: str):
    """
    Run a survey and deduplicate results.
    
    Args:
        survey_class: Survey class
        survey_name: Survey name (for display)
        csv_prefix: CSV filename prefix (e.g. 'windsurf', 'cursor')
        start_date: Start date
        end_date: End date
        output_dir: Output directory
    """
    print("\n" + "=" * 80)
    print(f"Starting: {survey_name}")
    print("=" * 80)
    
    # Get GitHub token
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print(f"Error: GITHUB_TOKEN environment variable is not set")
        print("Please set your GitHub token as an environment variable:")
        print("export GITHUB_TOKEN='your_token_here'")
        return
    
    # Initialize survey
    survey = survey_class(token)
    
    # Search repositories
    print(f"\nSearching repositories (date range: {start_date} to {end_date})...")
    repo_urls = survey.search_repositories(start_date, end_date)
    
    if not repo_urls:
        print(f"\nNo repositories found matching the criteria.")
        return
    
    # Process repositories
    survey.process_repositories(repo_urls)
    
    # Prepare to save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f'{csv_prefix}_rules_contributors_{timestamp}.csv')
    
    # Collect new results
    new_rows = []
    for repo_url, contributors in survey.results.items():
        for contrib in contributors:
            new_rows.append(contrib)
    
    if not new_rows:
        print(f"\nNo results to save.")
        return
    
    print(f"\nFound {len(new_rows)} new records")
    
    # Find existing CSV files
    print(f"\nLooking for existing {csv_prefix} CSV files...")
    existing_csv_files = find_existing_csv_files(output_dir, csv_prefix)
    
    if existing_csv_files:
        print(f"Found {len(existing_csv_files)} existing CSV files:")
        for csv_file in existing_csv_files:
            print(f"  - {os.path.basename(csv_file)}")
        
        # Deduplicate
        print(f"\nDeduplicating...")
        new_rows = deduplicate_results(new_rows, existing_csv_files)
    else:
        print(f"No existing {csv_prefix} CSV files found; skipping deduplication")
    
    if not new_rows:
        print(f"\nNo new records to save after deduplication.")
        return
    
    # Save results
    print(f"\nSaving results to: {filename}")
    
    # Get field names from first row keys
    if new_rows:
        fieldnames = list(new_rows[0].keys())
    else:
        # Use default field names if no rows (varies by survey class)
        if csv_prefix == 'cursor':
            fieldnames = ['repo_name', 'repo_url', 'repo_description', 'repo_stars', 
                         'repo_created', 'cursor_file_path', 'contributor_name', 
                         'contributor_email', 'contributor_login', 'total_commits']
        elif csv_prefix == 'windsurf':
            fieldnames = ['repo_name', 'repo_url', 'repo_description', 'repo_stars', 
                         'repo_created', 'windsurf_file_path', 'contributor_name', 
                         'contributor_email', 'contributor_login', 'total_commits']
        elif csv_prefix == 'kiro':
            fieldnames = ['repo_name', 'repo_url', 'repo_description', 'repo_stars', 
                         'repo_created', 'kiro_file_path', 'contributor_name', 
                         'contributor_email', 'contributor_login', 'total_commits']
        elif csv_prefix == 'qoder':
            fieldnames = ['repo_name', 'repo_url', 'repo_description', 'repo_stars', 
                         'repo_created', 'qoder_file_path', 'contributor_name', 
                         'contributor_email', 'contributor_login', 'total_commits']
        elif csv_prefix == 'trae':
            fieldnames = ['repo_name', 'repo_url', 'repo_description', 'repo_stars', 
                         'repo_created', 'trae_file_path', 'contributor_name', 
                         'contributor_email', 'contributor_login', 'total_commits']
        else:
            fieldnames = []
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_rows)
    
    print(f"\nResults saved to: {filename}")
    print(f"Total repositories: {len(survey.results)}")
    print(f"Total contributor entries: {len(new_rows)}")
    print(f"Unique contributors: {len(set(row['contributor_email'] for row in new_rows if row.get('contributor_email')))}")


def main():
    """Main entry point: run all 5 contributor survey scripts."""
    # Set date range
    start_date = "2025-06-01"
    end_date = "2025-09-30"
    
    # Get output directory
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 80)
    print("Running all IDE contributor surveys")
    print("=" * 80)
    print(f"Date range: {start_date} to {end_date}")
    print(f"Output directory: {output_dir}")
    print("=" * 80)
    
    # Survey configurations
    surveys = [
        (CursorRulesContributorsSurvey, "Cursor Rules Contributors Survey", "cursor"),
        (WindsurfRulesContributorsSurvey, "Windsurf Rules Contributors Survey", "windsurf"),
        (KiroSteeringContributorsSurvey, "Kiro Steering Contributors Survey", "kiro"),
        (QoderRulesContributorsSurvey, "Qoder Rules Contributors Survey", "qoder"),
        (TraeRulesContributorsSurvey, "Trae Rules Contributors Survey", "trae"),
    ]
    
    # Run each survey
    for survey_class, survey_name, csv_prefix in surveys:
        try:
            run_survey_with_dedup(
                survey_class=survey_class,
                survey_name=survey_name,
                csv_prefix=csv_prefix,
                start_date=start_date,
                end_date=end_date,
                output_dir=output_dir
            )
        except Exception as e:
            print(f"\nError while processing {survey_name}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print("\n" + "=" * 80)
    print("All surveys complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()

