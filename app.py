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
    page.title = "CasaStock Premium"
    page.window.width = 1000
    page.window.height = 800
    page.window.min_width = 350
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F9F8F6" # Fundo areia/gelo do Claude
    
    # Minimalist Theme
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE_GREY,
        font_family="Inter, Roboto, sans-serif",
        visual_density=ft.VisualDensity.COMFORTABLE
    )

    init_db()

    main_container = ft.Container(expand=True, padding=10)

    def nav_change(e):
        idx = e.control.selected_index
        update_view(idx)
        # Sync index between rail and bar
        nav_rail.selected_index = idx
        nav_bar.selected_index = idx
        page.update()

    destinations = [
        {"icon": ft.Icons.DASHBOARD_OUTLINED, "selected_icon": ft.Icons.DASHBOARD, "label": "Resumo"},
        {"icon": ft.Icons.INVENTORY_2_OUTLINED, "selected_icon": ft.Icons.INVENTORY_2, "label": "Estoque"},
        {"icon": ft.Icons.SHOPPING_CART_OUTLINED, "selected_icon": ft.Icons.SHOPPING_CART, "label": "Compras"},
        {"icon": ft.Icons.HISTORY_OUTLINED, "selected_icon": ft.Icons.HISTORY, "label": "Histórico"},
        {"icon": ft.Icons.SETTINGS_OUTLINED, "selected_icon": ft.Icons.SETTINGS, "label": "Ajustes"},
    ]

    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[ft.NavigationRailDestination(icon=d["icon"], selected_icon=d["selected_icon"], label=d["label"]) for d in destinations],
        on_change=nav_change,
    )

    nav_bar = ft.NavigationBar(
        selected_index=0,
        destinations=[ft.NavigationBarDestination(icon=d["icon"], selected_icon=d["selected_icon"], label=d["label"]) for d in destinations],
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
        # Add smooth fade in effect
        main_container.content = ft.AnimatedSwitcher(
            content=controls,
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=300,
            reverse_duration=100,
            switch_in_curve=ft.AnimationCurve.EASE_IN_OUT,
        )
        page.update()

    desktop_layout = ft.Row([nav_rail, ft.VerticalDivider(width=1), main_container], expand=True)

    def handle_resize(e):
        if not hasattr(page, 'casastock_user') or not page.casastock_user:
            return
            
        if page.window.width < 700:
            page.navigation_bar = nav_bar
            page.controls = [main_container]
        else:
            page.navigation_bar = None
            page.controls = [desktop_layout]
        page.update()

    page.on_resized = handle_resize

    def on_login_success():
        page.on_keyboard_event = None
        handle_resize(None)
        update_view(0)
        page.update()

    def check_auth():
        if hasattr(page, 'casastock_user') and page.casastock_user:
            on_login_success()
        else:
            page.navigation_bar = None
            page.controls.clear()
            page.add(get_login_view(page, on_login_success))
            page.update()

    def logout():
        page.casastock_user = None
        check_auth()
    
    page.logout = logout
    check_auth()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
