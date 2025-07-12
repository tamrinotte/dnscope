# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from socket import getaddrinfo
from dns.resolver import resolve as dnsresolve
from whois import whois
from modules.logging_config import debug, error, info
from time import time

##############################

# IP ADDRESS

##############################

def get_ip_addresses(target_domain_name):
    try:
        ip_addresses = []
        for result in getaddrinfo(target_domain_name, 80):
            ip_addresses.append(result[4][0])
        debug(f"Raw IP addresses: {ip_addresses}")
        ip_addresses = list(set(ip_addresses))
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

def get_mx_records(target_domain_name):
    try:
        answers = dnsresolve(target_domain_name, 'MX')
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

def get_nameservers(target_domain_name):
    try:
        answers = dnsresolve(target_domain_name, 'NS')
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

def get_whois_info(target_domain_name):
    try:
        w = whois(target_domain_name)
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

# COLLECT DOMAIN INFO

##############################

def collect_domain_info(target_domain_name):
    start_time = time()
    get_ip_addresses(target_domain_name=target_domain_name)
    get_mx_records(target_domain_name=target_domain_name)
    get_nameservers(target_domain_name=target_domain_name)
    get_whois_info(target_domain_name=target_domain_name)
    end_time = time()
    duration = end_time - start_time
    print(f"Duration: {duration:.2f} seconds.")
    info(f"Domain information has been collected. Duration: {duration:.2f} seconds.")