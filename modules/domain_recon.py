# -*- coding: utf-8 -*-

# MODULES AND/OR LIBRARIES
import socket
import dns.resolver
import whois
import time
from modules.logging_config import debug, error, info

##############################

# IP ADDRESS

##############################

def get_ip_addresses(target_domain_name):
    try:
        ip_addresses = []
        for result in socket.getaddrinfo(target_domain_name, 80):
            ip_addresses.append(result[4][0])
        debug(f"Raw IP addresses: {ip_addresses}")
        ip_addresses = list(set(ip_addresses))
        return ip_addresses
    except Exception as e:
        error(f"Error: {e}")

##############################

# MX RECORDS

##############################

def get_mx_records(target_domain_name):
    try:
        mx_records_raw = dns.resolver.resolve(target_domain_name, 'MX')
        mx_records = []
        for raw_data in mx_records_raw:
            mx_records.append(str(raw_data.exchange))
        debug(f"Raw mx records: {mx_records}")
        return mx_records
    except Exception as e:
        error(f"Error: {e}")

##############################

# NAMESERVERS

##############################

def get_nameservers(target_domain_name):
    try:
        nameservers_raw = dns.resolver.resolve(target_domain_name, 'NS')
        nameservers = []
        for raw_data in nameservers_raw:
            nameservers.append(str(raw_data.target))
        debug(f"Raw nameservers data: {nameservers}")
        return nameservers
    except Exception as e:
        error(f"Error: {e}")

##############################

# WHOIS

##############################

def get_whois_info(target_domain_name):
    try:
        whois_raw = whois.whois(target_domain_name)
        debug(f"Raw WHOIS data: {whois_raw}")
        whois_data = {
            "Registrar": whois_raw.registrar if whois_raw.name else 'N/A',
            "Registrant": whois_raw.name if whois_raw.name else 'N/A',
            "Creation Date": whois_raw.creation_date if whois_raw.creation_date else 'N/A',
            "Expiration Date": whois_raw.expiration_date if whois_raw.expiration_date else 'N/A',
            "Nameservers": whois_raw.name_servers if whois_raw.name_servers else [],
            "Emails": whois_raw.emails if whois_raw.emails else [],
            "Registrant Organization": whois_raw.org or 'N/A',
            "Abuse Contact": whois_raw.get('abuse_contact_email') or 'N/A',
            "DNSSEC": whois_raw.dnssec if whois_raw.dnssec else 'Not implemented',
            "Domain Status": whois_raw.status if whois_raw.status else 'N/A',
        }
        return whois_data
    except Exception as e:
        error(f"WHOIS lookup error: {e}")

##############################

# COLLECT DOMAIN INFO

##############################

def collect_domain_info(target_domain_name):
    start_time = time.time()
    print(f"[+] Collecting domain info for: {target_domain_name}")
    try:
        domain_info = {
            "IP Addresses": get_ip_addresses(target_domain_name=target_domain_name),
            "MX Records": get_mx_records(target_domain_name=target_domain_name),
            "Nameservers": get_nameservers(target_domain_name=target_domain_name),
            "Whois": get_whois_info(target_domain_name=target_domain_name),
        }
    except KeyboardInterrupt:
        print("\n[!] Enumeration interrupted. Returning partial results.\n")
    finally:
        duration = time.time() - start_time
        print(f"\n[✓] Domain information collection complete. Duration: {duration:.2f} seconds.\n")
        return domain_info