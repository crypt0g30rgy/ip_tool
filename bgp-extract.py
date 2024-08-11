import requests
import re

# URL to fetch data from
url = 'http://example.com/page'  # Replace with your actual URL

# Fetch the HTML content from the URL
try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    html_snippet = response.text
except requests.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit()

# Regex pattern to match the IP address and prefix
pattern = r'(?<=<a href="/net/)[^/]+'

# Find the IP address using regex
match = re.search(pattern, html_snippet)

if match:
    ip_address = match.group()
    print(f"Extracted IP address: {ip_address}")
else:
    print("No IP address found.")
