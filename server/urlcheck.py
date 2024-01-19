import requests
import os
import time
from urlextract import URLExtract


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


def isMaliciousUrlPresent(prompt):
    local_file_path = "url_list.txt"
    url = "https://urlhaus.abuse.ch/downloads/text_online/"
    db_status = download_and_check_url_file(url, local_file_path)
    inp_urls = URLExtract().find_urls(prompt)

    if db_status:
        # Read the contents of the file and store URLs in a list
        with open(local_file_path, "r") as file:
            url_list = file.read().strip().split('\n')

        for u in inp_urls:
            # Test the search_url function
            result = search_url(url_list, u)

            if result:
                print(f"URL '{u}' is MALWARE")
                return True
            else:
                print(f"URL '{u}' not found in the list.")
                return False
    else:
        print("Failed to download the abuse file or use the local copy.")
        return False


def getPromptFromPayload(headerAuthority, payloadDict):
    """
    Get the prompt message from the payload
    :param headerAuthority:  The authority header value
    :param payloadDict: The payload dictionary

    :return:
    """
    if headerAuthority == "api.openai.com":
        return payloadDict["body"]["messages"][0]["content"]
    elif headerAuthority == "kosha-genai.openai.azure.com":
        return payloadDict["body"]["messages"][0]["content"]
    elif headerAuthority == "vowel-unified-plugins.int.dev.eticloud.io":
        return payloadDict["body"]["raw_prompt"]

    return ""