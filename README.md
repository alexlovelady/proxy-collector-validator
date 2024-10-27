# Proxy Collector and Validator

This project is a standalone Python application that collects, validates, and exports proxies. It provides a GUI interface built with Tkinter, a backend powered by Flask, and a validation function that checks proxy status.

## Features
- **Collect Proxies** from online sources
- **Validate Proxies** individually or in bulk
- **Export Valid Proxies** to a CSV file
- Progress tracking with a progress bar

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/alexlovelady/proxy-collector-validator.git
   cd proxy-collector-validator
   ```

2. **Install the requirements**:

   ```bash
   pip install -r requirements.txt```
   ```

## Usage
1. **Start the application**: Run this command.

   ```bash
   python main.py
   ```

**File Structure**
- app.py - Flask server for collecting and validating proxies.
- gui.py - GUI application built with Tkinter.
- main.py - Main entry point for the application.
- proxy_gatherer.py - Functions to fetch proxies from online sources.
- proxy_validator.py - Functions to validate proxies.
- proxies.json - JSON file where collected proxies are stored.
- valid_proxies.json - JSON file where valid proxies are saved.
- valid_proxies.csv - CSV file containing the exported valid proxies.
- Requirements.txt - List of Python packages required for the project.

**Requirements**
- Python 3.x
- Flask
- Tkinter
- Requests
- BeautifulSoup4

## License
This project is licensed under the MIT License.