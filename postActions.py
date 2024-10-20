import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")

df = pd.read_excel('data.xlsx')
df['Title']=df['Title'].apply(lambda x: x+'.mp4')

def ensure_mp4_extension(source_folder):
    # Iterate over all files in the source folder
    for file in os.listdir(source_folder):
        # Check if the file doesn't already have a .mp4 extension
        if not file.lower().endswith('.mp4'):
            # Construct the old and new file paths
            old_file_path = os.path.join(source_folder, file)
            new_file_path = os.path.join(source_folder, file + '.mp4')
            
            # Rename the file to add the .mp4 extension
            os.rename(old_file_path, new_file_path)
            print(f"Renamed: {old_file_path} to {new_file_path}")

def check_missed_downloads(source_folder, file_list):
    # Get the list of files in the source folder
    files_in_folder = os.listdir(source_folder)
    
    # Find files in the list that are not in the folder
    missed_files = [file for file in file_list if file not in files_in_folder]
    
    # Optionally, you can also find files in the folder not in the list
    extra_files = [file for file in files_in_folder if file not in file_list]
    
    # Print the results
    print("Files missing from the folder:")
    for file in missed_files:
        print(file)
    print("\nExtra files in the folder:")
    for file in extra_files:
        print(file)
    
    # Return missed files for further processing if needed
    return missed_files, extra_files

# Example usage
# ensure_mp4_extension(DOWNLOAD_DIR)
check_missed_downloads(DOWNLOAD_DIR, list(df['Title']))