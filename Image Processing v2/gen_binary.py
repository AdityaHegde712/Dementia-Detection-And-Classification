import os
import shutil

# Define the source and destination directories
source_dir = "Multiclass_Data"
destination_dir = "Binary_Data"

# Map the source subfolder names to their corresponding destination subfolder names
subfolder_mapping = {
    "Mild dementia": "Demented",
    "Moderate Dementia": "Demented",
    "Severe Dementia": "Demented",
    "Non Dementia": "NonDemented"
}

# Iterate through the source subfolders in Multiclass_Data
for source_subfolder, destination_subfolder in subfolder_mapping.items():
    source_subfolder_path = os.path.join(source_dir, source_subfolder)
    destination_subfolder_path = os.path.join(destination_dir, destination_subfolder)

    # Create the destination subfolder if it doesn't exist
    os.makedirs(destination_subfolder_path, exist_ok=True)

    # Move files from source to destination while renaming them
    for root, _, files in os.walk(source_subfolder_path):
        for file in files:
            source_file_path = os.path.join(root, file)
            destination_file_path = os.path.join(destination_subfolder_path, file)

            # # Check if the file already exists in the destination
            # if os.path.exists(destination_file_path):
            #     # If it does, add a prefix to avoid overwriting
            #     filename, file_extension = os.path.splitext(file)
            #     counter = 1
            #     while os.path.exists(destination_file_path):
            #         new_filename = f"{filename}_{counter}{file_extension}"
            #         destination_file_path = os.path.join(destination_subfolder_path, new_filename)
            #         counter += 1

            shutil.copy(source_file_path, destination_file_path)
    print(f"Finished {source_subfolder_path}")

print("File transfer complete.")
