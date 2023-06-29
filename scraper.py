import csv
import requests
import re
import sys
from tqdm import tqdm
import html
import numpy as np


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


def extract_file_links_from_folders(input_file):
    links = []
    with open(input_file, "r") as csv_file:
        reader = csv.reader(csv_file)
        # next(reader)  # Skip header row
        for row in reader:
            folder_link = row[0]
            print(f"Extracting file links from folder: {folder_link}")
            links.append(retrieve_links_from_folder(folder_link))
    links = np.array(links).flatten()
    return links
    # save_links_to_csv(links, output_file)


def extract_links_from_html(html_content):
    pattern = r"https://lh3.googleusercontent.com/[^\s]+"
    links = re.findall(pattern, html_content)
    if links:
        link = links[0]
        link = html.unescape(link)
        link = link.split("\\u003d")[0]  # Remove trailing '\\u003ds1600' or similar
        return link
    return None


def process_links(links, output_file):
    extracted_links = []  # Use a list to store links in order
    extracted_links_set = set()  # Use a set to track unique links
    for google_drive_link in tqdm(links, desc="Processing links", unit=" links"):
        response = requests.get(google_drive_link)
        if response.ok:
            html_content = response.text
            link = extract_links_from_html(html_content)
            if link and link not in extracted_links_set:
                extracted_links.append(link)  # Append the link to the list
                extracted_links_set.add(link)  # Add the link to the set

    with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows([[link] for link in extracted_links])


def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        print(
            "Please provide the input CSV file and the output file path. up to 100 links per folder supported currently."
        )
        return
    input_file = sys.argv[1]  # Replace with the actual input CSV file
    output_file = sys.argv[2]
    links = extract_file_links_from_folders(input_file)
    process_links(links, output_file)


if __name__ == "__main__":
    main()
