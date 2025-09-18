# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
import argparse
import sys
from modules.domain_recon import collect_domain_info
from modules.dns_enumeration import get_subdomains
from modules.dir_enumeration import get_dirs

##############################

# DNScope

##############################

class DNScope:
    def __init__(
        self,
        domain,
        is_domain_information_requested,
        is_dns_enumeration_requested,
        is_dir_enumeration_requested,
        max_depth,
        workers,
        wordlist_path,
    ):
        self.domain = domain
        self.is_domain_information_requested = is_domain_information_requested
        self.is_dns_enumeration_requested = is_dns_enumeration_requested
        self.is_dir_enumeration_requested = is_dir_enumeration_requested
        self.wordlist_path = wordlist_path
        self.max_depth = max_depth
        self.is_recursive = True if self.max_depth is not None else False
        self.workers = workers
        self.results = {}

    ##############################

    # DOMAIN RECON

    ##############################

    def gather_domain_info(self):
        return collect_domain_info(target_domain_name=self.domain)

    ##############################

    # DNS ENUMERATION

    ##############################

    def perform_dns_enumeration(self):
        return get_subdomains(
            max_workers=self.workers,
            target_domain_name=self.domain,
            wordlist_path=self.wordlist_path
        )

    ##############################

    # DIR ENUMERATION

    ##############################

    def perform_dir_enumeration(self):
        return get_dirs(
            max_workers=self.workers,
            target_domain_name=self.domain,
            is_recursive=self.is_recursive,
            max_depth=self.max_depth,
            wordlist_path=self.wordlist_path,
        )

    ##############################

    # PRINT

    ##############################

    def print_results(self):
        if self.results.get("domain_info") is not None and self.is_domain_information_requested:
            print("[+] Domain info found:")
            if self.results["domain_info"]:
                # print(self.results["domain_info"])
                for key, value in self.results["domain_info"].items():
                    print(f'{key}: {value}')
            else:
                print("No domain info found.")
            print()

        if self.results.get("subdomains") is not None and self.is_dns_enumeration_requested:
            print("[+] Subdomains found:")
            if self.results["subdomains"]:
                for subdomain in self.results["subdomains"]:
                    print(subdomain)
            else:
                print("No subdomains found.")
            print()

        elif self.results.get("directories") is not None and self.is_dir_enumeration_requested:
            print("[+] Directories found:")
            if self.results["directories"]:
                for dir in self.results["directories"]:
                    print(dir)
            else:
                print("No directories found.")
            print()

    ##############################

    # START

    ##############################

    def start(self):
        try:
            if self.is_domain_information_requested:
                domain_info = self.gather_domain_info()
            if self.is_dns_enumeration_requested:
                subdomains = self.perform_dns_enumeration()
            elif self.is_dir_enumeration_requested:
                directories = self.perform_dir_enumeration()
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user (KeyboardInterrupt). Printing partial results:")
        finally:
            if self.is_domain_information_requested:
                self.results["domain_info"] = domain_info if domain_info else []
            if self.is_dns_enumeration_requested:
                self.results["subdomains"] = subdomains if subdomains else []
            elif self.is_dir_enumeration_requested:
                self.results["directories"] = directories if directories else []
            self.print_results()
            sys.exit()

##############################

# MAIN

##############################

def main():
    parser = argparse.ArgumentParser(description="DNS & WHOIS Recon Tool")
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("-gdi", action="store_true", help="Gather information about the target domain.")
    mod_group = parser.add_mutually_exclusive_group(required=False)
    mod_group.add_argument("-dns", action="store_true", help="Enumerate subdomains.")
    mod_group.add_argument("-dir", action="store_true", help="Enumerate directories.")
    parser.add_argument(
        "-r", "--recursive",
        type=int,
        default=0,
        help="Enable recursive directory enumeration. Specify max depth."
    )
    parser.add_argument("-w", "--wordlist", default="wordlist.txt", help="Path to your wordlist file.")
    parser.add_argument("-mw", "--max_worker", type=int, default=10, help="Maximum amount of workers.")
    args = parser.parse_args()
    dnscope = DNScope(
        domain=args.domain,
        is_domain_information_requested=args.gdi,
        is_dns_enumeration_requested=args.dns,
        is_dir_enumeration_requested=args.dir,
        max_depth=args.recursive,
        wordlist_path=args.wordlist,
        workers=args.max_worker,
    )
    dnscope.start()

if __name__ == "__main__":
    main()