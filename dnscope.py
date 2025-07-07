# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from socket import gethostbyname, getaddrinfo
from dns.resolver import resolve as dnsresolve
from whois import whois
from logging import (
    basicConfig,
    DEBUG,
    CRITICAL,
    disable,
    debug,
    info,
    error,
)
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed



##############################

# LOGGING CONFIG

##############################

basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
disable(CRITICAL)



##############################

# DNScope

##############################

class DNScope:
    def __init__(self, domain, wordlist_path):
        self.domain = domain
        self.wordlist_path = wordlist_path
        self.results = {}

    ##############################

    # IP ADDRESS

    ##############################

    def get_ip_addresses(self):
        try:
            ip_addresses = []
            for result in getaddrinfo(self.domain, 80):
                ip_addresses.append(result[4][0])
            ip_addresses = list(set(ip_addresses))  # Remove duplicates
            print("=== IP Addresses ===")
            for index, ip_address in enumerate(ip_addresses, start=1):
                print(f"{index}) {ip_address}")
            info("IP addresses have been obtained.")
        except Exception as e:
            error(f"Error: {e}")
            print("=== IP Addresses ===")
            print()

    ##############################

    # MX RECORDS

    ##############################

    def get_mx_records(self):
        try:
            answers = dnsresolve(self.domain, 'MX')
            debug(f"Raw mx records: {answers}")
            print("=== MX Records ===")
            for index, raw_data in enumerate(answers, start=1):
                print(f"{index}) {str(raw_data.exchange)}")
            info("MX records has been displayed.")
        except Exception as e:
            error(f"Error: {e}")
            print("=== MX Records ===")
            print()

    ##############################

    # NAMESERVERS

    ##############################

    def get_nameservers(self):
        try:
            answers = dnsresolve(self.domain, 'NS')
            debug(f"Raw nameservers data: {answers}")
            print("=== Nameservers ===")
            for index, raw_data in enumerate(answers, start=1):
                print(f"{index}) {str(raw_data.target)}")
            info("Nameservers has been found.")
        except Exception as e:
            error(f"Error: {e}")
            print("=== Nameservers ===")
            print()

    ##############################

    # WHOIS

    ##############################

    def get_whois_info(self):
        try:
            w = whois(self.domain)
            debug(f"Raw whois data: {w}")
            print("=== WHOIS ===")
            print(f"Registrar: {w.registrar}")
            print(f"Registrant: {w.name}")
            print(f"Creation Date: {str(w.creation_date)}")
            print(f"Expiration Date: {str(w.expiration_date)}")
            info("Whois info has been identified.")
        except Exception as e:
            error(f"Error: {e}")
            print("=== WHOIS ===")
            print()

    ##############################

    # SUBDOMAINS

    ##############################

    def get_subdomains(self):
        subdomains = []
        try:
            with open(self.wordlist_path, 'r') as f:
                subdomain_list = [line.strip() + "." + self.domain for line in f]
            def resolve(subdomain):
                try:
                    gethostbyname(subdomain)
                    return subdomain
                except:
                    return None
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = {executor.submit(resolve, sub): sub for sub in subdomain_list}
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        subdomains.append(result)
            print("=== Subdomains ===")
            for index, subdomain in enumerate(subdomains, start=1):
                print(f"{index}) {subdomain}")
            info("Subdomain enumeration has been completed.")
        except Exception as e:
            error(f"Error: {e}")
            print("=== Subdomains ===")
            print()

    ##############################

    # START

    ##############################
    
    def start(self):
        self.get_ip_addresses()
        self.get_mx_records()
        self.get_nameservers()
        self.get_whois_info()
        self.get_subdomains()



##############################

# MAIN

##############################

def main():
    parser = ArgumentParser(description="DNS & WHOIS Recon Tool")
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("--wordlist", default="subdomains.txt", help="Subdomains wordlist file.")
    args = parser.parse_args()

    dnscope = DNScope(args.domain, args.wordlist)
    dnscope.start()

if __name__ == "__main__":
    main()