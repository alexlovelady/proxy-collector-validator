from flask import Flask, request, jsonify
from proxy_gatherer import fetch_proxies
from proxy_validator import validate_proxy, load_proxies, save_proxies
import os

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))

proxies = load_proxies('proxies.json')
valid_proxies = load_proxies('valid_proxies.json')

@app.route('/collect_proxies', methods=['POST'])
def collect_proxies():
    new_proxies = fetch_proxies()
    if new_proxies:
      proxies.update(new_proxies)
      save_proxies('proxies.json', proxies)
      return jsonify({"status": "success", "message": f"Collected {len(new_proxies)} new proxies"}), 200
    return jsonify({"status": "error", "message": "No new proxies found"}), 200
  
@app.route('/validate_proxy', methods=['POST'])
def validate_proxy_route():
    proxy = request.json.get('proxy')
    if proxy:
      is_valid = validate_proxy(proxy)
      if is_valid:
          valid_proxies.add(proxy)
          save_proxies('valid_proxies.json', valid_proxies)
      return jsonify({"status": "success", "message": "Proxy is valid"}), 200
    return jsonify({"status": "error", "message": "Invalid request"}), 400
  
@app.route('/validate_all_proxies', methods=['POST'])
def validate_all_proxies():
    from concurrent.futures import ThreadPoolExecutor
    
    valid_count = 0
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(validate_proxy, proxies)
        for proxy, is_valid in zip(proxies, results):
            if is_valid:
                valid_proxies.add(proxy)
                valid_count += 1
            
    save_proxies('valid_proxies.json', valid_proxies)
    return jsonify({"status": "success", "message": f"Validated {valid_count} proxies"}), 200
  
if __name__ == '__main__':
    app.run(port=port)