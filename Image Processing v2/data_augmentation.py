# from keras.preprocessing import image
# from keras.preprocessing.image import ImageDataGenerator
# import os
# import numpy as np

# def load_and_preprocess_image(image_path):
#     try:
#         img = image.load_img(image_path, target_size=(224, 224))
#         img = image.img_to_array(img)
#         img = np.expand_dims(img, axis=0)
#         img = img / 255.0
#     except Exception as e:
#         print(f"Error processing image {image_path}: {e}")
#         return None

#     return img

# # Define the data augmentation parameters
# datagen = ImageDataGenerator(
#     rotation_range=50,
#     zoom_range=0.2,
#     horizontal_flip=True,
#     vertical_flip=True,
#     fill_mode='nearest'
# )

# # Specify the source directory (NonDemented) and a directory to save the augmented images
# source_directory = "Image Processing v2\Binary_Data\Demented"
# destination_directory = "Image Processing v2\Binary_Data\Demented_Augmented"

# # Create the destination directory if it doesn't exist
# if not os.path.exists(destination_directory):
#     os.makedirs(destination_directory)

# # Get a list of image files in the source directory
# image_files = [f for f in os.listdir(source_directory) if os.path.isfile(os.path.join(source_directory, f))]

# # Number of augmented images to generate for each original image
# augmentation_factor = 10  # You can adjust this as needed

# # Apply data augmentation to each image in the source directory
# for filename in image_files:
#     img = load_and_preprocess_image(os.path.join(source_directory, filename))
#     if img is not None:
#         i = 0
#         for _ in datagen.flow(img, save_to_dir=destination_directory, save_prefix='aug', save_format='jpg'):
#             i += 1
#             if i >= augmentation_factor:
#                 break  # Break the loop after generating the desired number of augmented images

# print("Data augmentation complete.")


import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
import os

# Define your directories
demented_dir = './Image Processing v2/Binary_Data/Demented'
nondemented_dir = './Image Processing v2/Binary_Data/NonDemented'

# Define your output directories
alt_demented_dir = './Image Processing v2/Binary_Data/altDemented'
alt_nondemented_dir = './Image Processing v2/Binary_Data/altNonDemented'

# Create the output directories if they don't exist
os.makedirs(alt_demented_dir, exist_ok=True)
os.makedirs(alt_nondemented_dir, exist_ok=True)

print("Made the directories")

# Create an ImageDataGenerator instance for the 'Demented' class with data augmentation
datagen_demented = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    fill_mode='nearest'
)

print("Created the ImageDataGenerator")

# Load and iterate training datasets for 'Demented'
demented_data = datagen_demented.flow_from_directory(demented_dir, class_mode='binary', batch_size=20, save_to_dir=alt_demented_dir, save_prefix='aug', save_format='jpg')
print("Completed demented data")
# Create an ImageDataGenerator instance for the 'NonDemented' class without data augmentation
datagen_nondemented = ImageDataGenerator(rescale=1./255)

# Load and iterate training datasets for 'NonDemented'
nondemented_data = datagen_nondemented.flow_from_directory(nondemented_dir, class_mode='binary', batch_size=20, save_to_dir=alt_nondemented_dir, save_prefix='aug', save_format='jpg')
print("Completed nonDemented data")
# Generate 3 augmented images for each original image
num_aug_images_wanted = 3  

# Find how many multiple of the batch size is needed to get the desired number of augmented images
num_files_demented = len(demented_data.filenames)
num_files_nondemented = len(nondemented_data.filenames)

num_batches_to_process_demented = int(num_aug_images_wanted / num_files_demented)
num_batches_to_process_nondemented = int(num_aug_images_wanted / num_files_nondemented)

# augment the images and save them to the new directory
for i in range(num_batches_to_process_demented):
    imgs, labels = next(demented_data)
print("Completed full demented data")

for i in range(num_batches_to_process_nondemented):
    imgs, labels = next(nondemented_data)
print("Completed full nonDemented data")
