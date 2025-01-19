import os
import re
import requests
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox
from bs4 import BeautifulSoup

def download_mp3s(web_address, download_folder):
    try:
        print(f"Fetching HTML content from: {web_address}")
        # Fetch the HTML content
        response = requests.get(web_address)
        if response.status_code != 200:
            print(f"Error fetching the HTML content: HTTP {response.status_code}")
            messagebox.showerror("Error", f"Error fetching the HTML content: HTTP {response.status_code}")
            return
        html_content = response.text
        
        # Parse the HTML content
        print("Parsing HTML content...")
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the link inside the noscript tag
        noscript = soup.find('noscript')
        if not noscript:
            print("No <noscript> tag found in the HTML content.")
            messagebox.showerror("Error", "No <noscript> tag found in the HTML content.")
            return
        iframe = noscript.find('iframe')
        if not iframe:
            print("No <iframe> tag found within the <noscript> tag.")
            messagebox.showerror("Error", "No <iframe> tag found within the <noscript> tag.")
            return
        link = iframe.get('src')
        if not link:
            print("No 'src' attribute found in the <iframe> tag.")
            messagebox.showerror("Error", "No 'src' attribute found in the <iframe> tag.")
            return
        
        print(f"Found link: {link}")
        
        # Fetch the content of the link
        print(f"Fetching content from: {link}")
        response = requests.get(link)
        if response.status_code != 200:
            print(f"Error fetching the link content: HTTP {response.status_code}")
            messagebox.showerror("Error", f"Error fetching the link content: HTTP {response.status_code}")
            return
        
        # Search for MP3 links directly in the text
        print("Searching for MP3 links in the fetched content...")
        mp3_links = re.findall(r'https?://[^\s]+\.mp3', response.text)
        
        print(f"MP3 links found: {len(mp3_links)}")
        
        if not mp3_links:
            print("No mp3 links found.")
            messagebox.showinfo("Info", "No MP3 links found.")
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

        messagebox.showinfo("Success", "MP3 files downloaded successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

def browse_folder():
    foldername = filedialog.askdirectory()
    if foldername:
        folder_entry.delete(0, 'end')
        folder_entry.insert(0, foldername)

def start_download():
    web_address = web_entry.get()
    download_folder = folder_entry.get()
    if not web_address or not download_folder:
        messagebox.showerror("Error", "Please enter both the web address and download folder.")
        return
    download_mp3s(web_address, download_folder)

# Create the main window
root = Tk()
root.title("MP3 Downloader")

# Create and place the widgets
Label(root, text="Web Address:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
web_entry = Entry(root, width=50)
web_entry.grid(row=0, column=1, padx=5, pady=5)

Label(root, text="Download Folder:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
folder_entry = Entry(root, width=50)
folder_entry.grid(row=1, column=1, padx=5, pady=5)
Button(root, text="Browse...", command=browse_folder).grid(row=1, column=2, padx=5, pady=5)

Button(root, text="Start Download", command=start_download).grid(row=2, column=0, columnspan=3, padx=5, pady=10)

# Run the main loop
root.mainloop()
