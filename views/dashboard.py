import flet as ft
from services.historico_service import HistoricoService
from components.cards import card_resumo

def dashboard_view(page: ft.Page) -> ft.Container:
    user_id = getattr(page, 'casastock_user_id', 1)
    resumo = HistoricoService.obter_resumo_dashboard(user_id)
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Dashboard", size=30, weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(card_resumo("Total de Produtos", str(resumo['total_produtos']), ft.Icons.INVENTORY, ft.Colors.BLUE), col={"sm": 12, "md": 6, "xl": 3}),
                        ft.Container(card_resumo("Em Falta", str(resumo['produtos_em_falta']), ft.Icons.WARNING_AMBER_ROUNDED, ft.Colors.RED), col={"sm": 12, "md": 6, "xl": 3}),
                        ft.Container(card_resumo("Estoque Baixo", str(resumo['produtos_estoque_baixo']), ft.Icons.TRENDING_DOWN, ft.Colors.ORANGE), col={"sm": 12, "md": 6, "xl": 3}),
                        ft.Container(card_resumo("Na Lista de Compras", str(resumo['itens_lista_compras']), ft.Icons.SHOPPING_CART, ft.Colors.GREEN), col={"sm": 12, "md": 6, "xl": 3}),
                        ft.Container(card_resumo("Gasto no Mês", f"R$ {resumo['valor_gasto_mes']:.2f}", ft.Icons.ATTACH_MONEY, ft.Colors.TEAL), col={"sm": 12, "md": 6, "xl": 4}),
                    ],
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        ),
        padding=20,
        expand=True
    )
