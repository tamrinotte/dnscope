# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
from modules.logging_config import debug, info, error
from requests import get as reqget, RequestException

##############################

# GET DIR

##############################

def get_dir(url):
    try:
        response = reqget(url, timeout=5)
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
    found_dirs = []
    language_dirs = []

    try:
        with open(wordlist_path, 'r') as f:
            dir_list = [line.strip() for line in f]

        with ThreadPoolExecutor(max_workers=20) as executor:
            # First: scan root-level directories
            futures = {
                executor.submit(get_dir, f"http://{target_domain_name}/{directory}"): directory
                for directory in dir_list
            }

            for future in as_completed(futures):
                result = future.result()
                if result:
                    url, status = result
                    found_dirs.append(result)
                    # Check if directory name looks like a language code (2-letter ISO)
                    if len(url.split("/")[-1]) == 2:
                        language_dirs.append(url)

        # Second: scan inside any discovered language directories
        if language_dirs:
            info(f"Discovered language directories: {language_dirs}")
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = {
                    executor.submit(get_dir, f"{lang_dir}/{directory}"): directory
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