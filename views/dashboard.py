import flet as ft
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
