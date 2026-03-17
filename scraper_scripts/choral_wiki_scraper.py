import os
import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def setup_directories(base_path):
    # creates the main directory if it does not exist
    os.makedirs(base_path, exist_ok=True)

def create_session():
    # setup a session with automatic retries for server errors
    session = requests.Session()
    # increased total retries and backoff factor to give the server more time to recover
    retry_strategy = Retry(
        total=10, 
        backoff_factor=3, 
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    return session

def get_soup(url, session):
    # fetches a web page using the robust session and returns a beautifulsoup object
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def download_file(url, folder_path, session):
    # downloads a file from a url into the specified folder using the robust session
    try:
        file_name = unquote(url.split('/')[-1])
        file_path = os.path.join(folder_path, file_name)
        
        # skip download if the file is already in the folder
        if os.path.exists(file_path):
            print(f"    file {file_name} already exists, skipping")
            return

        response = session.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except Exception as e:
        print(f"    could not download {url}: {e}")

def scrape_monteverdi():
    base_url = "https://www.cpdl.org"
    main_page_url = "https://www.cpdl.org/wiki/index.php/Claudio_Monteverdi"
    output_dir = os.path.join("data", "choral_wiki_monteverdi")
    
    setup_directories(output_dir)
    session = create_session()
    
    print("fetching main page...")
    try:
        soup = get_soup(main_page_url, session)
    except Exception as e:
        print(f"failed to load main page: {e}")
        return
    
    # find all headings that contain book information
    book_keywords = ["libro de madrigali", "libro di madrigali", "libro nono"]
    headings = soup.find_all(['h3', 'h2'])
    
    book_counter = 1
    
    for heading in headings:
        heading_text = heading.get_text().lower()
        
        if any(keyword in heading_text for keyword in book_keywords) and book_counter <= 9:
            book_folder_name = f"Book_{book_counter}"
            book_path = os.path.join(output_dir, book_folder_name)
            setup_directories(book_path)
            
            print(f"scraping {book_folder_name}...")
            
            # the list of madrigals is usually in the next ordered list tag
            ol_tag = heading.find_next_sibling('ol')
            if not ol_tag:
                continue
                
            madrigal_links = ol_tag.find_all('a')
            
            for link in madrigal_links:
                madrigal_title = link.get_text().strip().replace('/', '_').replace(':', '')
                madrigal_url = urljoin(base_url, link.get('href'))
                madrigal_path = os.path.join(book_path, madrigal_title)
                
                setup_directories(madrigal_path)
                
                # check if metadata already exists as a sign of successful past scrape
                metadata_path = os.path.join(madrigal_path, "metadata.json")
                if os.path.exists(metadata_path):
                    print(f"  skipping {madrigal_title}, metadata already exists")
                    # still check files just in case the scrape was interrupted during file download
                    scrape_madrigal_files_only(madrigal_url, madrigal_path, session)
                else:
                    scrape_madrigal_page(madrigal_url, madrigal_path, session)
                
                # increased pause to respect server rate limits and avoid 502s
                time.sleep(3)
                
            book_counter += 1

def scrape_madrigal_page(url, save_path, session):
    # scrapes individual madrigal pages for files, metadata, and text
    print(f"  processing {os.path.basename(save_path)}...")
    try:
        soup = get_soup(url, session)
    except Exception as e:
        print(f"  failed to load {url} after retries: {e}")
        return

    # extract metadata
    metadata = {}
    info_heading = soup.find(id="General_Information")
    if info_heading:
        info_section = info_heading.parent
        for sibling in info_section.find_next_siblings():
            if sibling.name in ['h2', 'h3']:
                break
            if sibling.name == 'p':
                bold_tags = sibling.find_all('b')
                for b in bold_tags:
                    key = b.get_text().strip().strip(':')
                    value = b.next_sibling
                    if value and isinstance(value, str):
                        metadata[key] = value.strip()
                    elif value and value.name == 'a':
                        metadata[key] = value.get_text().strip()
                        
        with open(os.path.join(save_path, "metadata.json"), 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4)

    # extract texts and translations
    poems = soup.find_all('div', class_='poem')
    if poems:
        with open(os.path.join(save_path, "text.txt"), 'w', encoding='utf-8') as f:
            for poem in poems:
                f.write(poem.get_text().strip() + "\n\n")

    # extract and download files
    extract_and_download_files(soup, save_path, session)

def scrape_madrigal_files_only(url, save_path, session):
    # quick pass to check if any files were missed during a previous scrape
    try:
        soup = get_soup(url, session)
        extract_and_download_files(soup, save_path, session)
    except Exception:
        pass

def extract_and_download_files(soup, save_path, session):
    # helper function to find file links and trigger the download
    file_links = soup.find_all('a', class_='internal')
    for file_link in file_links:
        href = file_link.get('href')
        if href:
            full_file_url = urljoin("https://www.cpdl.org", href)
            # filter for relevant file types
            if any(ext in full_file_url.lower() for ext in ['.pdf', '.mid', '.midi', '.mxl', '.xml', '.mp3', '.zip']):
                download_file(full_file_url, save_path, session)

if __name__ == "__main__":
    scrape_monteverdi()