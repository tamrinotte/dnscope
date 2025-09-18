# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
import time
import requests
import random
import pathlib
import concurrent.futures
import json
import queue
from modules.logging_config import debug, error

##############################

# CONSTANTS

##############################

current_dir = pathlib.Path(__file__).parent
fake_user_agents_file_path = pathlib.Path(current_dir.parent, "data", "fake_user_agents.json")

##############################

# LOAD JSON

##############################

def load_json(json_file_path):
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        error(f"Failed to load JSON file {json_file_path}: {e}")
        return {"user_agents": []}

##############################

# GET DIR

##############################

def get_dir(url, fake_user_agent, timeout=2.5, retries=1):
    headers = {
        "User-Agent": fake_user_agent,
        "Referer": url,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    for attempt in range(retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code in (200, 301, 302, 403):
                return (url, response.status_code)
            return None
        except requests.RequestException as e:
            debug(f"Request to {url} failed (attempt {attempt+1}/{retries+1}): {e}")
            if attempt < retries:
                time.sleep(0.2)
            else:
                return None

##############################

# GET DIRS

##############################

def get_dirs(max_workers, target_domain_name, is_recursive, max_depth, wordlist_path):
    start_time = time.time()
    directories = set()
    json_data = load_json(fake_user_agents_file_path)
    fake_user_agents = json_data.get("user_agents", [])
    user_agent = random.choice(fake_user_agents) if fake_user_agents else "Mozilla/5.0"

    with open(wordlist_path, "r", encoding="utf-8") as wordlist_file:
        dir_list = [line.strip() for line in wordlist_file if line.strip()]

    dirs_to_scan = queue.Queue()
    dirs_to_scan.put((f"http://{target_domain_name}/", 0))

    print(f"[+] Starting directory enumeration for: {target_domain_name}")
    print(f"[+] Wordlist: {wordlist_path}")
    print(f"[+] Max number of workers: {max_workers}")
    print(f"[+] Max depth: {max_depth}")

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            while not dirs_to_scan.empty():
                base_url, depth = dirs_to_scan.get()
                if depth > max_depth:
                    continue

                # Submit all jobs and keep the Future objects
                futures = {}
                for directory in dir_list:
                    future = executor.submit(get_dir, f"{base_url}{directory}", user_agent)
                    futures[future] = directory

                new_discovered = []

                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result:
                        url, status = result
                        directories.add((url, status))
                        if is_recursive:
                            new_discovered.append((f"{url}/", depth + 1))

                for item in new_discovered:
                    dirs_to_scan.put(item)
    except KeyboardInterrupt:
        print("\n[!] Enumeration interrupted. Returning partial results.\n")
    finally:
        duration = time.time() - start_time
        print(f"\n[✓] Enumeration complete. Duration: {duration:.2f} seconds.")
        print(f"Total unique directories found: {len(directories)}\n")
        return directories