import re
import os


def process_facebook_urls(file_input, file_output, file_invalid):
    # Check if the input file does not exist
    if not os.path.exists(file_input):
        print(
            f"The file '{file_input}' does not exist or is not in the specified path. Process stopped.")
        return

    # Check if the input file is empty
    if os.stat(file_input).st_size == 0:
        print(f"The file '{file_input}' is empty. Process stopped.")
        return

    # Read URLs from the input file
    with open(file_input, 'r') as infile:
        urls = [line.strip() for line in infile.readlines()]

    if not urls:
        print(
            f"The file '{file_input}' does not contain valid URLs. Process stopped.")
        return

    # Variables to store results
    formatted_urls = []
    group_urls = []
    non_compliant_urls = []
    non_facebook_urls = []

    for url in urls:
        # Check that the URL belongs to the Facebook domain
        if "facebook.com" not in url:
            non_facebook_urls.append(url)
            continue

        # Identify if it is a group
        if "/groups/" in url:
            group_urls.append(url)
        # Identify if it is a mobile profile (/people/)
        elif "/people/" in url:
            match_id = re.search(r'/people/.+/(\d+)/', url)
            if match_id:
                user_id = match_id.group(1)
                formatted_urls.append(
                    f"https://www.facebook.com/profile.php?id={user_id}")
            else:
                non_compliant_urls.append(url)
        else:
            # Search for standard numeric ID in other URLs
            match_id = re.search(r'(\d+)', url)
            if match_id:
                user_id = match_id.group(1)
                formatted_urls.append(
                    f"https://www.facebook.com/profile.php?id={user_id}")
            else:
                non_compliant_urls.append(url)

    # Save the converted URLs in the output file
    with open(file_output, 'w') as outfile:
        if formatted_urls or group_urls:
            outfile.write("\n".join(formatted_urls + group_urls) + "\n")

    # Save the invalid URLs in the non-compliant file
    with open(file_invalid, 'w') as invalidfile:
        if non_compliant_urls:
            invalidfile.write("\n".join(non_compliant_urls) + "\n")

    # Display final messages
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
