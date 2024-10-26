import requests
from concurrent.futures import ThreadPoolExecutor
import json

def validate_proxy(proxy):
    proxy_dict = {'http': proxy, 'https': proxy}
    try:
        response = requests.get('https://www.google.com', proxies=proxy_dict, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
    
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