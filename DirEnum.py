import requests
import sys

stop_execution = False

def check_directory(url, directory):
    global stop_execution
    if stop_execution:
        return
    full_url = url.rstrip('/') + '/' + directory.strip()
    try:
        response = requests.get(full_url)
        if response.status_code == 200:
            print(f'[+] {full_url}')
        elif response.status_code == 403:
            print(f'[!] Forbidden access: {full_url}')
        elif response.status_code == 404:
            pass
    except requests.RequestException as e:
        print(f'[-] Request failed for {full_url}: {e}')

def enumerate_directory(url):
    global stop_execution
    try:
        with open('direnumwordlist.txt', 'r') as file:
            directories = file.readlines()
            for directory in directories:
                if stop_execution:
                    sys.exit()
                check_directory(url, directory)
    except FileNotFoundError:
        print(f'Error: Wordlist file "direnumwordlist.txt" not found.')
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt: Exiting the script...")
        sys.exit()
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

if __name__ == '__main__':
    url = input("Enter the URL: ").strip()
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    enumerate_directory(url)

