# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from argparse import ArgumentParser
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
        wordlist_path,
    ):
        self.domain = domain
        self.is_domain_information_requested = is_domain_information_requested
        self.is_dns_enumeration_requested = is_dns_enumeration_requested
        self.is_dir_enumeration_requested = is_dir_enumeration_requested
        self.wordlist_path = wordlist_path
        self.results = {}

    ##############################

    # DNS RECON

    ##############################

    def gather_domain_info(self):
        collect_domain_info(target_domain_name=self.domain)

    ##############################

    # DNS ENUMERATION

    ##############################

    def perform_dns_enumeration(self):
        get_subdomains(target_domain_name=self.domain, wordlist_path=self.wordlist_path)

    ##############################

    # DIR ENUMERATION

    ##############################

    def perform_dir_enumeration(self):
        get_dirs(target_domain_name=self.domain, wordlist_path=self.wordlist_path)

    ##############################

    # START

    ##############################

    def start(self):
        if self.is_domain_information_requested:
            self.gather_domain_info()
        if self.is_dns_enumeration_requested:
            self.perform_dns_enumeration()
        elif self.is_dir_enumeration_requested:
            self.perform_dir_enumeration()

##############################

# MAIN

##############################

def main():
    parser = ArgumentParser(description="DNS & WHOIS Recon Tool")
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("-gdi", action="store_true", help="Gather information about the target domain.")
    mod_group = parser.add_mutually_exclusive_group(required=False)
    mod_group.add_argument("-dns", action="store_true", help="Enumerate subdomains.")
    mod_group.add_argument("-dir", action="store_true", help="Enumerate directories.")
    parser.add_argument("-w", "--wordlist", default="wordlist.txt", help="Path to your wordlist file.")
    args = parser.parse_args()
    dnscope = DNScope(
        domain=args.domain,
        is_domain_information_requested=args.gdi,
        is_dns_enumeration_requested=args.dns,
        is_dir_enumeration_requested=args.dir,
        wordlist_path=args.wordlist,
    )
    dnscope.start()

if __name__ == "__main__":
    main()