"""
Filter rules: remove rules that are hard to detect (using rules from all JSON files under file_diffs).
"""

import os
import json
import random
import re
import requests
from pathlib import Path
from typing import Dict, Any, Optional, List
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# ==================== Configuration ====================
# OpenRouter API configuration   
API_URL = "https://openrouter.ai/api/v1/responses"
API_KEY = "<your-api-key>"
MODELS = ["google/gemini-3-flash-preview", "z-ai/glm-5", "qwen/qwen3-max"]  
# Debug mode: random sample size (None = process all rules)
DEBUG_SAMPLE_SIZE = None

# Thread pool size (LLM calls are IO-bound; can increase moderately)
# Suggested: 10–20 conservative, 20–50 moderate, 50–100 aggressive; reduce if hitting 429 rate limits
MAX_WORKERS = 1

# Output file templates (model name inserted into filename)
OUTPUT_RESULTS_FILE_TEMPLATE = "filter_results_{model_name}.json"  # Save key result data (JSON format)
FAILED_RULES_FILE_TEMPLATE = "failed_rules_{model_name}.json"  # Save failed rules
DEBUG_OUTPUT_FILE_TEMPLATE = "debug_output_{model_name}.json"  # Write console output to this JSON in debug mode
# ==================================================


def get_model_name_identifier(model: str) -> str:
    """Extract an identifier from model name for filenames
    
    Examples:
    - "qwen/qwen3-coder" -> "qwen3-coder"
    - "openai/gpt-5.2" -> "gpt-5.2"
    - "google/gemini-3-pro-preview" -> "gemini-3-pro-preview"
    """
    # If slash present, take part after slash; otherwise use full name
    if '/' in model:
        return model.split('/')[-1]
    return model.replace('/', '_').replace('\\', '_')


def get_unique_file_path(base_path: Path) -> Path:
    """Get a unique file path; append _2, _3, etc. if file already exists
    
    Args:
        base_path: Base file path
        
    Returns:
        Unique file path (original if absent, otherwise with numeric suffix)
    """
    if not base_path.exists():
        return base_path
    
    # File exists; add numeric suffix
    stem = base_path.stem  # Filename without extension
    suffix = base_path.suffix  # Extension (e.g. .json)
    parent = base_path.parent  # Directory path
    
    # Try _2, _3, ... until an unused filename is found
    counter = 2
    while True:
        new_path = parent / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def load_system_prompt(prompt_file: Path) -> str:
    """Load system prompt"""
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error: cannot read system prompt file {prompt_file}: {e}")
        raise


def build_user_prompt(rule: Dict[str, Any]) -> str:
    """Build user prompt"""
    return f"""# Input Rule
{{
  "change_type": "{rule.get('change_type', '')}", 
  "first_level": "{rule.get('first_level', '')}",
  "second_level": "{rule.get('second_level', '')}",
  "content": "{rule.get('content', '')}"
}}"""


def call_openrouter_api(system_prompt: str, user_prompt: str, model: str) -> Optional[Dict[str, Any]]:
    """Call OpenRouter API"""
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
    """Extract output text from response"""
    try:
        # Get output field
        output = response_data.get('output', [])
        if not isinstance(output, list):
            print("Warning: output field is not an array")
            return None
        
        # Iterate output array for items with type "message"
        for item in output:
            if not isinstance(item, dict):
                continue
            
            if item.get('type') == 'message':
                # Get content array
                content = item.get('content', [])
                if not isinstance(content, list):
                    continue
                
                # Iterate content array for items with type "output_text"
                for content_item in content:
                    if not isinstance(content_item, dict):
                        continue
                    
                    if content_item.get('type') == 'output_text':
                        text = content_item.get('text', '')
                        if text:
                            return text
        
        print("Warning: output text not found")
        return None
    
    except Exception as e:
        print(f"Error extracting output text: {e}")
        return None


def parse_output_json(output_text: str) -> Optional[Dict[str, Any]]:
    """Parse JSON object from output text"""
    if not output_text:
        return None
    
    try:
        # Try parsing entire text directly
        parsed = json.loads(output_text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    
    # If direct parse fails, try extracting JSON code block
    try:
        # Find JSON code block (```json ... ```)
        json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
        matches = re.findall(json_pattern, output_text, re.DOTALL)
        if matches:
            parsed = json.loads(matches[0])
            if isinstance(parsed, dict):
                return parsed
    except (json.JSONDecodeError, IndexError):
        pass
    
    # Try content between first { and last }
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
    
    print("Warning: cannot parse JSON from output text")
    return None


def process_rule(rule: Dict[str, Any], system_prompt: str, model: str, output_func=None, is_debug_mode=False) -> tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]], bool, Optional[Dict[str, str]]]:
    """
    Process a single rule
    
    Args:
        rule: Rule object
        system_prompt: System prompt
        model: Model name
        output_func: Output function; uses print if None
        is_debug_mode: Whether debug mode is enabled
    
    Returns:
        tuple: (full response with rule_id, key result data, success flag, debug input+output or None)
    """
    if output_func is None:
        output_func = print
    
    rule_id = rule.get('id', 'unknown')
    
    # Output details only in debug mode (DEBUG no longer prints each rule to console)
    if is_debug_mode:
        output_func(f"Processing rule: {rule_id}")
        content = rule.get('content', '')
        output_func(f"Rule Content: {content}\n")
    
    # Build user prompt
    user_prompt = build_user_prompt(rule)
    
    # Call API
    response_data = call_openrouter_api(system_prompt, user_prompt, model)
    
    if response_data is None:
        # Always print errors (debug and non-debug)
        print(f"Rule {rule_id}: API call failed")
        debug_entry = None
        if is_debug_mode:
            debug_entry = {
                "rule_id": rule_id,
                "change_type": rule.get("change_type", ""),
                "first_level": rule.get("first_level", ""),
                "second_level": rule.get("second_level", ""),
                "content": rule.get("content", ""),
                "success": False,
            }
        return None, None, False, debug_entry
    
    # Add rule_id to response data
    response_with_id = response_data.copy()
    response_with_id['rule_id'] = rule_id
    
    # Extract and output text
    output_text = extract_output_text(response_data)
    
    # Parse JSON from output text
    parsed_json = None
    if output_text:
        parsed_json = parse_output_json(output_text)
    
    # Build key result: rule_id, rule_content, and parsed JSON fields
    result_data = {
        'rule_id': rule_id,
        'rule_content': rule.get('content', '')
    }
    
    # Merge parsed JSON fields into result if successful
    if parsed_json:
        result_data.update(parsed_json)
    
    # Debug-only detail output (logic kept for debug_entry)
    if is_debug_mode and output_text:
        output_func(f"\n{'='*80}")
        output_func(f"Rule ID: {rule_id}")
        output_func(f"{'='*80}")
        output_func(output_text)
        output_func(f"{'='*80}\n")
    elif not output_text and is_debug_mode:
        output_func(f"Warning: rule {rule_id} has no output text")
    
    # Success requires both output text and parsed JSON
    success = bool(output_text and parsed_json)
    
    # Warn if text extracted but JSON parse failed
    if output_text and not parsed_json:
        print(f"Warning: rule {rule_id} has output text but JSON parse failed; marking as failed")
    
    # Debug entry: rule_id, four input fields, output fields; content only (no duplicate rule_content)
    debug_entry = None
    if is_debug_mode:
        if success and result_data is not None and parsed_json is not None:
            debug_entry = {
                "rule_id": rule_id,
                "change_type": rule.get("change_type", ""),
                "first_level": rule.get("first_level", ""),
                "second_level": rule.get("second_level", ""),
                "content": rule.get("content", ""),
            }
            debug_entry.update(parsed_json)
        else:
            debug_entry = {
                "rule_id": rule_id,
                "change_type": rule.get("change_type", ""),
                "first_level": rule.get("first_level", ""),
                "second_level": rule.get("second_level", ""),
                "content": rule.get("content", ""),
                "success": False,
            }
    return response_with_id, result_data, success, debug_entry


def find_all_json_files(file_diffs_dir: Path) -> list:
    """Find all JSON files"""
    json_files = list(file_diffs_dir.rglob('*.json'))
    print(f"Found {len(json_files)} JSON files")
    return json_files


def process_all_rules():
    """Process all rules (once per model)"""
    # Script directory
    script_dir = Path(__file__).parent
    file_diffs_dir = script_dir.parent.parent / "rq2_1_evolved_rules" / "file_diffs"
    system_prompt_file = script_dir / 'filter_system_prompt.txt'
    
    # Iterate over each model
    for model in MODELS:
        model_name = get_model_name_identifier(model)
        print("\n" + "="*80)
        print(f"Starting model: {model}")
        print("="*80)
        
        # Base filenames with model name
        base_failed_rules_file = script_dir / FAILED_RULES_FILE_TEMPLATE.format(model_name=model_name)
        
        # Unique paths (suffix if file exists)
        failed_rules_file = get_unique_file_path(base_failed_rules_file)
        
        # Notify if filename was changed
        if failed_rules_file != base_failed_rules_file:
            print(f"Note: {base_failed_rules_file.name} exists; using {failed_rules_file.name}")
        
        # Process rules for current model
        process_rules_for_model(model, script_dir, file_diffs_dir, system_prompt_file, 
                               failed_rules_file)


def process_rules_for_model(model: str, script_dir: Path, file_diffs_dir: Path, 
                           system_prompt_file: Path, failed_rules_file: Path):
    """Process all rules for one model"""
    
    # Check directories and files
    if not file_diffs_dir.exists():
        print(f"Error: directory not found: {file_diffs_dir}")
        return
    
    if not system_prompt_file.exists():
        print(f"Error: system prompt file not found: {system_prompt_file}")
        return
    
    # Load system prompt
    print("Loading system prompt...")
    system_prompt = load_system_prompt(system_prompt_file)
    
    # Find all JSON files
    json_files = find_all_json_files(file_diffs_dir)
    
    # Collect all valid rules first
    all_valid_rules: List[Dict[str, Any]] = []
    
    print("Collecting all rules...")
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                continue
            
            # Collect valid rules
            for rule in data:
                if not isinstance(rule, dict):
                    continue
                
                # Check required fields
                if all(key in rule for key in ['id', 'change_type', 'first_level', 'second_level', 'content']):
                    all_valid_rules.append(rule)
        
        except json.JSONDecodeError as e:
            print(f"Warning: cannot parse JSON file {json_file}: {e}")
            continue
        except Exception as e:
            print(f"Warning: error processing file {json_file}: {e}")
            continue
    
    print(f"Collected {len(all_valid_rules)} valid rules in total")
    
    # Random sample if debug mode enabled
    if DEBUG_SAMPLE_SIZE is not None and len(all_valid_rules) > DEBUG_SAMPLE_SIZE:
        print(f"Debug mode: randomly selected {DEBUG_SAMPLE_SIZE} rules to process")
        rules_to_process = random.sample(all_valid_rules, DEBUG_SAMPLE_SIZE)
    else:
        print("Processing all rules")
        rules_to_process = all_valid_rules
    
    # Statistics
    total_rules = len(rules_to_process)
    
    # Whether debug mode is active
    is_debug_mode = DEBUG_SAMPLE_SIZE is not None
    
    # Debug: collect per-rule results (filter_results format + change_type/first_level/second_level/content)
    debug_entries: List[Dict[str, Any]] = []
    
    # Output function; DEBUG skips per-rule console output
    def output_func(text):
        if not is_debug_mode:
            pass  # Non-debug: only errors via print
        # Debug mode: no per-rule console output
    
    # Pending rules (initially all rules)
    pending_rules = rules_to_process.copy()
    
    # Output results path (model name; suffix if exists)
    model_name = get_model_name_identifier(model)
    base_output_results_file = script_dir / OUTPUT_RESULTS_FILE_TEMPLATE.format(model_name=model_name)
    output_results_file = get_unique_file_path(base_output_results_file)
    
    # Notify if results filename changed (non-debug writes this file)
    if not is_debug_mode and output_results_file != base_output_results_file:
        print(f"Note: {base_output_results_file.name} exists; using {output_results_file.name}")
    
    # Up to 10 retry rounds
    max_retries = 10
    
    # Debug: skip filter_results file; accumulate successes in memory for debug_output
    all_results_accumulated: List[Dict[str, Any]] = []
    
    # Before round 1: init results file (non-debug only)
    if not is_debug_mode:
        try:
            with open(output_results_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Warning: failed to initialize results file: {e}")
    
    # First round: process all rules
    print(f"\nStarting round 1, {len(pending_rules)} rules...")
    print(f"Using {MAX_WORKERS} worker threads\n")
    
    for round_num in range(1, max_retries + 1):
        if not pending_rules:
            print(f"\nAll rules processed; no retry round {round_num} needed")
            break
        
        if round_num > 1:
            print(f"\nStarting retry round {round_num}, {len(pending_rules)} failed rules remaining...")
        
        # Round successes/failures (lock-protected for thread pool)
        round_successful_results: List[Dict[str, Any]] = []
        round_failed_rules: List[Dict[str, Any]] = []
        results_lock = Lock()
        
        # Wrapper for thread pool
        def process_rule_wrapper(rule: Dict[str, Any]) -> tuple:
            """Thread pool worker; returns (rule, result_data, success, debug_entry)"""
            try:
                _, result_data, success, debug_entry = process_rule(
                    rule, system_prompt, model, output_func, is_debug_mode
                )
                return rule, result_data, success, debug_entry
            except Exception as e:
                rule_id = rule.get('id', 'unknown')
                print(f"Error processing rule {rule_id}: {e}")
                debug_entry = None
                if is_debug_mode:
                    debug_entry = {
                        "rule_id": rule.get("id", "unknown"),
                        "change_type": rule.get("change_type", ""),
                        "first_level": rule.get("first_level", ""),
                        "second_level": rule.get("second_level", ""),
                        "content": rule.get("content", ""),
                        "success": False,
                    }
                else:
                    debug_entry = None
                return rule, None, False, debug_entry
        
        # Process rules concurrently via thread pool
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_rule = {executor.submit(process_rule_wrapper, rule): rule for rule in pending_rules}
            desc = f"Round {round_num}" if round_num > 1 else "Round 1"
            with tqdm(total=len(pending_rules), desc=desc, unit="rules") as pbar:
                for future in as_completed(future_to_rule):
                    rule, result_data, success, debug_entry = future.result()
                    with results_lock:
                        if success and result_data is not None:
                            round_successful_results.append(result_data)
                        else:
                            round_failed_rules.append(rule)
                        if is_debug_mode and debug_entry is not None:
                            debug_entries.append(debug_entry)
                    pbar.update(1)
        
        # Append round successes (debug accumulates in memory only)
        if round_successful_results:
            if is_debug_mode:
                all_results_accumulated.extend(round_successful_results)
            else:
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
                    print(f"Round {round_num}: processed {len(round_successful_results)} rules; appended to {output_results_file.name}")
                except Exception as e:
                    print(f"Error saving results file: {e}")
        
        # Pending rules = failures from this round
        pending_rules = round_failed_rules
        
        # Exit early if no failures this round
        if not round_failed_rules:
            print(f"\nRound {round_num} complete; all rules succeeded")
            break
        
        print(f"Round {round_num}: {len(round_failed_rules)} failed; will retry next round")
    
    # Save remaining failures to failed_rules (non-debug)
    failed_rules = pending_rules
    
    # Final results: memory (debug) or file (non-debug)
    if is_debug_mode:
        all_results = all_results_accumulated
    else:
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
    
    if failed_rules and not is_debug_mode:
        print(f"\nSaving failed rules to: {failed_rules_file}")
        try:
            with open(failed_rules_file, 'w', encoding='utf-8') as f:
                json.dump(failed_rules, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(failed_rules)} failed rules")
        except Exception as e:
            print(f"Error saving failed rules file: {e}")
    elif not is_debug_mode and not failed_rules:
        print(f"\nAll rules succeeded; no failed rules to save")
    
    # Print summary statistics
    if is_debug_mode:
        # Debug: summary only; count can_detect true/false
        can_detect_true = sum(1 for e in debug_entries if e.get("can_detect") is True)
        can_detect_false = sum(1 for e in debug_entries if e.get("can_detect") is False)
        print("\n" + "="*80)
        print("DEBUG mode summary")
        print(f"Rules processed: {total_rules}")
        print(f"Succeeded: {len(all_results)}")
        print(f"Failed: {len(failed_rules)}")
        print(f"can_detect true: {can_detect_true}")
        print(f"can_detect false: {can_detect_false}")
        print("="*80)
    else:
        results_file_name = output_results_file.name
        failed_file_name = failed_rules_file.name
        print("\n" + "="*80)
        print(f"Model {model} processing complete")
        print(f"Total rules: {total_rules}")
        print(f"Succeeded: {len(all_results)}")
        print(f"Failed: {len(failed_rules)}")
        print(f"{results_file_name} record count: {len(all_results)}")
        print(f"{failed_file_name} record count: {len(failed_rules)}")
        print(f"Total check: {len(all_results)} + {len(failed_rules)} = {len(all_results) + len(failed_rules)} (expected {total_rules})")
        if len(all_results) + len(failed_rules) == total_rules:
            print("✓ Total check passed")
        else:
            print("✗ Total check failed; data may be incomplete")
        if len(failed_rules) == 0:
            if len(all_results) == total_rules:
                print(f"✓ {results_file_name} record count matches total rules")
            else:
                print(f"✗ {results_file_name} count ({len(all_results)}) != total rules ({total_rules})")
        print("="*80)
    
    # Debug: write debug_output_{model_name}.json as filter_results-shaped array
    if is_debug_mode and debug_entries:
        debug_output_file = script_dir / DEBUG_OUTPUT_FILE_TEMPLATE.format(model_name=model_name)
        try:
            with open(debug_output_file, 'w', encoding='utf-8') as f:
                json.dump(debug_entries, f, ensure_ascii=False, indent=2)
            print(f"Debug results written to: {debug_output_file.name}")
        except Exception as e:
            print(f"Warning: failed to write debug output file: {e}")


if __name__ == '__main__':
    print("Starting rule processing...")
    process_all_rules()