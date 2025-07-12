# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from socket import gethostbyname
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
from modules.logging_config import debug, info, error

##############################

# RESOLVE SUBDOMAIN

##############################

def resolve_subdomain(subdomain):
    try:
        gethostbyname(subdomain)
        return subdomain
    except:
        return None

##############################

# GET SUBDOMAINS

##############################

def get_subdomains(target_domain_name, wordlist_path):
    start_time=time()
    subdomains = []
    try:
        with open(wordlist_path, 'r') as f:
            subdomain_list = [line.strip() + "." + target_domain_name for line in f]
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(resolve_subdomain, sub): sub for sub in subdomain_list}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    subdomains.append(result)
        print("=== Subdomains ===")
        for index, subdomain in enumerate(subdomains, start=1):
            print(f"{index}) {subdomain}")
        end_time = time()
        duration = end_time - start_time
        print(f"Duration: {duration:.2f} seconds.")
        info(f"Subdomain enumeration has been completed. Duration: {duration:.2f} seconds.")
    except Exception as e:
        error(f"Error: {e}")
        print("=== Subdomains ===")
        print()