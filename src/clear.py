import os

def clear(file_path):
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error occurred while deleting {file_path}: {e}")

def clear_multiple(file1, file2, file3, file4, file5, file6):
    clear(file1)
    clear(file2)
    clear(file3)
    clear(file4)
    clear(file5)
    clear(file6)
    
