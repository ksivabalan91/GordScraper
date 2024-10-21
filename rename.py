import os, re
import pandas as pd
import urllib.parse
from downloader import loadData
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")
assert DOWNLOAD_DIR,"Error: DOWNLOAD_DIR is not set."

df: pd.DataFrame = loadData("missed_data.xlsx")
# extract original filenames from download link and remove URL encoding
df['filename'] = df['Download Link'].apply(lambda x: x.split("/")[-1])
df['filename'] = df['filename'].apply(lambda x: urllib.parse.unquote(x))
# remove illegal characters for Titles
df['Title'] = df['Title'].apply(lambda x: re.sub(r'[\/:*?"<>|]','_',x))

def delete_duplicates(source_folder) -> None:
    # Regex pattern to match filenames ending with (1), (2), (3), etc., before the file extension
    pattern = re.compile(r".*\(\d+\)\.[a-zA-Z0-9]+$")

    # Combine filtering and mapping into a single generator expression
    files_to_delete = (os.path.join(source_folder, f) for f in os.listdir(source_folder) if pattern.search(f))
    
    # Iterate over the files and delete them
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

def rename_file(source_folder, old_filename, new_filename) -> None:
    # Get the full path of the old and new filenames
    old_file_path = os.path.join(source_folder, old_filename)
    new_file_path = os.path.join(source_folder, new_filename)

    # Append a number to the new filename if it already exists
    if new_filename != old_filename:
        counter = 2
        while os.path.exists(new_file_path):
            # Append the counter to the new filename (before the file extension)
            file_name, file_extension = os.path.splitext(new_filename)
            new_file_path = os.path.join(source_folder, f"{file_name}_{counter}{file_extension}")
            counter += 1

        # Rename the file
        os.rename(old_file_path, new_file_path)
        # print(f'Renamed: {old_file_path} to {new_file_path}')

def start() -> None:
    delete_duplicates(DOWNLOAD_DIR)
    # Iterate over the files in the download directory
    for filename in os.listdir(DOWNLOAD_DIR):
        try:
            dataRow = df.loc[df['filename'] == filename]
            new_filename = str(dataRow['Title'].values[0])+".mp4"
            print(f"Renaming {filename} to {new_filename}")
            rename_file(DOWNLOAD_DIR, filename, new_filename)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    start()
