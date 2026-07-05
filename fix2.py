import os

dashboard_code = """import flet as ft
from services.historico_service import HistoricoService
from components.cards import card_resumo

def dashboard_view(page: ft.Page) -> ft.Container:
    resumo = HistoricoService.obter_resumo_dashboard()
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Dashboard", size=30, weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[
                        card_resumo("Total de Produtos", str(resumo['total_produtos']), ft.Icons.INVENTORY, ft.Colors.BLUE),
                        card_resumo("Em Falta", str(resumo['produtos_em_falta']), ft.Icons.WARNING_AMBER_ROUNDED, ft.Colors.RED),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    controls=[
                        card_resumo("Estoque Baixo", str(resumo['produtos_estoque_baixo']), ft.Icons.TRENDING_DOWN, ft.Colors.ORANGE),
                        card_resumo("Na Lista de Compras", str(resumo['itens_lista_compras']), ft.Icons.SHOPPING_CART, ft.Colors.GREEN),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    controls=[
                        card_resumo("Gasto no Mês", f"R$ {resumo['valor_gasto_mes']:.2f}", ft.Icons.ATTACH_MONEY, ft.Colors.TEAL),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        ),
        padding=20,
        expand=True
    )
"""

configuracoes_code = """import flet as ft
import shutil
import os
from components.dialogs import mostrar_snackbar

def configuracoes_view(page: ft.Page) -> ft.Container:
    def alterar_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.update()
        
    def fazer_backup(e):
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'casastock.db')
            backup_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backup')
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f'casastock_backup_{timestamp}.db')
            
            shutil.copy2(db_path, backup_path)
            mostrar_snackbar(page, f"Backup realizado com sucesso: casastock_backup_{timestamp}.db")
        except Exception as ex:
            mostrar_snackbar(page, f"Erro ao fazer backup: {str(ex)}", ft.Colors.RED)

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Configurações", size=30, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.ListTile(
                    leading=ft.Icon(icon=ft.Icons.DARK_MODE),
                    title=ft.Text("Alternar Tema Claro/Escuro"),
                    on_click=alterar_tema
                ),
                ft.ListTile(
                    leading=ft.Icon(icon=ft.Icons.SAVE),
                    title=ft.Text("Fazer Backup do Banco de Dados"),
                    subtitle=ft.Text("Cria uma cópia do banco na pasta backup"),
                    on_click=fazer_backup
                ),
                ft.ListTile(
                    leading=ft.Icon(icon=ft.Icons.INFO),
                    title=ft.Text("Sobre o CasaStock"),
                    subtitle=ft.Text("Versão 1.0 - Controle de Estoque Doméstico")
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        ),
        padding=20,
        expand=True
    )
"""

with open('views/dashboard.py', 'w', encoding='utf-8') as f: f.write(dashboard_code)
with open('views/configuracoes.py', 'w', encoding='utf-8') as f: f.write(configuracoes_code)
