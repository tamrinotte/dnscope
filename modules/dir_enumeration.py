# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
from modules.logging_config import debug, info, error
from requests import get as reqget, RequestException
from random import choice as randomchoice
from pathlib import Path
from json import load as jsonload

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
            data = jsonload(file)
        return data
    except Exception as e:
        error(f"Failed to load JSON file {json_file_path}: {e}")
        return {"user_agents": []}

##############################

# GET DIR

##############################

def get_dir(url, fake_user_agents):
    try:
        user_agent = randomchoice(fake_user_agents) if fake_user_agents else "Mozilla/5.0"
        headers = {
            "User-Agent": user_agent,
            "Referer": url,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9"
        }
        response = reqget(url, headers=headers, timeout=5)
        if response.status_code in [200, 301, 302, 403]:
            return (url, response.status_code)
        else:
            return None
    except RequestException as e:
        debug(f"Request to {url} failed: {e}")
        return None

##############################

# GET DIRS

##############################

def get_dirs(target_domain_name, wordlist_path):
    start_time = time()
    json_data = load_json(fake_user_agents_file_path)
    fake_user_agents = json_data.get("user_agents", [])
    found_dirs = []
    language_dirs = []

    try:
        with open(wordlist_path, 'r', encoding="utf-8") as f:
            dir_list = [line.strip() for line in f if line.strip()]

        with ThreadPoolExecutor(max_workers=20) as executor:
            # First: scan root-level directories
            futures = {
                executor.submit(get_dir, f"http://{target_domain_name}/{directory}", fake_user_agents): directory
                for directory in dir_list
            }

            for future in as_completed(futures):
                result = future.result()
                if result:
                    url, status = result
                    found_dirs.append(result)
                    # Check if directory name looks like a language code (2-letter ISO)
                    last_segment = url.rstrip("/").split("/")[-1]
                    if len(last_segment) == 2 and last_segment.isalpha():
                        language_dirs.append(url)

        # Second: scan inside any discovered language directories
        if language_dirs:
            info(f"Discovered language directories: {language_dirs}")
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = {
                    executor.submit(get_dir, f"{lang_dir}/{directory}", fake_user_agents): directory
                    for lang_dir in language_dirs
                    for directory in dir_list
                }

                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        found_dirs.append(result)

        print("=== Discovered Directories ===")
        for index, (url, status_code) in enumerate(found_dirs, start=1):
            print(f"{index}) {url} [Status: {status_code}]")

        end_time = time()
        duration = end_time - start_time
        print(f"Duration: {duration:.2f} seconds.")
        info(f"Directory enumeration completed. Duration: {duration:.2f} seconds.")

    except Exception as e:
        error(f"Error during directory enumeration: {e}")
        print("=== Discovered Directories ===")
        print("None found due to an error.")