import os
import shutil
import requests
from bs4 import BeautifulSoup

def get_correct_ordering():
    # fetch the main page to extract the original numbered list of madrigals
    url = "https://www.cpdl.org/wiki/index.php/Claudio_Monteverdi"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    ordering = {}
    book_keywords = ["libro de madrigali", "libro di madrigali", "libro nono"]
    headings = soup.find_all(['h3', 'h2'])
    book_counter = 1
    
    for heading in headings:
        heading_text = heading.get_text().lower()
        if any(keyword in heading_text for keyword in book_keywords) and book_counter <= 9:
            book_key = f"Book_{book_counter}"
            ordering[book_key] = []
            
            ol_tag = heading.find_next_sibling('ol')
            if ol_tag:
                for link in ol_tag.find_all('a'):
                    # sanitize the title exactly as it was done in the scraper
                    title = link.get_text().strip().replace('/', '_').replace(':', '')
                    ordering[book_key].append(title)
            book_counter += 1
            
    return ordering

def select_best_files(madrigal_path):
    # groups files by their base name to find a complete triplet and discards duplicates and zips
    files = os.listdir(madrigal_path)
    groups = {}
    
    for f in files:
        if f.endswith('.zip'):
            continue
            
        name, ext = os.path.splitext(f)
        ext = ext.lower()
        
        if ext in ['.pdf', '.mid', '.midi', '.mxl', '.xml']:
            if name not in groups:
                groups[name] = {}
            
            # classify the file by its format type
            if ext in ['.mid', '.midi']:
                groups[name]['midi'] = f
            elif ext in ['.mxl', '.xml']:
                groups[name]['xml'] = f
            elif ext == '.pdf':
                # ignore files containing -bc or _bc to avoid picking basso continuo parts over the full score
                if not f.lower().endswith('-bc.pdf') and not f.lower().endswith('_bc.pdf'):
                    groups[name]['pdf'] = f

    best_group_name = None
    best_score = -1
    
    # evaluate which base name has the most complete set of formats
    for name, exts in groups.items():
        score = len(exts)
        if score > best_score:
            best_score = score
            best_group_name = name
            
    if best_group_name:
        return list(groups[best_group_name].values())
    return []

def preprocess_madrigals():
    base_dir = os.path.join("data", "choral_wiki_monteverdi")
    new_base_dir = os.path.join("data", "preprocessed_choral_wiki_monteverdi")
    
    if not os.path.exists(base_dir):
        print(f"directory {base_dir} not found. please run the scraper first.")
        return

    os.makedirs(new_base_dir, exist_ok=True)
    ordering = get_correct_ordering()
    
    for i in range(1, 10):
        book_folder = f"Book_{i}"
        book_path = os.path.join(base_dir, book_folder)
        
        if not os.path.isdir(book_path):
            continue
            
        os.makedirs(os.path.join(new_base_dir, book_folder), exist_ok=True)
        book_ordering = ordering.get(book_folder, [])
        
        for madrigal_folder in os.listdir(book_path):
            madrigal_path = os.path.join(book_path, madrigal_folder)
            
            if not os.path.isdir(madrigal_path):
                continue
            
            # find the correct index based on the original html list
            try:
                madrigal_index = book_ordering.index(madrigal_folder) + 1
            except ValueError:
                # assign a high number if the folder name somehow does not match the list
                madrigal_index = 99
                
            safe_name = madrigal_folder.replace(' ', '_').replace(',', '')
            new_madrigal_folder_name = f"{i}_{madrigal_index:02d}_{safe_name}"
            new_madrigal_path = os.path.join(new_base_dir, book_folder, new_madrigal_folder_name)
            
            os.makedirs(new_madrigal_path, exist_ok=True)
            
            selected_files = select_best_files(madrigal_path)
            
            # copy only the selected music files
            for file_to_copy in selected_files:
                src = os.path.join(madrigal_path, file_to_copy)
                dst = os.path.join(new_madrigal_path, file_to_copy)
                shutil.copy2(src, dst)
            
            # keep the text and metadata files if they were downloaded
            for extra_file in ['metadata.json', 'text.txt']:
                src = os.path.join(madrigal_path, extra_file)
                if os.path.exists(src):
                    shutil.copy2(src, os.path.join(new_madrigal_path, extra_file))
                
            print(f"processed {madrigal_folder} -> {new_madrigal_folder_name} ({len(selected_files)} music files)")

if __name__ == "__main__":
    preprocess_madrigals()