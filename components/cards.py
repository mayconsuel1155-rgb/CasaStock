import flet as ft
from database.models import Produto

def card_resumo(titulo: str, valor: str, icone: str, cor: str) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(icon=icone, size=40, color=cor),
                    padding=10,
                    bgcolor=ft.Colors.with_opacity(0.1, cor),
                    border_radius=10,
                ),
                ft.Column(
                    controls=[
                        ft.Text(titulo, size=14, weight=ft.FontWeight.W_500, color=ft.Colors.ON_SURFACE),
                        ft.Text(valor, size=24, weight=ft.FontWeight.BOLD),
                    ],
                    spacing=2,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=20,
        bgcolor=ft.Colors.SURFACE,
        border_radius=15,
        expand=True,
    )
