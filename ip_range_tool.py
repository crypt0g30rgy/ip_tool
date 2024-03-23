import argparse
import ipaddress

def generate_ips(ip_range):
    try:
        ip_network = ipaddress.ip_network(ip_range)
        return [str(ip) for ip in ip_network]
    except ValueError as e:
        print(f"Error: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Generate all possible IP addresses within a given range")
    parser.add_argument("--ip-range", help="IP range in CIDR notation (e.g., 192.168.0.0/24)", required=True)
    args = parser.parse_args()

    ips = generate_ips(args.ip_range)
    for ip in ips:
        print(ip)

if __name__ == "__main__":
    main()
