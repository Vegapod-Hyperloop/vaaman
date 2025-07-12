import os
import datetime

def create_log_file():
    if not os.path.exists('logs/main.log.txt'):
        with open('logs/main.log.txt', 'w') as f:
            f.write('')

def main_log(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    with open('main.log.txt', 'a') as f:
        f.write(f"[{timestamp}] {message}\n")

def read_log_file():
    with open('/logs/main.log.txt', 'r') as f:
        return f.read()

def add_to_log(message, host):
    try:
        # Ensure the main log file exists
        create_log_file()

        # Create timestamp for the message
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        # Create or append to host-specific log file (e.g., host.txt)
        host_file = f"logs/{host}.txt"
        if not os.path.exists(host_file):
            with open(host_file, 'w') as f:
                f.write('')

        # Append message to host-specific log file
        with open(host_file, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")

        # Append message to main log file with host information
        main_log(f"[{host}] {message}")

    except (IOError, OSError) as e:
        # Log error to main log file to avoid silent failures
        main_log(f"Error logging for host {host}: {str(e)}")

