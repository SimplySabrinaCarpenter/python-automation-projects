import time
import pandas as pd
import sqlite3
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
# The folder this script will monitor for new CSV files
FOLDER_TO_WATCH = Path("./csv_to_process")

# The SQLite database file where data will be stored
DATABASE_FILE = "analytics_database.db"

# The name of the table to which the data will be appended
TABLE_NAME = "sales_data"
# ---------------------

def process_csv(csv_path: Path):
    """
    Reads a CSV file using Pandas and appends its data to an SQLite database table.
    After processing, it moves the file to a 'processed' subdirectory.
    """
    try:
        print(f"⚙️ Processing new file: {csv_path.name}")
        df = pd.read_csv(csv_path)
        
        # Ensure the dataframe is not empty
        if df.empty:
            print(f"WARNING: The file '{csv_path.name}' is empty. Skipping.")
            return

        # Connect to the SQLite database (it will be created if it doesn't exist)
        with sqlite3.connect(DATABASE_FILE) as conn:
            # Use 'if_exists="append"' to add data to the table if it already exists
            # The table will be created from the first CSV's structure
            df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
        
        print(f"✅ Data from '{csv_path.name}' successfully loaded into table '{TABLE_NAME}'.")
        
        # Move the processed file to a subfolder to avoid reprocessing
        processed_dir = FOLDER_TO_WATCH / "processed"
        processed_dir.mkdir(exist_ok=True)
        csv_path.rename(processed_dir / csv_path.name)
        print(f"Moved '{csv_path.name}' to the processed folder.")

    except pd.errors.EmptyDataError:
        print(f"WARNING: The file '{csv_path.name}' is empty or malformed. Skipping.")
    except Exception as e:
        print(f"An error occurred while processing '{csv_path.name}': {e}")


class CSVHandler(FileSystemEventHandler):
    """
    An event handler that reacts to file system events.
    We are only interested in the 'on_created' event for new CSV files.
    """
    def on_created(self, event):
        # Ignore directory creation events
        if event.is_directory:
            return

        # Check if the created file is a CSV
        if event.src_path.endswith('.csv'):
            file_path = Path(event.src_path)
            # Give the system a moment to finish writing the file before processing
            time.sleep(1) 
            process_csv(file_path)

if __name__ == "__main__":
    # Ensure the folder to be watched exists
    FOLDER_TO_WATCH.mkdir(exist_ok=True)
    
    print(f"Starting data pipeline. Watching folder: '{FOLDER_TO_WATCH.resolve()}'")
    print("Drop new CSV files into this folder to have them automatically processed.")
    print("Press Ctrl+C to stop.")
    
    event_handler = CSVHandler()
    observer = Observer()
    # Schedule the handler to watch the specified folder (not recursively)
    observer.schedule(event_handler, str(FOLDER_TO_WATCH), recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping the data pipeline observer.")
        observer.stop()
    
    observer.join()
    print("Pipeline has been shut down.")
