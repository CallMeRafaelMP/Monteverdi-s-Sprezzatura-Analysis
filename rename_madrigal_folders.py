import os
import re

def rename_madrigal_folders_exact():
    base_dir = os.path.join("data", "choral_wiki_monteverdi_cleaned")
    
    if not os.path.exists(base_dir):
        print(f"directory {base_dir} does not exist.")
        return

    # strict regular expression matching exactly Monte-number-number
    file_pattern = re.compile(r'Monte-(\d+)-(\d+)')

    for book_folder in os.listdir(base_dir):
        book_path = os.path.join(base_dir, book_folder)
        
        if not os.path.isdir(book_path):
            continue
            
        for madrigal_folder in os.listdir(book_path):
            madrigal_path = os.path.join(book_path, madrigal_folder)
            
            if not os.path.isdir(madrigal_path):
                continue
                
            files = os.listdir(madrigal_path)
            book_num = None
            madrigal_num = None
            
            # inspect files to find the exact numbering pattern
            for file_name in files:
                match = file_pattern.search(file_name)
                if match:
                    book_num = match.group(1)
                    # pad with zero to ensure two digits
                    madrigal_num = match.group(2).zfill(2)
                    break
            
            if book_num and madrigal_num:
                new_folder_name = f"{book_num}-{madrigal_num}-{madrigal_folder}"
                new_madrigal_path = os.path.join(book_path, new_folder_name)
                
                # rename the folder if the new name is different
                if madrigal_path != new_madrigal_path:
                    try:
                        os.rename(madrigal_path, new_madrigal_path)
                        print(f"renamed: {madrigal_folder} -> {new_folder_name}")
                    except Exception as e:
                        print(f"error renaming {madrigal_folder}: {e}")
            else:
                print(f"no matching file pattern found in folder: {madrigal_folder}")

if __name__ == "__main__":
    rename_madrigal_folders_exact()