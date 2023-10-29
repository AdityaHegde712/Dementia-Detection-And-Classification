from nicegui import ui, app
import asyncio
import tempfile
import os

@ui.page('/index')
def index_page():
    # Function definitions
    async def on_upload(e):
        if str(e.name).endswith('csv') or str(e.name).endswith('jpg'):
            with open(os.path.join('C:\\Users\\hifia\\Projects\\Dementia Detection and Classification\\Front-End\\uploads', e.name), mode='wb') as f:
                f.write(e.content.read())
            ui.notify(f"Uploaded and saved {e.name}")
            return
        await display_error_message()

    async def display_error_message():
        label = ui.label('Error: Invalid File Type!').classes('error')
        await asyncio.sleep(3)
        label.delete()
    
    def processMRI():
        ui.notify("The model will now work")

    # Styling
    ui.add_head_html('''
                    <link href="https://fonts.googleapis.com/css?family=Cairo+Play&display=swap" rel="stylesheet">
                    <style>
                        .subtitle {
                            font-family: 'Cairo Play', sans-serif;
                            font-size: 24px;
                            padding-left: 80px;
                            font-weight: bold;
                            margin-top: 50px;
                        }
                        .upload {
                            margin-left: 80px;
                        }
                        .error {
                            font-size: 18px;
                            font-family: 'Cairo Play', sans-serif;
                            font-color: red;
                            padding-left: 80px;
                            font-weight: bold;
                        }
                        .form {
                            margin-left: 80px;
                            margin-top: 20px;
                            margin-right: 150px;
                            font-family: 'Cairo Play', sans-serif;
                            font-size: 20px;
                            font-weight: bold;
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
    with ui.tabs().classes('w-full').style('margin-top: -120px;') as tabs:
        mri = ui.tab('MRI Scan')
        csv = ui.tab('CSV Report')
        form = ui.tab('Manual Entry')

    with ui.tab_panels(tabs, value=form).classes('w-full'):

        with ui.tab_panel(mri): # MRI Tab
            ui.label('Upload the MRI Scans Here\n').classes('subtitle')
            ui.upload(on_upload=on_upload, 
                    multiple=True, 
                    max_file_size=100000000, 
                    label="MRI file"
                    ).classes('upload items-center').tailwind.flex('auto').place_items('center')
            ui.add_body_html('<br><br>')
            ui.button(text="Get Probabilities", on_click=processMRI).classes('items-center').style('margin-left: 80px; margin-top: 50px;').tailwind.flex('auto').place_items('center')
            
        with ui.tab_panel(csv): # CSV Tab
            ui.label("Upload the CSV Reports here\n").classes('subtitle')
            ui.upload(on_upload=on_upload, 
                    multiple=True, 
                    max_file_size=100000000, 
                    label="CSV file"
                    ).classes('upload items-center').tailwind.flex('auto').place_items('center')
            ui.add_body_html('<br><br>')
            ui.button(text="Get Probabilities", on_click=processMRI).classes('items-center').style('margin-left: 80px; margin-top: 50px;').tailwind.flex('auto').place_items('center')
        
        with ui.tab_panel(form): # Form Tab
            ui.label('Enter your information manually:').classes('subtitle')
            # Form control for MMSE, nWBW, M/F, EDUC, MR Delay, eTIV, ASF
            ui.input(label='MMSE', placeholder='Please enter MMSE value',
            validation={'Wrong Input type': lambda value: str(value).isnumeric()}).classes('form')
            ui.input(label='nWBW', placeholder='Please enter nWBW value',
            validation={'Wrong Input type': lambda value: str(value).isnumeric()}).classes('form')
            ui.input(label='M/F', placeholder='Please enter M/F value',
            validation={'Wrong Input type': lambda value: str(value).isnumeric()}).classes('form')
            ui.input(label='EDUC', placeholder='Please enter EDUC value',
            validation={'Wrong Input type': lambda value: str(value).isnumeric()}).classes('form')
            ui.input(label='MR Delay', placeholder='Please enter MR Delay value',
            validation={'Wrong Input type': lambda value: str(value).isnumeric()}).classes('form')
            ui.input(label='eTIV', placeholder='Please enter eTIV value',
            validation={'Wrong Input type': lambda value: str(value).isnumeric()}).classes('form')
            ui.input(label='ASF', placeholder='Please enter ASF value',
            validation={'Wrong Input type': lambda value: str(value).isnumeric()}).classes('form')
            ui.add_body_html('<br><br>')
            ui.button(text="Get Probabilities", on_click=processMRI).classes('items-center').style('margin-left: 80px; margin-top: 50px;').tailwind.flex('auto').place_items('center')       
    

index_page()
ui.run(favicon='Front-End\\resources\\dl3.png', port=5000)