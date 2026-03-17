import os

def check_empty_madrigal_folders():
    base_dir = os.path.join("data", "choral_wiki_monteverdi")
    
    if not os.path.exists(base_dir):
        print(f"the directory {base_dir} does not exist.")
        return

    empty_folders = []

    # iterate through book folders
    for book_folder in os.listdir(base_dir):
        book_path = os.path.join(base_dir, book_folder)
        
        if os.path.isdir(book_path):
            # iterate through madrigal folders inside the book
            for madrigal_folder in os.listdir(book_path):
                madrigal_path = os.path.join(book_path, madrigal_folder)
                
                if os.path.isdir(madrigal_path):
                    # check if the folder is completely empty
                    if not os.listdir(madrigal_path):
                        empty_folders.append(f"{book_folder}/{madrigal_folder}")

    # print the final count and the names of the folders
    print(f"found {len(empty_folders)} empty folders.")
    print("-" * 30)
    
    for folder in empty_folders:
        print(folder)

if __name__ == "__main__":
    check_empty_madrigal_folders()