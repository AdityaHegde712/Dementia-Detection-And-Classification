from sklearn.metrics import PredictionErrorDisplay
import torch
import timm
from torchvision import transforms
from torch.utils.data import DataLoader, Dataset
from torchvision.datasets import ImageFolder
import torch
import os
import shutil
from keras.models import load_model
from sklearn.preprocessing import StandardScaler
import pandas as pd
from tqdm import tqdm
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.applications.mobilenet_v2 import preprocess_input  




def preprocess_csv(csv_file_path):
    sc = StandardScaler()
    df = pd.read_csv(csv_file_path)
    df = df.dropna()
    df.drop(['cdr', 'cdr_id', 'oasis_id'], axis=1, inplace=True)

    print("Preprocessed Dataframe:")
    print(df.head())

    expected_attributes = ['visit_days', 'memory', 'orient', 'judgement', 'community', 'homehobb', 'perscare', 'sumbox']
    expected_attributes_lower = [attr.lower() for attr in expected_attributes]

    if not set(expected_attributes_lower).issubset(map(str.lower, df.columns)):
        print("Error: Attributes do not match.")
        return None
    df = sc.fit_transform(df)
    return df


def model_predict(model, preprocessed_dataframe):
    predictions = model.predict(preprocessed_dataframe)
    return predictions


def predictCSVs():
    csv_file_path = 'C:/Users/hifia/Projects/Dementia Detection and Classification/Front-End/uploads/CSVs/uploaded_file.csv'
    model_path = 'C:/Users/hifia/Projects/Dementia Detection and Classification/Front-End/resources/models/OASIS4_CDR.h5'
    model = load_model(model_path)
    predictions = []

    # Preprocess the CSV file
    preprocessed_dataframe = preprocess_csv(csv_file_path)
    
    if preprocessed_dataframe is not None:
        # Make predictions and append them to the list
        predictions.extend(model_predict(model, preprocessed_dataframe))

        # Process predictions
        f_predictions = []
        # Columns are Entry and Diagnosis.
        
        for i in range(len(predictions)):
            index_of_max = np.argmax(predictions[i])
            entry_no = i+1
            if index_of_max == 1:
                f_predictions.append({'entry': entry_no, 'diag': 'Demented'})
            else:
                f_predictions.append({'entry': entry_no, 'diag': 'Non-Demented'})   
            # f_predictions.append(index_of_max)

        # Delete the opened CSV
        os.remove(csv_file_path)
        # Count number of 'Demented' and 'Non-Demented'
        return f_predictions
    

def getLoader():
    # Define a dummy folder and classes
    Temp = 'Temp'
    os.makedirs(Temp, exist_ok=True)

    # Save the uploaded image in the dummy folder with both class labels
    uploaded_image_path = "C:/Users/hifia/Projects/Dementia Detection and Classification/Front-End/uploads/MRIs/uploaded_image.jpg"
    dummy_image_path_demented = os.path.join(Temp, 'Demented', 'uploaded_image.jpg')
    dummy_image_path_nondemented = os.path.join(Temp, 'NonDemented', 'uploaded_image.jpg')

    # Create subfolders for each class
    os.makedirs(os.path.join(Temp, 'Demented'), exist_ok=True)
    os.makedirs(os.path.join(Temp, 'NonDemented'), exist_ok=True)

    # Copy the uploaded image to both class folders
    shutil.copy(uploaded_image_path, dummy_image_path_demented)
    shutil.copy(dummy_image_path_demented, dummy_image_path_nondemented)

    # Define transformations for image preprocessing
    transform = transforms.Compose([
        transforms.Resize((176, 208)),  # Resize images to a common size (adjust as needed)
        transforms.ToTensor(),           # Convert images to tensors
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),  # Normalize using ImageNet stats
    ])

    # Load training and testing datasets
    test_image = ImageFolder(root=Temp, transform=transform)

    batch_size = 1  # Adjust as needed

    data_loader = DataLoader(test_image, batch_size=batch_size)

    # Delete the image file
    # os.remove(uploaded_image_path)
    return data_loader


def predict() -> str:
    uploaded_loader = getLoader()
    model = timm.create_model('mobilenetv3_large_100', pretrained=True, num_classes=2, drop_rate=0.2).to('cpu')
    model.load_state_dict(torch.load('Front-End\\resources\\models\\new_mobilenetv3_large.pth', map_location=torch.device('cpu')))
    model.eval()
    predicted_class = None
    with torch.no_grad():
        for inputs, _ in uploaded_loader:
            inputs = inputs.to('cpu')
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            predicted_class = 'Demented' if predicted.item() == 0 else 'NonDemented'
    return predicted_class


def getMultiLoader(image_path):
    # img = image.load_img(image_path, target_size=(176, 208))
    img = image.load_img(image_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    img_array = preprocess_input(img_array)

    return img_array



def multiPrediction(loader, model):
    # Make predictions using the Keras model
    predictions = model.predict(loader)

    # Get the predicted class index
    predicted_class_index = predictions.argmax(axis=1)[0]

    # Map the class index to your class labels
    # class_labels = {0: 'Demented', 1: 'NonDemented'}  # Modify this based on your actual class labels
    # predicted_class = class_labels[predicted_class_index]

    return predicted_class_index


def predictMulti():
    predictions = []
    model_path = 'C:/Users/hifia/Projects/Dementia Detection and Classification/Front-End/resources/models/multi-model.keras'
    for image in os.listdir('C:/Users/hifia/Projects/Dementia Detection and Classification/Front-End/uploads/MRIs/'):
        # image_path = 'C:/Users/hifia/Projects/Dementia Detection and Classification/Front-End/uploads/MRIs/uploaded_image.jpg'
        image_path = os.path.join('C:/Users/hifia/Projects/Dementia Detection and Classification/Front-End/uploads/MRIs/', image)
        model = load_model(model_path)
        loader = getMultiLoader(image_path)
        predicted_class = multiPrediction(loader, model)
        print(f"Name: {image}, Prediction: {predicted_class}")
        predictions.append(predicted_class)
    return predictions


