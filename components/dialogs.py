import flet as ft

def mostrar_alerta(page: ft.Page, titulo: str, mensagem: str):
    dialog = ft.AlertDialog(
        title=ft.Text(titulo),
        content=ft.Text(mensagem),
        actions=[
            ft.TextButton("OK", on_click=lambda e: fechar_dialog(page, dialog))
        ],
    )
    page.show_dialog(dialog)

def mostrar_confirmacao(page: ft.Page, titulo: str, mensagem: str, on_confirm):
    def handle_confirm(e):
        fechar_dialog(page, dialog)
        on_confirm()
        
    dialog = ft.AlertDialog(
        title=ft.Text(titulo),
        content=ft.Text(mensagem),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: fechar_dialog(page, dialog)),
            ft.TextButton("Confirmar", on_click=handle_confirm),
        ],
    )
    page.show_dialog(dialog)

def mostrar_snackbar(page: ft.Page, mensagem: str, cor: str = ft.Colors.GREEN):
    snack = ft.SnackBar(
        content=ft.Text(mensagem),
        bgcolor=cor,
        duration=3000
    )
    page.overlay.append(snack)
    snack.open = True
    page.update()

def fechar_dialog(page: ft.Page, dialog: ft.AlertDialog):
    page.pop_dialog()
