import os

def check_madrigal_files():
    base_dir = os.path.join("data", "choral_wiki_monteverdi_cleaned")
    
    if not os.path.exists(base_dir):
        print(f"directory {base_dir} does not exist. please check the folder name.")
        return

    incomplete_madrigals = []

    # iterate through the book folders
    for book_folder in sorted(os.listdir(base_dir)):
        book_path = os.path.join(base_dir, book_folder)
        
        if os.path.isdir(book_path):
            # iterate through the madrigal folders inside each book
            for madrigal_folder in sorted(os.listdir(book_path)):
                madrigal_path = os.path.join(book_path, madrigal_folder)
                
                if os.path.isdir(madrigal_path):
                    files = os.listdir(madrigal_path)
                    
                    # check for the presence of the three required file types
                    has_pdf = any(f.lower().endswith('.pdf') for f in files)
                    has_mxl = any(f.lower().endswith(('.mxl')) for f in files)
                    has_mid = any(f.lower().endswith(('.mid')) for f in files)
                    
                    if not (has_pdf and has_mxl and has_mid):
                        missing = []
                        if not has_pdf:
                            missing.append('.pdf')
                        if not has_mxl:
                            missing.append('.mxl')
                        if not has_mid:
                            missing.append('.mid')
                            
                        incomplete_madrigals.append(f"{book_folder}/{madrigal_folder} is missing: {', '.join(missing)}")

    # print the results
    if incomplete_madrigals:
        print(f"found {len(incomplete_madrigals)} madrigals with missing files:")
        print("-" * 50)
        for item in incomplete_madrigals:
            print(item)
    else:
        print("all madrigals have the complete triplet of files.")

if __name__ == "__main__":
    check_madrigal_files()