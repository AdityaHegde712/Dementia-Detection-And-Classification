import os

# Define the root directory where your folders are located
root_directory = "Image Processing v2\Multiclass_Data"

# Initialize a counter
counter = 1

# Iterate through the subdirectories within the root directory
for subdirectory in os.listdir(root_directory):
    subdirectory_path = os.path.join(root_directory, subdirectory)

    # Check if the item in the root directory is a directory
    if os.path.isdir(subdirectory_path):
        # Get a list of image files in the subdirectory
        image_files = [f for f in os.listdir(subdirectory_path) if os.path.isfile(os.path.join(subdirectory_path, f))]

        # Iterate through the image files and rename them
        for filename in image_files:
            # Get the file extension
            file_extension = os.path.splitext(filename)[-1]

            # Define the new filename
            new_filename = "a" + str(counter) + file_extension

            # Build the full paths to the original and new files
            original_file_path = os.path.join(subdirectory_path, filename)
            new_file_path = os.path.join(subdirectory_path, new_filename)

            # Rename the file
            os.rename(original_file_path, new_file_path)

            # Increment the counter for the next file
            counter += 1
    print(f"Completed {subdirectory}")

print("File renaming complete.")
