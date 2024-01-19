import requests
import os
import time


# Define a function to search for a URL in the list
def search_url(url_list, url):
    for stored_url in url_list:
        if url == stored_url:
            return True
    return False


# Define a function to download the file and check if it's still valid
def download_and_check_url_file(url, local_file_path):
    if os.path.exists(local_file_path):
        # Check if the file is older than 1 day
        file_age = time.time() - os.path.getmtime(local_file_path)
        if file_age < 86400:
            return True  # File is still valid, use the local copy

    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_file_path, "w") as f:
                f.write(response.text)
            return True
    except requests.exceptions.RequestException:
        pass  # Ignore any errors when downloading

    if os.path.exists(local_file_path):
        # Use the local copy as a fallback if available
        return True

    return False


def run():
    local_file_path = "url_list.txt"
    url = "https://urlhaus.abuse.ch/downloads/text_online/"

    if download_and_check_url_file(url, local_file_path):
        # Read the contents of the file and store URLs in a list
        with open(local_file_path, "r") as file:
            url_list = file.read().strip().split('\n')

        # Sample URL to search for
        test_urls = ["http://example.com", "http://113.27.8.90:31926/.i"]

        for u in test_urls:
            # Test the search_url function
            result = search_url(url_list, u)

            if result:
                print(f"URL '{u}' is MALWARE")
            else:
                print(f"URL '{u}' not found in the list.")
    else:
        print("Failed to download the abuse file or use the local copy.")


# Call the run function to execute the code
if __name__ == "__main__":
    run()
