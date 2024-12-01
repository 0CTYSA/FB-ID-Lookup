import re
import os


def process_facebook_urls(file_input, file_output, file_invalid):
    def read_urls(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def write_urls(file_path, urls):
        with open(file_path, 'w') as file:
            if urls:
                file.write("\n".join(urls) + "\n")

    def extract_user_id(url, pattern):
        match = re.search(pattern, url)
        return match.group(1) if match else None

    if not os.path.exists(file_input):
        print(
            f"The file '{file_input}' does not exist or is not in the specified path. Process stopped.")
        return

    if os.stat(file_input).st_size == 0:
        print(f"The file '{file_input}' is empty. Process stopped.")
        return

    urls = read_urls(file_input)
    if not urls:
        print(
            f"The file '{file_input}' does not contain valid URLs. Process stopped.")
        return

    formatted_urls = []
    group_urls = []
    non_compliant_urls = []
    non_facebook_urls = []

    for url in urls:
        if "facebook.com" not in url:
            non_facebook_urls.append(url)
            continue

        if "/groups/" in url:
            group_urls.append(url)
        elif "/people/" in url:
            user_id = extract_user_id(url, r'/people/.+/(\d+)/')
            if user_id:
                formatted_urls.append(
                    f"https://www.facebook.com/profile.php?id={user_id}")
            else:
                non_compliant_urls.append(url)
        else:
            user_id = extract_user_id(url, r'(\d+)')
            if user_id:
                formatted_urls.append(
                    f"https://www.facebook.com/profile.php?id={user_id}")
            else:
                non_compliant_urls.append(url)

    write_urls(file_output, formatted_urls + group_urls)
    write_urls(file_invalid, non_compliant_urls)

    if non_facebook_urls:
        print("\nThe following URLs do not belong to Facebook and were not processed:")
        for url in non_facebook_urls:
            print(url)

    print(
        f"\nProcess complete. Results saved in:\n - {file_output}\n - {file_invalid}")


# Files
file_input = "Data/URLInt.txt"
file_output = "Data/URLFinal.txt"
file_invalid = "Data/NoCumplen.txt"

# Process the URLs
process_facebook_urls(file_input, file_output, file_invalid)
