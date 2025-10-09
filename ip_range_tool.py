#!/usr/bin/env python3

import argparse
import ipaddress
from pathlib import Path

def generate_ips(ip_range):
    """Generate all IPs in a CIDR range."""
    try:
        ip_network = ipaddress.ip_network(ip_range.strip(), strict=False)
        return [str(ip) for ip in ip_network]
    except ValueError as e:
        print(f"Skipping invalid range '{ip_range.strip()}': {e}")
        return []

def main():
    parser = argparse.ArgumentParser(
        description="Generate all possible IP addresses from CIDR ranges (single or from file)."
    )
    parser.add_argument(
        "--ip-range",
        help="Single IP range in CIDR notation (e.g., 192.168.0.0/24)."
    )
    parser.add_argument(
        "--file",
        help="Path to a text file containing multiple CIDR prefixes (one per line)."
    )
    parser.add_argument(
        "--output",
        help="Optional output file to save generated IPs (e.g., all_ips.txt)."
    )

    args = parser.parse_args()

    all_ips = []

    # Handle single range
    if args.ip_range:
        all_ips.extend(generate_ips(args.ip_range))

    # Handle file input
    if args.file:
        path = Path(args.file)
        if not path.is_file():
            print(f"Error: File '{args.file}' not found.")
            return
        with open(path, "r") as f:
            for line in f:
                if line.strip():
                    all_ips.extend(generate_ips(line.strip()))

    if not all_ips:
        print("No IPs generated. Check your input.")
        return

    # Output results
    if args.output:
        with open(args.output, "w") as f:
            for ip in all_ips:
                f.write(ip + "\n")
        print(f"✅ Generated {len(all_ips)} IPs and saved to '{args.output}'.")
    else:
        print(f"✅ Generated {len(all_ips)} IPs:\n")
        for ip in all_ips:
            print(ip)

if __name__ == "__main__":
    main()