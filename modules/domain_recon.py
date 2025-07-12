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
        debug(f"Raw WHOIS data: {w}")

        print("=== WHOIS ===")

        # Core registrar and dates
        print(f"Registrar: {w.registrar or 'N/A'}")
        print(f"Registrant: {w.name or 'N/A'}")
        print(f"Creation Date: {w.creation_date if w.creation_date else 'N/A'}")
        print(f"Expiration Date: {w.expiration_date if w.expiration_date else 'N/A'}")

        # Nameservers
        nameservers = w.name_servers if w.name_servers else []
        if isinstance(nameservers, str):
            nameservers = [nameservers]
        print(f"Nameservers: {', '.join(nameservers) if nameservers else 'N/A'}")

        # Emails (registrant/admin/tech/abuse)
        emails = w.emails if w.emails else []
        if isinstance(emails, str):
            emails = [emails]
        print(f"Contact Emails: {', '.join(emails) if emails else 'N/A'}")

        # Registrant organization
        org = w.org or 'N/A'
        print(f"Registrant Organization: {org}")

        # Abuse contact (if sometimes in WHOIS)
        abuse_contact = w.get('abuse_contact_email') or 'N/A'
        print(f"Abuse Contact: {abuse_contact}")

        # DNSSEC
        dnssec = w.dnssec if w.dnssec else 'Not implemented'
        print(f"DNSSEC: {dnssec}")

        # Status
        status = w.status if w.status else 'N/A'
        print(f"Domain Status: {status}")

        info("WHOIS information has been identified and displayed.")

    except Exception as e:
        error(f"WHOIS lookup error: {e}")
        print("=== WHOIS ===")
        print("Failed to retrieve WHOIS information.")

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