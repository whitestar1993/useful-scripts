import os
import re
import sys
import requests
from bs4 import BeautifulSoup

def download_mp3s(html_file, download_folder):
    try:
        print(f"Reading HTML file: {html_file}")
        # Read the HTML file
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Parse the HTML content
        print("Parsing HTML content...")
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the link inside the noscript tag
        noscript = soup.find('noscript')
        if not noscript:
            print("No <noscript> tag found in the HTML file.")
            return
        iframe = noscript.find('iframe')
        if not iframe:
            print("No <iframe> tag found within the <noscript> tag.")
            return
        link = iframe.get('src')
        if not link:
            print("No 'src' attribute found in the <iframe> tag.")
            return
        
        print(f"Found link: {link}")
        
        # Fetch the content of the link
        print(f"Fetching content from: {link}")
        response = requests.get(link)
        if response.status_code != 200:
            print(f"Error fetching the link content: HTTP {response.status_code}")
            return
        
        # Search for MP3 links directly in the text
        print("Searching for MP3 links in the fetched content...")
        mp3_links = re.findall(r'https?://[^\s]+\.mp3', response.text)
        
        print(f"MP3 links found: {len(mp3_links)}")
        
        if not mp3_links:
            print("No mp3 links found.")
            return
        
        # Create the download folder if it doesn't exist
        if not os.path.exists(download_folder):
            print(f"Creating download folder: {download_folder}")
            os.makedirs(download_folder)
        
        # Download each mp3 file
        for mp3_url in mp3_links:
            mp3_name = os.path.basename(mp3_url)
            mp3_path = os.path.join(download_folder, mp3_name)
            
            print(f"Downloading {mp3_url}...")
            
            response = requests.get(mp3_url)
            if response.status_code == 200:
                with open(mp3_path, 'wb') as mp3_file:
                    mp3_file.write(response.content)
                print(f"{mp3_name} downloaded successfully!")
            else:
                print(f"Failed to download {mp3_name}: HTTP {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <html_file> <download_folder>")
    else:
        html_file = sys.argv[1]
        download_folder = sys.argv[2]
        download_mp3s(html_file, download_folder)
