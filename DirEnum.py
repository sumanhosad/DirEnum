import requests
import concurrent.futures
import sys

stop_execution = False

def check_directory(url, directory):
    """Check if the directory exists on the given URL."""
    global stop_execution
    if stop_execution:
        return
    full_url = url.rstrip('/') + '/' + directory.strip()
    response = requests.get(full_url)
    if response.status_code == 200:
        print(f'[+] {full_url}')
    elif response.status_code == 403:
        print(f'[!] Forbidden access: {full_url}')
    elif response.status_code == 404:
        pass

def enumerate_directory(url):
    """Enumerate directories on the given URL using the provided wordlist."""
    global stop_execution
    try:
        with open('direnumwordlist.txt', 'r') as file:
            directories = file.readlines()
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                # Submit tasks to the ThreadPoolExecutor
                futures = {executor.submit(check_directory, url, directory): directory for directory in directories}
                # Wait for all tasks to complete
                for future in concurrent.futures.as_completed(futures):
                    future.result()
                    if stop_execution:
                        sys.exit()
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

