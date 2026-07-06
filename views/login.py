import flet as ft
from services.auth_service import AuthService
from components.dialogs import mostrar_snackbar

def get_login_view(page: ft.Page, on_login_success):
    tf_username = ft.TextField(label="Usuário", width=300, autofocus=True)
    tf_password = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)

    def fazer_login(e):
        if not tf_username.value or not tf_password.value:
            mostrar_snackbar(page, "Preencha usuário e senha!", ft.Colors.RED)
            return
            
        auth_result = AuthService.login(tf_username.value, tf_password.value)
        if auth_result.get("success"):
            page.casastock_user = auth_result["username"]
            page.casastock_user_id = auth_result["id"]
            page.casastock_role = auth_result["role"]
            on_login_success()
        else:
            mostrar_snackbar(page, "Usuário ou senha incorretos!", ft.Colors.RED)

    # Allow Enter key to trigger login
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "Enter":
            fazer_login(None)

    page.on_keyboard_event = on_keyboard

    btn_login = ft.ElevatedButton(
        content=ft.Text("Entrar", size=16, weight=ft.FontWeight.BOLD),
        width=300,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=fazer_login
    )

    # Centralize card on screen
    return ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.LOCK_PERSON, size=80, color=ft.Colors.BLUE),
                ft.Text("CasaStock Login", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                tf_username,
                tf_password,
                ft.Container(height=20),
                btn_login,
                ft.Container(height=10),
                ft.Text("Usuário padrão: admin / admin", italic=True, color=ft.Colors.GREY_500)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        ),
        alignment=ft.Alignment.CENTER,
        expand=True
    )
