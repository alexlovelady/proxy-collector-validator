import requests
from bs4 import BeautifulSoup
import json

def fetch_proxies():
    proxy_sources = [
        'https://www.sslproxies.org/',
        'https://free-proxy-list.net/',
        'https://www.us-proxy.org/',
        'https://www.socks-proxy.net/'
    ]
    proxies = set()
    
    for url in proxy_sources:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'class': 'table table-striped table-bordered'})
            if not table:
                continue
            
            for row in table.find('tbody').find_all('tr'):
                tds = row.find_all('td')
                if len(tds) >= 2:
                    ip = tds[0].text.strip()
                    port = tds[1].text.strip()
                    proxy = f"{ip}:{port}"
                    proxies.add(proxy)
        except requests.RequestException:
            continue
        
    return proxies

def save_proxies(file_path, proxies):
    with open(file_path, 'w') as f:
        json.dump({'proxies': list(proxies)}, f)
        
def load_proxies(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return set(data['proxies'])
    except (FileNotFoundError, json.JSONDecodeError):
        return set()