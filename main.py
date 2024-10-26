import threading
import subprocess
import os
import tkinter as tk
from gui import ProxyApp

def start_flask_server():
    os.environ['PORT'] = '5000'
    subprocess.run(['python', 'app.py'])
    
def start_gui():
    os.environ['API_URL'] = 'http://localhost:5000'
    root = tk.Tk()
    app = ProxyApp(root)
    root.mainloop()
    
def main():
    flask_thread = threading.Thread(target=start_flask_server)
    flask_thread.daemon = True
    flask_thread.start()
    
    start_gui()
    
if __name__ == '__main__':
    main()