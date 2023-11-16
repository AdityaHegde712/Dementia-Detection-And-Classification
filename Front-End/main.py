from nicegui import ui, app
import asyncio
import tempfile
import os
from model import *

table_display = None

@ui.page('/index')
def index_page():
    # Function definitions
    async def on_upload(e):
        os.makedirs('C:\\Users\\hifia\\Projects\\Dementia Detection and Classification\\Front-End\\uploads\\CSVs', exist_ok=True)
        os.makedirs('C:\\Users\\hifia\\Projects\\Dementia Detection and Classification\\Front-End\\uploads\\MRIs', exist_ok=True)
        if str(e.name).endswith('csv'):
            with open(os.path.join('C:\\Users\\hifia\\Projects\\Dementia Detection and Classification\\Front-End\\uploads\\CSVs', "uploaded_file.csv"), mode='wb') as f:
                f.write(e.content.read())
            ui.notify(f"Uploaded and saved {e.name} as uploaded_file.csv")
            return
        elif str(e.name).endswith('jpg'):
            with open(os.path.join('C:\\Users\\hifia\\Projects\\Dementia Detection and Classification\\Front-End\\uploads\\MRIs', "uploaded_image.jpg"), mode='wb') as f:
                f.write(e.content.read())
            ui.notify(f"Uploaded and saved {e.name} as uploaded_image.jpg")
            return
        await display_error_message()

    async def display_error_message():
        label = ui.label('Error: Invalid File Type!').classes('error')
        await asyncio.sleep(3)
        label.delete()

    def processMRI():
        ui.notify("The model will now work")
        prediction = predict()
        ui.add_body_html('<br><br><br>')
        ui.label(f"Prediction: {prediction}").style('font-size: 24px; font-weight: bold; text-align: center; margin-top: 50px;')
        # if prediction == 'Demented':
        #     m_prediction = predictMulti()
        #     ui.add_body_html('<br><br><br>')
        #     ui.label(f"Multi-Class Prediction: {m_prediction}").style('font-size: 24px; font-weight: bold; text-align: center; margin-top: 30px;')
        os.remove('C:\\Users\\hifia\\Projects\\Dementia Detection and Classification\\Front-End\\uploads\\MRIs\\uploaded_image.jpg')

    def processCSV():
        global table_display
        ui.notify("The model will now work")
        table_display = predictCSVs()
        print(f"Table: {table_display}")
        ui.add_body_html('<br><br><br>')
        columns = [
            {'name': 'entry', 'label': 'Entry', 'field': 'entry', 'required': True, 'align': 'center'},
            {'name': 'diag', 'label': 'Diagnosis', 'field': 'diag', 'sortable': True, 'align': 'center'},
        ]
        print(f"\n\nRows: {table_display}")
        print(f"\n\nColumns: {columns}\n")
        ui.table(columns=columns, rows=table_display).style('margin-left: 580px; margin-right: 600px; margin-top: 50px;')
        
        

    # Styling
    ui.add_head_html('''
                    <link href="https://fonts.googleapis.com/css?family=Cairo+Play&display=swap" rel="stylesheet">
                    <style>
                        .subtitle {
                            font-family: 'Cairo Play', sans-serif;
                            font-size: 24px;
                            font-weight: bold;
                            margin-top: 50px;
                        }
                        .upload {
                            margin-left: auto;
                            margin-right: auto;
                            text-align: center;  
                        }
                        .error {
                            font-size: 18px;
                            font-family: 'Cairo Play', sans-serif;
                            font-color: red;
                            padding-left: 80px;
                            font-weight: bold;
                        }
                        .form {
                            font-family: 'Cairo Play', sans-serif;
                            font-size: 20px;
                            font-weight: bold;
                            justify-content: center;
                            width: 50%;
                            margin-left: 380px;
                            margin-top: 20px;
                            margin-right: 400px;
                        }
                    </style>       
             ''')
    
    # Navbar
    with ui.header(elevated=True).style('background-color: #4861f0; padding: 20px;').classes('items-center justify-between'):
        with ui.row().style('align-items: center;'):
            ui.image('C:\\Users\\hifia\\Projects\\Dementia Detection and Classification\\Front-End\\resources\\dl3.png').classes('w-10')
            ui.label("Dementia Detection").style('font-size: 24px; font-weight: bold; color: #ffffff;')
        with ui.row():
            ui.button('Home', on_click=lambda: ui.notify('Go back home')).style('color: ##4861f0; text-decoration: none; margin-right: 20px;')
            ui.button('About', on_click=lambda: ui.notify('Go to footer')).style('color: ##4861f0; text-decoration: none;')
    
    # Content
    with ui.tabs().classes('w-full').style('margin-top: -120px; margin-left: auto; margin-right: auto; text-align: center;') as tabs:
        mri = ui.tab('MRI Scan')
        csv = ui.tab('CSV Report')

    with ui.tab_panels(tabs, value=mri).classes('w-full'):

        with ui.tab_panel(mri): # MRI Tab
            ui.label('Upload the MRI Scans Here\n').classes('subtitle').style('text-align: center;'); ui.html('<br>')
            ui.upload(on_upload=on_upload, 
                    multiple=True, 
                    max_file_size=100000000, 
                    label="MRI file"
                    ).classes('upload items-center').tailwind.flex('auto').place_items('center')
            ui.add_body_html('<br><br>')
            ui.button(text="Get Probabilities", on_click=processMRI).classes('items-center upload').style('margin-top: 50px; display: flex; justify-content: center;')
            ui.add_body_html('<br><br>')

            
        with ui.tab_panel(csv): # CSV Tab
            ui.label("Upload the CSV Reports here\n").classes('subtitle').style('text-align: center;'); ui.html('<br>')
            ui.upload(on_upload=on_upload, 
                    multiple=True, 
                    max_file_size=100000000, 
                    label="CSV file"
                    ).classes('upload')
            ui.add_body_html('<br><br>')
            ui.button(text="Get Probabilities", on_click=processCSV).classes('items-center upload').style('margin-top: 50px; display: flex; justify-content: center;')
            ui.add_body_html('<br><br>')
            
            
index_page()
ui.run(favicon='Front-End\\resources\\dl3.png', port=5000, on_air=True)