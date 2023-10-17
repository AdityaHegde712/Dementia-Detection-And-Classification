# from nicegui import ui
# import os

# def handle_upload(e):
#     with open(os.path.join('uploads', e.name), 'wb') as f:
#         f.write(e.file)

# @ui.page('/index')
# def index_page():
#     with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
#         with ui.row():
#             ui.label("Dementia Detection").style('font-size: 24px; font-weight: bold; color: #ffffff;')
#         with ui.row():
#             ui.button('Home', on_click=lambda: ui.notify('Go back home'))
#             ui.button('About', on_click=lambda: ui.notify('Go to footer'))

# index_page()
# ui.run(favicon='resources/dl3.png')

from nicegui import ui

@ui.page('/index')
def index_page():
    with ui.header(elevated=True).style('background-color: #4861f0; padding: 20px;').classes('items-center justify-between'):
        with ui.row().style('align-items: center;'):
            ui.label("Dementia Detection").style('font-size: 24px; font-weight: bold; color: #ffffff;')
        with ui.row():
            ui.button('Home', on_click=lambda: ui.notify('Go back home')).style('color: ##4861f0; text-decoration: none; margin-right: 20px;')
            ui.button('About', on_click=lambda: ui.notify('Go to footer')).style('color: ##4861f0; text-decoration: none;')

    ui.upload(on_upload=lambda e: ui.notify(f"Uploaded {e.name}"), 
              multiple=True, 
              max_file_size=100000000, 
              label="Upload the CSV Reports here")
       
index_page()
ui.run(favicon='resources/dl3.png')
