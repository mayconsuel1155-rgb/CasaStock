import flet as ft
import time
import threading

def main(page: ft.Page):
    dialog = ft.AlertDialog(title=ft.Text("Dialog from thread"))
    
    def on_click(e):
        def show():
            time.sleep(0.5)
            try:
                page.show_dialog(dialog)
                print("Dialog opened!")
            except Exception as e:
                print("Error:", e)
        threading.Thread(target=show).start()
        
    page.add(ft.ElevatedButton("Open", on_click=on_click))

ft.app(target=main)
