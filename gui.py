import csv
import time
import json
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog
import requests
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

API_URL = os.environ.get('API_URL', 'http://localhost:5000')

class ProxyApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('500x300')
        self.root.title('Proxy Collector and Validator')
        self.total_proxies = 0
        self.start_time = None
        self.valid_proxies_count = 0
        self.create_widgets()

    def create_widgets(self):
        self.collect_button = ttk.Button(self.root, text='Collect Proxies', command=self.collect_proxies)
        self.collect_button.pack(pady=10)
        
        self.max_workers_label = ttk.Label(self.root, text='Max Number of Proxies to Validate at Once(Uses more system resources)')
        self.max_workers_label.pack(pady=5)
        
        self.max_workers_entry = ttk.Entry(self.root)
        self.max_workers_entry.pack(pady=5)
        self.max_workers_entry.insert(0, '20')
        
        self.validate_all_button = ttk.Button(self.root, text='Validate All Proxies', command=self.validate_all_proxies)
        self.validate_all_button.pack(pady=10)
        
        self.export_button = ttk.Button(self.root, text='Export Valid Proxies to CSV', command=self.export_to_csv)
        self.export_button.pack(pady=10)
        
        self.progress_label = ttk.Label(self.root, text='Progress')
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(self.root, orient='horizontal', mode='determinate', length=280)
        self.progress_bar.pack(pady=10)
        
    def collect_proxies(self):
        try:
            response = requests.post(f'{API_URL}/collect_proxies')
            if response.status_code == 200:
                messagebox.showinfo('Success', 'Proxies collected successfully and saved to file')
            else:
                messagebox.showerror('Error', response.json().get('message', 'Failed to collect proxies'))
        except requests.RequestException as e:
            messagebox.showerror('Error', f'Failed to connect to API: {e}')
    
    def validate_all_proxies(self):
        validate_thread = threading.Thread(target=self._validate_all_proxies)
        validate_thread.start()
    
    def _validate_all_proxies(self):
        self.start_time = time.time()
        self.valid_proxies_count = 0

        try:
            with open('proxies.json', 'r') as f:
                proxy_data = json.load(f)
                proxies = proxy_data.get('proxies', [])
                if not proxies:
                    messagebox.showerror("Error", "No proxies found in `proxies.json`.")
                    return
        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("Error", f"Failed to load proxies from file: {e}")
            return

        self.total_proxies = len(proxies)
        self.progress_bar['maximum'] = self.total_proxies
        validated_proxies = 0

        with ThreadPoolExecutor(max_workers=int(self.max_workers_entry.get())) as executor:
            future_to_proxy = {executor.submit(self._validate_proxy_request, proxy): proxy for proxy in proxies}
            for future in as_completed(future_to_proxy):
                if future.result():
                    self.valid_proxies_count += 1
                validated_proxies += 1
                self.root.after(0, self.update_progress, validated_proxies)
                
        with open('valid_proxies.json', 'r') as f:
            valid_proxies_data = json.load(f)
            valid_proxies = valid_proxies_data.get('proxies', [])
            num_valid_proxies = len(valid_proxies)

            messagebox.showinfo('Success', f'Validation complete. {num_valid_proxies} valid proxies found')
            
    def _validate_proxy_request(self, proxy):
        try:
            response = requests.post(f'{API_URL}/validate_proxy', json={'proxy': proxy})
            if response.status_code == 200:
                return response.json().get('is_valid', False)
        except requests.RequestException:
            pass
        return False
    
    def update_progress(self, validated_proxies):
        elapsed_time = time.time() - self.start_time
        avg_time_per_proxy = elapsed_time / validated_proxies if validated_proxies > 0 else 0
        remaining_proxies = self.total_proxies - validated_proxies
        estimated_remaining_time = avg_time_per_proxy * remaining_proxies
        estimated_remaining_time_formatted = time.strftime('%H:%M:%S', time.gmtime(estimated_remaining_time))

        self.progress_bar['value'] = validated_proxies
        self.progress_label.config(
            text=f'Checked {validated_proxies}/{self.total_proxies} proxies. | '
                 f'Estimated time remaining: {estimated_remaining_time_formatted}'
        )
        self.root.update_idletasks()
        
    def export_to_csv(self):
        try:
            with open('valid_proxies.json', 'r') as f:
                data = json.load(f)
                valid_proxies = data.get('proxies', [])
            
            if not valid_proxies:
                messagebox.showinfo('No Data', 'No valid proxies to export.')
                return

            file_path = 'valid_proxies.csv'  # Default file path

            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Proxy'])
                for proxy in valid_proxies:
                    writer.writerow([proxy])
                    
            messagebox.showinfo('Export Successful', f'Valid proxies exported to {file_path}')
            
        except FileNotFoundError:
            messagebox.showerror('Error', 'valid_proxies.json not found. Please validate proxies first.')
        except json.JSONDecodeError:
            messagebox.showerror('Error', 'Error reading valid_proxies.json. The file might be corrupted.')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to export to CSV: {e}')

def run_gui():
    root = tk.Tk()
    app = ProxyApp(root)
    root.mainloop()
    
if __name__ == '__main__':
    run_gui()
