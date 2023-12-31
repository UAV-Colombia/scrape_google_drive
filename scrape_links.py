import csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import html


def extract_links_from_html(html_content):
    pattern = r"https://lh3.googleusercontent.com/[^\s]+"
    links = re.findall(pattern, html_content)
    if links:
        link = links[0]
        link = html.unescape(link)
        link = link.split("\\u003d")[0]  # Remove trailing '\\u003ds1600' or similar
        return link
    return None


def process_links(input_file, output_file):
    extracted_links = []  # Use a list to store links in order
    extracted_links_set = set()  # Use a set to track unique links
    with open(input_file, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in tqdm(reader, desc="Processing links", unit=" links"):
            google_drive_link = row[0].strip()
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
    input_file = "arg_file_links.csv"
    output_file = "central_termoelectrica.csv"
    process_links(input_file, output_file)


if __name__ == "__main__":
    main()
