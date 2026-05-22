"""
Analyze reasons for rule changes.
"""

import json
import re
import requests
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# ==================== Configuration ====================
# OpenRouter API settings
API_URL = "https://openrouter.ai/api/v1/responses"
API_KEY = "<your-api-key>"
MODELS = ["google/gemini-3-flash-preview", "z-ai/glm-5", "qwen/qwen3-max"]
# Debug mode: random sample size (set to None to process all rules)
DEBUG_SAMPLE_SIZE = None
# Thread pool size for concurrent processing
# Note: LLM calls are IO-bound; most time is spent waiting on network responses,
# so a larger thread count is usually acceptable.
# Suggested values:
#   - Conservative: 10-20 (strict API rate limits or unstable network)
#   - Moderate: 20-50 (stable API and network)
#   - Aggressive: 50-100 (requires high-concurrency API support; watch error rate)
# Lower this value if you see 429 (rate limit) or connection errors.
MAX_WORKERS = 30
# Some models fail more often under high concurrency on OpenRouter; lower workers here.
MAX_WORKERS_QWEN3_MAX = 2

# Retry wait time in seconds when a 429 rate-limit error occurs
# Suggested value: 30-60 seconds, depending on API limits
RATE_LIMIT_RETRY_WAIT_SECONDS = 60

# Output file templates (model name is inserted into the filename)
OUTPUT_RESULTS_FILE_TEMPLATE = "reason_results_{model_name}.json"  # Key result data (JSON)
FAILED_RULES_FILE_TEMPLATE = "failed_reason_rules_{model_name}.json"  # Failed rules
# =======================================================


def get_model_name_identifier(model: str) -> str:
    """Extract a filename-safe identifier from a model name."""
    if '/' in model:
        return model.split('/')[-1]
    return model.replace('/', '_').replace('\\', '_')


def max_workers_for_model(model: str) -> int:
    """Return thread-pool size for a model; defaults to MAX_WORKERS."""
    m = (model or "").strip()
    if m == "qwen/qwen3-max":
        return MAX_WORKERS_QWEN3_MAX
    return MAX_WORKERS


def get_unique_file_path(base_path: Path) -> Path:
    """Return a unique file path, appending _2, _3, etc. if the file already exists."""
    if not base_path.exists():
        return base_path

    stem = base_path.stem
    suffix = base_path.suffix
    parent = base_path.parent

    counter = 2
    while True:
        new_path = parent / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def load_system_prompt(prompt_file: Path) -> str:
    """Load the system prompt from a file."""
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error: unable to read system prompt file {prompt_file}: {e}")
        raise


def parse_commit_info(commit_info_file: Path) -> Dict[str, Dict[str, Any]]:
    """
    Parse commit_info.txt and return a commit_id -> commit info mapping.

    Returns:
        Dict[commit_id, {
            'commit_message': str,
            'co_changed_files': List[str]  # format: "change_type file_path added_lines deleted_lines"
        }]
    """
    commit_map = {}

    if not commit_info_file.exists():
        print(f"Warning: commit_info.txt not found: {commit_info_file}")
        return commit_map

    try:
        with open(commit_info_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split each commit block using the = separator
        # Format: ==========...==========\nCommit #X\n==========...==========\nCommit ID: ...
        commit_blocks = re.split(r'={80,}', content)

        for block in commit_blocks:
            block = block.strip()
            if not block:
                continue

            # Skip header lines like "Commit #X"
            if re.match(r'^Commit #\d+$', block.strip()):
                continue

            # Extract commit_id
            commit_id_match = re.search(r'Commit ID:\s*([a-f0-9]+)', block)
            if not commit_id_match:
                continue

            commit_id = commit_id_match.group(1)

            # Extract commit message (between "Commit Message:" and "Changed Files:")
            commit_message_match = re.search(r'Commit Message:\s*\n(.*?)(?=\nChanged Files:)', block, re.DOTALL)
            if commit_message_match:
                commit_message = commit_message_match.group(1).strip()
            else:
                commit_message = ""

            # Use fallback text when commit message is empty
            if not commit_message:
                commit_message = "No commit message provided"

            # Extract changed files (after "Changed Files:" until next separator or EOF)
            changed_files_match = re.search(r'Changed Files:\s*\n(.*?)(?=\n={80,}|$)', block, re.DOTALL)
            co_changed_files = []
            if changed_files_match:
                files_text = changed_files_match.group(1).strip()
                # One file per line
                for line in files_text.split('\n'):
                    line = line.strip()
                    if line:
                        co_changed_files.append(line)

            commit_map[commit_id] = {
                'commit_message': commit_message,
                'co_changed_files': co_changed_files
            }

        print(f"Parsed {len(commit_map)} commit record(s) successfully")
        return commit_map

    except Exception as e:
        print(f"Error: failed to parse commit_info.txt: {e}")
        return commit_map


def build_user_prompt(rule: Dict[str, Any], commit_info: Optional[Dict[str, Any]]) -> str:
    """Build the user prompt for a rule."""
    project_name = rule.get('project', '')
    rule_file_path = rule.get('file', '')
    change_type = rule.get('change_type', '')
    rule_content = rule.get('content', '')

    # Get commit message and co-changed files
    if commit_info:
        commit_message = commit_info.get('commit_message', 'No commit message provided')
        co_changed_files = commit_info.get('co_changed_files', [])
    else:
        commit_message = 'No commit message provided'
        co_changed_files = []

    # Format co-changed files
    if co_changed_files:
        co_changed_files_raw_list = '\n'.join(co_changed_files)
    else:
        co_changed_files_raw_list = 'No other files changed in this commit'

    user_prompt = f"""# Input Data for Analysis

## 1. Rule Info
*   **Project Name:** {project_name}
*   **Target Rule File:** {rule_file_path}
*   **Change Type:** {change_type}
*   **Rule Content (Diff):** 
{rule_content}

## 2. Commit Info
*   **Commit Message:** "{commit_message}"

## 3. Co-changed Files
*(Format: change_type file_path added_lines deleted_lines)*
{co_changed_files_raw_list}

# Task
Based on the inputs above, categorize the driver of this rule change."""

    return user_prompt


def call_openrouter_api(system_prompt: str, user_prompt: str, model: str) -> Optional[Dict[str, Any]]:
    """Call the OpenRouter API."""
    payload = {
        "input": [
            {
                "type": "message",
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": system_prompt,
                    },
                ]
            },
            {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": user_prompt,
                    },
                ]
            }
        ],
        "model": model,
        "reasoning": {
            "effort": "medium",
        },
        "response_format": {
            "type": "json_object",
        },
        "temperature": 1.0,
        "top_p": 0.95
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=60)

        if response.status_code != 200:
            error_data = response.json() if response.content else {}
            error_msg = error_data.get('error', {}).get('message', f'HTTP {response.status_code}')

            # On 429 (rate limit), wait and retry once
            if response.status_code == 429:
                print(f"API rate limit (429); waiting {RATE_LIMIT_RETRY_WAIT_SECONDS}s before retry...")
                time.sleep(RATE_LIMIT_RETRY_WAIT_SECONDS)

                # Retry request
                try:
                    retry_response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
                    if retry_response.status_code == 200:
                        return retry_response.json()
                    else:
                        # Still failing after retry; return None for next round
                        retry_error_data = retry_response.json() if retry_response.content else {}
                        retry_error_msg = retry_error_data.get('error', {}).get('message', f'HTTP {retry_response.status_code}')
                        print(f"API error (after retry): {retry_error_msg}")
                        return None
                except Exception as e:
                    print(f"Error during retry request: {e}")
                    return None
            else:
                # Other errors: return None for next round
                print(f"API error: {error_msg}")
                return None

        return response.json()

    except requests.Timeout:
        print("API request timed out")
        return None
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        return None
    except Exception as e:
        print(f"Unknown error: {e}")
        return None


def extract_output_text(response_data: Dict[str, Any]) -> Optional[str]:
    """Extract output text from an API response."""
    try:
        output = response_data.get('output', [])
        if not isinstance(output, list):
            print("Warning: output field is not an array")
            return None

        for item in output:
            if not isinstance(item, dict):
                continue

            if item.get('type') == 'message':
                content = item.get('content', [])
                if not isinstance(content, list):
                    continue

                for content_item in content:
                    if not isinstance(content_item, dict):
                        continue

                    if content_item.get('type') == 'output_text':
                        text = content_item.get('text', '')
                        if text:
                            return text

        print("Warning: no output text found")
        return None

    except Exception as e:
        print(f"Error while extracting output text: {e}")
        return None


def parse_output_json(output_text: str) -> Optional[Dict[str, Any]]:
    """Parse a JSON object from output text."""
    if not output_text:
        return None

    try:
        parsed = json.loads(output_text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    # Try extracting a JSON code block
    try:
        json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
        matches = re.findall(json_pattern, output_text, re.DOTALL)
        if matches:
            parsed = json.loads(matches[0])
            if isinstance(parsed, dict):
                return parsed
    except (json.JSONDecodeError, IndexError):
        pass

    # Try content between the first { and last }
    try:
        start = output_text.find('{')
        end = output_text.rfind('}')
        if start != -1 and end != -1 and end > start:
            json_str = output_text[start:end+1]
            parsed = json.loads(json_str)
            if isinstance(parsed, dict):
                return parsed
    except json.JSONDecodeError:
        pass

    print("Warning: unable to parse JSON from output text")
    return None


def process_rule(rule: Dict[str, Any], commit_map: Dict[str, Dict[str, Any]],
                 system_prompt: str, model: str, output_func=None, is_debug_mode=False) -> tuple[Optional[Dict[str, Any]], bool]:
    """
    Process a single rule.

    Args:
        rule: Rule object
        commit_map: commit_id -> commit info mapping
        system_prompt: System prompt
        model: Model name
        output_func: Output function; uses print when None
        is_debug_mode: Whether debug mode is enabled

    Returns:
        tuple: (result data, success flag)
    """
    if output_func is None:
        output_func = print

    rule_id = rule.get('id', 'unknown')
    commit_id = rule.get('commit_id', '')

    # Get commit info (all commit_ids should already be validated)
    commit_info = commit_map.get(commit_id)
    if not commit_info:
        # Should not happen because validation runs before processing starts
        raise ValueError(f"commit_id {commit_id} for rule {rule_id} not found in commit_info.txt")

    if commit_info.get('commit_message', '') == 'No commit message provided':
        print(f"[no commit message] rule_id={rule_id} commit_id={commit_id}")
        print(json.dumps(rule, ensure_ascii=False, indent=2))

    # Verbose output only in debug mode
    if is_debug_mode:
        output_func(f"Processing rule: {rule_id}")
        content = rule.get('content', '')
        output_func(f"Rule Content: {content}\n")

    # Build user prompt
    user_prompt = build_user_prompt(rule, commit_info)

    # Call API
    response_data = call_openrouter_api(system_prompt, user_prompt, model)

    if response_data is None:
        print(f"Rule {rule_id} API call failed")
        return None, False

    # Extract and parse output text
    output_text = extract_output_text(response_data)

    parsed_json = None
    if output_text:
        parsed_json = parse_output_json(output_text)

    # Build result payload
    result_data = {
        'rule_id': rule_id,
        'project': rule.get('project', ''),
        'file': rule.get('file', ''),
        'change_type': rule.get('change_type', ''),
        'rule_content': rule.get('content', ''),
        'commit_id': commit_id
    }

    if parsed_json:
        result_data.update(parsed_json)

    # Verbose output only in debug mode
    if is_debug_mode and output_text:
        output_func(f"\n{'='*80}")
        output_func(f"Rule ID: {rule_id}")
        output_func(f"{'='*80}")
        output_func(output_text)
        output_func(f"{'='*80}\n")
    elif not output_text and is_debug_mode:
        output_func(f"Warning: no output text found for rule {rule_id}")

    # Success requires both output text and parsed JSON
    success = bool(output_text and parsed_json)

    if output_text and not parsed_json:
        print(f"Warning: rule {rule_id} returned output text but JSON parsing failed; marking as failed")

    return result_data, success


def find_all_json_files(file_diffs_dir: Path) -> list:
    """Find all JSON files under file_diffs_dir."""
    json_files = list(file_diffs_dir.rglob('*.json'))
    print(f"Found {len(json_files)} JSON file(s)")
    return json_files


def process_all_rules():
    """Process all rules once for each configured model."""
    script_dir = Path(__file__).parent
    rq22_dir = script_dir.parent
    file_diffs_dir = rq22_dir.parent / "rq2_1_evolved_rules" / "file_diffs"
    system_prompt_file = script_dir / 'reason_taxonomy_system_prompt.txt'
    commit_info_file = rq22_dir / 'commit_info.txt'

    for model in MODELS:
        model_name = get_model_name_identifier(model)
        print("\n" + "="*80)
        print(f"Processing model: {model}")
        print("="*80)

        base_failed_rules_file = script_dir / FAILED_RULES_FILE_TEMPLATE.format(model_name=model_name)
        failed_rules_file = get_unique_file_path(base_failed_rules_file)

        if failed_rules_file != base_failed_rules_file:
            print(f"Note: {base_failed_rules_file.name} already exists; using {failed_rules_file.name}")

        process_rules_for_model(
            model, script_dir, file_diffs_dir, system_prompt_file,
            commit_info_file, failed_rules_file,
        )


def process_rules_for_model(model: str, script_dir: Path, file_diffs_dir: Path,
                           system_prompt_file: Path, commit_info_file: Path,
                           failed_rules_file: Path):
    """Process all rules for a single model."""

    if not file_diffs_dir.exists():
        print(f"Error: directory not found: {file_diffs_dir}")
        return

    if not system_prompt_file.exists():
        print(f"Error: system prompt file not found: {system_prompt_file}")
        return

    if not commit_info_file.exists():
        print(f"Error: commit_info.txt not found: {commit_info_file}")
        return

    print("Loading system prompt...")
    system_prompt = load_system_prompt(system_prompt_file)

    print("Parsing commit info...")
    commit_map = parse_commit_info(commit_info_file)

    json_files = find_all_json_files(file_diffs_dir)

    all_valid_rules: List[Dict[str, Any]] = []

    print("Collecting all rules...")
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                continue

            for rule in data:
                if not isinstance(rule, dict):
                    continue

                if all(key in rule for key in ['id', 'change_type', 'content', 'commit_id']):
                    all_valid_rules.append(rule)

        except json.JSONDecodeError as e:
            print(f"Warning: unable to parse JSON file {json_file}: {e}")
            continue
        except Exception as e:
            print(f"Warning: error processing file {json_file}: {e}")
            continue

    print(f"Collected {len(all_valid_rules)} valid rule(s)")

    print("Checking that all commit_id values exist...")
    missing_commit_ids = []
    for rule in all_valid_rules:
        commit_id = rule.get('commit_id', '')
        if commit_id and commit_id not in commit_map:
            rule_id = rule.get('id', 'unknown')
            missing_commit_ids.append((rule_id, commit_id))

    if missing_commit_ids:
        print(f"\nError: {len(missing_commit_ids)} rule(s) have commit_id values missing from commit_info.txt:")
        for rule_id, commit_id in missing_commit_ids[:10]:
            print(f"  rule {rule_id}: commit_id {commit_id}")
        if len(missing_commit_ids) > 10:
            print(f"  ... and {len(missing_commit_ids) - 10} more")
        print("\nStopping. Please verify that commit_info.txt is complete.")
        raise ValueError(f"{len(missing_commit_ids)} rule(s) have commit_id values missing from commit_info.txt")

    print("✓ All commit_id values found")

    if DEBUG_SAMPLE_SIZE is not None and len(all_valid_rules) > DEBUG_SAMPLE_SIZE:
        import random
        print(f"Debug mode: randomly sampling {DEBUG_SAMPLE_SIZE} rule(s)")
        rules_to_process = random.sample(all_valid_rules, DEBUG_SAMPLE_SIZE)
    else:
        print("Processing all rules")
        rules_to_process = all_valid_rules

    total_rules = len(rules_to_process)
    is_debug_mode = DEBUG_SAMPLE_SIZE is not None

    def output_func(text):
        if is_debug_mode:
            print(text)

    pending_rules = rules_to_process.copy()

    model_name = get_model_name_identifier(model)
    base_output_results_file = script_dir / OUTPUT_RESULTS_FILE_TEMPLATE.format(model_name=model_name)
    output_results_file = get_unique_file_path(base_output_results_file)

    if output_results_file != base_output_results_file:
        print(f"Note: {base_output_results_file.name} already exists; using {output_results_file.name}")

    max_retries = 10

    # Initialize results file as an empty array before the first round
    try:
        with open(output_results_file, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: failed to initialize results file: {e}")

    num_workers = max_workers_for_model(model)

    print(f"\nStarting first pass with {len(pending_rules)} rule(s)...")
    print(f"Using {num_workers} worker thread(s)\n")

    for round_num in range(1, max_retries + 1):
        if not pending_rules:
            print(f"\nAll rules processed; no retry needed for round {round_num}")
            break

        if round_num > 1:
            print(f"\nStarting retry round {round_num}; {len(pending_rules)} failed rule(s) remaining...")

        round_successful_results: List[Dict[str, Any]] = []
        round_failed_rules: List[Dict[str, Any]] = []
        results_lock = Lock()

        def process_rule_wrapper(rule: Dict[str, Any]) -> tuple[Dict[str, Any], Optional[Dict[str, Any]], bool]:
            """Wrapper for processing a single rule in the thread pool."""
            try:
                result_data, success = process_rule(
                    rule, commit_map, system_prompt, model, output_func, is_debug_mode,
                )
                return rule, result_data, success
            except Exception as e:
                rule_id = rule.get('id', 'unknown')
                print(f"Error: exception while processing rule {rule_id}: {e}")
                return rule, None, False

        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            future_to_rule = {executor.submit(process_rule_wrapper, rule): rule for rule in pending_rules}

            desc = f"Round {round_num}" if round_num > 1 else "First pass"
            with tqdm(total=len(pending_rules), desc=desc, unit="rule") as pbar:
                for future in as_completed(future_to_rule):
                    rule, result_data, success = future.result()

                    with results_lock:
                        if success and result_data is not None:
                            round_successful_results.append(result_data)
                        else:
                            round_failed_rules.append(rule)

                    pbar.update(1)

        if round_successful_results:
            existing_results = []
            if output_results_file.exists():
                try:
                    with open(output_results_file, 'r', encoding='utf-8') as f:
                        existing_results = json.load(f)
                    if not isinstance(existing_results, list):
                        existing_results = []
                except Exception as e:
                    print(f"Warning: failed to read existing results file: {e}")
                    existing_results = []

            all_results = existing_results + round_successful_results
            try:
                with open(output_results_file, 'w', encoding='utf-8') as f:
                    json.dump(all_results, f, ensure_ascii=False, indent=2)
                print(f"Round {round_num}: processed {len(round_successful_results)} rule(s); appended to {output_results_file.name}")
            except Exception as e:
                print(f"Error: failed to save results file: {e}")

        pending_rules = round_failed_rules

        if not round_failed_rules:
            print(f"\nRound {round_num} complete; all rules processed successfully")
            break

        print(f"Round {round_num}: {len(round_failed_rules)} rule(s) failed; retrying next round")

    failed_rules = pending_rules

    try:
        if output_results_file.exists():
            with open(output_results_file, 'r', encoding='utf-8') as f:
                all_results = json.load(f)
            if not isinstance(all_results, list):
                all_results = []
        else:
            all_results = []
    except Exception as e:
        print(f"Warning: failed to read results file: {e}")
        all_results = []

    if failed_rules:
        print(f"\nSaving failed rules to: {failed_rules_file}")
        try:
            with open(failed_rules_file, 'w', encoding='utf-8') as f:
                json.dump(failed_rules, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(failed_rules)} failed rule(s)")
        except Exception as e:
            print(f"Error: failed to save failed-rules file: {e}")
    else:
        print(f"\nAll rules processed successfully; no failed rules to save")

    results_file_name = output_results_file.name
    failed_file_name = failed_rules_file.name
    print("\n" + "="*80)
    print(f"Model {model} finished")
    print(f"Total rules: {total_rules}")
    print(f"Succeeded: {len(all_results)}")
    print(f"Failed: {len(failed_rules)}")
    print(f"{results_file_name} records: {len(all_results)}")
    print(f"{failed_file_name} records: {len(failed_rules)}")
    print(f"Count check: {len(all_results)} + {len(failed_rules)} = {len(all_results) + len(failed_rules)} (expected {total_rules})")
    if len(all_results) + len(failed_rules) == total_rules:
        print("✓ Count check passed")
    else:
        print("✗ Count check failed; data may be incomplete")

    if len(failed_rules) == 0:
        if len(all_results) == total_rules:
            print(f"✓ {results_file_name} record count matches total rules")
        else:
            print(f"✗ {results_file_name} record count ({len(all_results)}) does not match total rules ({total_rules})")
    print("="*80)


if __name__ == '__main__':
    print("Starting rule processing...")
    process_all_rules()
