from nicegui import ui, app
import asyncio
import os

@ui.page('/index')
def index_page():
    # Function definitions
    async def on_upload(e):
        if not str(e.name).endswith('csv'):
            await display_error_message()
        else:
            with open(os.path.join('uploads', e.name), 'wb') as f:
                f.write(e.content)
            ui.label(f"Uploaded and saved {e.name}")

    async def display_error_message():
        label = ui.label('Error: Invalid File Type!').classes('error')
        await asyncio.sleep(3)
        label.delete()

    # Styling
    ui.add_head_html('''
                    <link href="https://fonts.googleapis.com/css?family=Cairo+Play&display=swap" rel="stylesheet">
                    <style>
                        .subtitle {
                            font-family: 'Cairo Play', sans-serif;
                            font-size: 24px;
                            padding-left: 80px;
                            font-weight: bold;
                            margin-top: 80px;
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
                    </style>       
             ''')
    
    # Navbar
    with ui.header(elevated=True).style('background-color: #4861f0; padding: 20px;').classes('items-center justify-between'):
        with ui.row().style('align-items: center;'):
            ui.image('resources/dl3.png').classes('w-10')
            ui.label("Dementia Detection").style('font-size: 24px; font-weight: bold; color: #ffffff;')
        with ui.row():
            ui.button('Home', on_click=lambda: ui.notify('Go back home')).style('color: ##4861f0; text-decoration: none; margin-right: 20px;')
            ui.button('About', on_click=lambda: ui.notify('Go to footer')).style('color: ##4861f0; text-decoration: none;')
    
    # Content
    ui.label("Upload the CSV Reports here").classes('subtitle')
    ui.upload(on_upload=on_upload, 
              multiple=True, 
              max_file_size=100000000, 
              label="CSV file"
            ).classes('upload').tailwind.flex('auto').place_items('center')
       
index_page()
ui.run(favicon='resources/dl3.png')

# Tab viwe