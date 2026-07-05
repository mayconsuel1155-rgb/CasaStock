import flet as ft
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.banco import init_db
from views.dashboard import dashboard_view
from views.estoque import estoque_view
from views.compras import compras_view
from views.historico import historico_view
from views.configuracoes import configuracoes_view
from views.login import get_login_view

def main(page: ft.Page):
    page.title = "CasaStock"
    page.window.width = 1000
    page.window.height = 800
    page.window.min_width = 800
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)

    init_db()

    main_container = ft.Container(expand=True)

    def nav_change(e):
        idx = nav_rail.selected_index
        update_view(idx)

    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.DASHBOARD_OUTLINED, selected_icon=ft.Icons.DASHBOARD, label="Dashboard"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.INVENTORY_2_OUTLINED, selected_icon=ft.Icons.INVENTORY_2, label="Estoque"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SHOPPING_CART_OUTLINED, selected_icon=ft.Icons.SHOPPING_CART, label="Compras"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.HISTORY_OUTLINED, selected_icon=ft.Icons.HISTORY, label="Histórico"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS, label="Configurações"
            ),
        ],
        on_change=nav_change,
    )

    def get_view(idx):
        if idx == 0: return dashboard_view(page)
        elif idx == 1: return estoque_view(page)
        elif idx == 2: return compras_view(page)
        elif idx == 3: return historico_view(page)
        elif idx == 4: return configuracoes_view(page)
        return dashboard_view(page)

    def update_view(idx):
        controls = get_view(idx)
        main_container.content = controls
        page.update()

    layout = ft.Row(
        [
            nav_rail,
            ft.VerticalDivider(width=1),
            main_container
        ],
        expand=True
    )

    def on_login_success():
        page.on_keyboard_event = None
        page.controls.clear()
        page.add(layout)
        update_view(0)
        page.update()

    def check_auth():
        if hasattr(page, 'casastock_user') and page.casastock_user:
            on_login_success()
        else:
            page.controls.clear()
            page.add(get_login_view(page, on_login_success))
            page.update()

    # Public function to logout
    def logout():
        page.casastock_user = None
        check_auth()
    
    # Store logout function in page for views to access
    page.logout = logout

    check_auth()

if __name__ == "__main__":
    ft.run(main)
