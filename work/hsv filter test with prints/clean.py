import os
import threading
import time

def clean_folder(folder_path):
    while True:
        # Get the list of items in the folder
        items = os.listdir(folder_path)
        
        # Sort the items by their modification time (oldest first)
        items.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
        
        # Calculate the number of items to keep (last 3)
        num_items_to_keep = max(0, len(items) - 3)
        
        # Clean the excess items in the folder
        for i in range(num_items_to_keep):
            item_path = os.path.join(folder_path, items[i])
            # Perform the desired cleaning operation, e.g., delete the item
            os.remove(item_path)
        
        # Wait for 5 seconds before cleaning again
        time.sleep(5)

# Example usage
script_path = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(script_path, 'images')

# Create a separate thread for cleaning the folder
cleaning_thread = threading.Thread(target=clean_folder, args=(folder_path,))
cleaning_thread.start()
