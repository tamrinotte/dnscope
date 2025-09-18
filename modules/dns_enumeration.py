# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
import socket
import concurrent.futures
import time
from modules.logging_config import debug, info, error

##############################

# RESOLVE SUBDOMAIN

##############################

def resolve_subdomain(subdomain):
    try:
        socket.gethostbyname(subdomain)
        return subdomain
    except:
        return None

##############################

# GET SUBDOMAINS

##############################

def get_subdomains(max_workers, target_domain_name, wordlist_path):
    start_time=time.time()
    subdomains = set()

    with open(wordlist_path, 'r') as f:
        subdomain_list = [line.strip() + "." + target_domain_name for line in f]

    print(f"[+] Starting DNS enumeration for: {target_domain_name}")
    print(f"[+] Wordlist: {wordlist_path}")
    print(f"[+] Max number of workers: {max_workers}")

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(resolve_subdomain, sub): sub for sub in subdomain_list}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    subdomains.add(result)
    except KeyboardInterrupt:
        print("\n[!] Enumeration interrupted. Returning partial results.\n")
    finally:
        duration = time.time() - start_time
        print(f"\n[✓] Enumeration complete. Duration: {duration:.2f} seconds.")
        print(f"Total unique directories found: {len(subdomains)}\n")
        return subdomains