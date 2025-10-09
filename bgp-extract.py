#!/usr/bin/env python3

import requests
import re

# URL to fetch data from
url = 'https://bgp.he.net/search?search%5Bsearch%5D=contry&commit=Search'

# Fetch the HTML content from the URL
try:
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    response.raise_for_status()
    html_snippet = response.text
except requests.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit()

# Regex patterns
asn_pattern = r'<a href="/AS(\d+)">AS\d+</a>'
ip_pattern = r'<a href="/net/([0-9a-fA-F:.%/]+)">[0-9a-fA-F:.%/]+</a>'

# Extract ASNs and IP prefixes
asns = sorted(set(re.findall(asn_pattern, html_snippet)))
ip_prefixes = sorted(set(re.findall(ip_pattern, html_snippet)))

# Write ASNs to file
with open('asns.txt', 'w') as f:
    for asn in asns:
        f.write(f"AS{asn}\n")

# Write IP prefixes to file
with open('ip_prefixes.txt', 'w') as f:
    for ip in ip_prefixes:
        f.write(f"{ip}\n")

# Summary
print(f"✅ Extracted {len(asns)} ASNs and {len(ip_prefixes)} IP prefixes.")
print("Results saved to 'asns.txt' and 'ip_prefixes.txt'.")