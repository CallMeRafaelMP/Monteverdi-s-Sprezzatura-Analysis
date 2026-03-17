import os
import re
import unicodedata

def sanitize_name(name):
    # decompose the unicode string and drop the accented characters
    nfd_name = unicodedata.normalize('NFD', name)
    ascii_name = nfd_name.encode('ascii', 'ignore').decode('utf-8')
    
    # remove invalid windows characters
    invalid_chars_pattern = re.compile(r'[<>:"/\\|!?*]')
    safe_name = invalid_chars_pattern.sub('', ascii_name).strip()
    
    return safe_name

def sanitize_all_names():
    target_directories = [
        os.path.join("data", "choral_wiki_monteverdi"),
        os.path.join("data", "choral_wiki_monteverdi_cleaned")
    ]
    
    for base_dir in target_directories:
        if not os.path.exists(base_dir):
            print(f"directory {base_dir} does not exist, skipping.")
            continue
            
        # walking bottom-up so we can safely rename files before their parent folders change names
        for root, dirs, files in os.walk(base_dir, topdown=False):
            
            # check and rename files
            for file_name in files:
                safe_file_name = sanitize_name(file_name)
                
                # only rename if the sanitized name is different from the original
                if safe_file_name != file_name:
                    old_file_path = os.path.join(root, file_name)
                    new_file_path = os.path.join(root, safe_file_name)
                    
                    try:
                        os.rename(old_file_path, new_file_path)
                        print(f"renamed file: '{file_name}' -> '{safe_file_name}'")
                    except Exception as e:
                        print(f"error renaming file '{file_name}': {e}")
            
            # check and rename directories
            for dir_name in dirs:
                safe_dir_name = sanitize_name(dir_name)
                
                # only rename if the sanitized name is different from the original
                if safe_dir_name != dir_name:
                    old_dir_path = os.path.join(root, dir_name)
                    new_dir_path = os.path.join(root, safe_dir_name)
                    
                    try:
                        os.rename(old_dir_path, new_dir_path)
                        print(f"renamed folder: '{dir_name}' -> '{safe_dir_name}'")
                    except Exception as e:
                        print(f"error renaming folder '{dir_name}': {e}")

if __name__ == "__main__":
    sanitize_all_names()