#!/usr/bin/env python3

import os
import requests
import json
import sys

def download_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print("File downloaded successfully")
    else:
        print("Failed to download file")

def generate_url(command):
    base_url = "https://raw.githubusercontent.com/Quantum-Linux/packages/main/"
    package_json = "/package.json"
    return base_url + command + package_json

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <command>".format(sys.argv[0]))
        sys.exit(1)
    
    command = sys.argv[1]
    
    url = generate_url(command)
    
    response = requests.get(url)

    if response.status_code == 200:

        data = json.loads(response.text)
        

        file_url = data.get("URL")
        if file_url:

            script_dir = os.path.dirname(__file__)

            file_name = os.path.basename(file_url)
            save_path = os.path.join(script_dir, file_name)

            download_file(file_url, save_path)
        else:
            print("File URL not found in package.json")

        if "NOTES" in data:
            print("NOTES:", data["NOTES"])
        else:
            print("NOTES not found in package.json, please contact the maintainer of this repo")
    else:
        print("Failed to fetch package.json from the repository at", url)
