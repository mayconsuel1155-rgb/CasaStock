import flet as ft

def botao_primario(texto: str, on_click, icone: str = None) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        content=texto,
        icon=icone,
        on_click=on_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=6),
            elevation=0,
            bgcolor=ft.Colors.BLUE_GREY_900,
            color=ft.Colors.WHITE,
        )
    )

def botao_secundario(texto: str, on_click, icone: str = None) -> ft.OutlinedButton:
    return ft.OutlinedButton(
        content=texto,
        icon=icone,
        on_click=on_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=6),
            color=ft.Colors.BLUE_GREY_900,
        )
    )

def botao_icone(icone: str, on_click, tooltip: str = "", cor: str = None) -> ft.IconButton:
    return ft.IconButton(
        icon=icone,
        on_click=on_click,
        tooltip=tooltip,
        icon_color=cor
    )
