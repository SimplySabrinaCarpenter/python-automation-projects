from pathlib import Path
import shutil

# --- CONFIGURATION ---
# The folder to organize. Path.home() gets your user's home directory.
# Example: C:\Users\YourUser\Downloads or /home/youruser/Downloads
FOLDER_TO_ORGANIZE = Path.home() / "Downloads"

# Mapping of file extensions to their destination folder names.
# You can easily add or change categories here.
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".bmp", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".txt", ".md"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv"],
    "Music": [".mp3", ".wav", ".aac", ".flac"],
    "Compressed": [".zip", ".rar", ".gz", ".tar", ".7z"],
    "Executables": [".exe", ".msi", ".dmg", ".pkg"]
}
# ---------------------

def organize_folder(path: Path):
    """
    Organizes all files in the specified path into subdirectories based on CATEGORIES.
    """
    if not path.is_dir():
        print(f"Error: The path '{path}' is not a valid directory.")
        return

    print(f"Starting to organize files in: {path}")

    # Iterate over all files in the specified directory
    for item in path.iterdir():
        # We only want to process files, not subdirectories
        if item.is_file():
            destination_category = "Other" # Default category
            
            # Check which category the file belongs to
            for category, extensions in CATEGORIES.items():
                if item.suffix.lower() in extensions:
                    destination_category = category
                    break
            
            # Create the destination folder if it doesn't already exist
            destination_folder = path / destination_category
            destination_folder.mkdir(exist_ok=True)
            
            # Move the file to its new home
            try:
                print(f"Moving '{item.name}' to '{destination_category}'...")
                shutil.move(str(item), str(destination_folder))
            except Exception as e:
                print(f"Could not move '{item.name}'. Error: {e}")

if __name__ == "__main__":
    organize_folder(FOLDER_TO_ORGANIZE)
    print("\n✅ Organization complete.")
