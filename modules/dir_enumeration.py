# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time, sleep
from modules.logging_config import debug, info, error
from requests import get as reqget, RequestException
from random import choice as randomchoice
from pathlib import Path
from queue import Queue
from json import load as jsonload
from os import cpu_count

##############################

# GLOBAL VARIABLES

##############################

current_dir = Path(__file__).parent
fake_user_agents_file_path = Path(current_dir.parent, "data", "fake_user_agents.json")

##############################

# LOAD JSON

##############################

def load_json(json_file_path):
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            return jsonload(file)
    except Exception as e:
        error(f"Failed to load JSON file {json_file_path}: {e}")
        return {"user_agents": []}

##############################

# GET DIR

##############################

def get_dir(url, fake_user_agents, timeout=2.5, retries=1):
    user_agent = randomchoice(fake_user_agents) if fake_user_agents else "Mozilla/5.0"
    headers = {
        "User-Agent": user_agent,
        "Referer": url,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9"
    }
    for attempt in range(retries + 1):
        try:
            response = reqget(url, headers=headers, timeout=timeout)
            if response.status_code in [200, 301, 302, 403]:
                return (url, response.status_code)
            return None
        except RequestException as e:
            debug(f"Request to {url} failed (attempt {attempt+1}/{retries+1}): {e}")
            if attempt < retries:
                sleep(0.3)
            else:
                return None

##############################

# GET DIRS

##############################

def get_dirs(target_domain_name, is_recursive, max_depth, wordlist_path, max_workers=30):
    start_time = time()
    json_data = load_json(fake_user_agents_file_path)
    fake_user_agents = json_data.get("user_agents", [])
    found_dirs = []

    try:
        with open(wordlist_path, 'r', encoding="utf-8") as f:
            dir_list = [line.strip() for line in f if line.strip()]

        dirs_to_scan = Queue()
        dirs_to_scan.put((f"http://{target_domain_name}/", 0))

        with ThreadPoolExecutor(max_workers=max_workers or cpu_count() * 2) as executor:
            while not dirs_to_scan.empty():
                base_url, depth = dirs_to_scan.get()
                if depth > max_depth:
                    continue

                futures = {
                    executor.submit(get_dir, f"{base_url}{directory}", fake_user_agents): directory
                    for directory in dir_list
                }

                new_discovered = []

                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        url, status = result
                        found_dirs.append((url, status))
                        if is_recursive:
                            new_discovered.append((f"{url}/", depth + 1))

                for item in new_discovered:
                    dirs_to_scan.put(item)

        print("\n=== Discovered Directories ===")
        for index, (url, status_code) in enumerate(found_dirs, start=1):
            print(f"{index}) {url} [Status: {status_code}]")

        duration = time() - start_time
        print(f"\nDuration: {duration:.2f} seconds.")
        info(f"Directory enumeration completed. Duration: {duration:.2f} seconds.")

    except Exception as e:
        error(f"Error during directory enumeration: {e}")
        print("\n=== Discovered Directories ===\nNone found due to an error.")
