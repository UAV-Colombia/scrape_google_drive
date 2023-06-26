import csv
import requests
import re


def retrieve_links_from_folder(google_drive_folder_url):
    response = requests.get(google_drive_folder_url)
    html_content = response.text

    pattern = r"https://drive\.google\.com/file/d/[a-zA-Z0-9_-]+/"
    links = re.findall(pattern, html_content)

    return links


def save_links_to_csv(links, output_file):
    with open(output_file, "a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows([[link] for link in links])


def extract_file_links_from_folders(input_file, output_file):
    with open(input_file, "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip header row
        for row in reader:
            folder_link = row[0]
            print(f"Extracting file links from folder: {folder_link}")
            links = retrieve_links_from_folder(folder_link)
            save_links_to_csv(links, output_file)


def main():
    input_file = "folder_links.csv"  # Replace with the actual input CSV file
    output_file = "file_links.csv"

    # Clear the contents of the output file before extracting new links
    open(output_file, "w").close()

    extract_file_links_from_folders(input_file, output_file)


if __name__ == "__main__":
    main()
