import flet as ft
from services.historico_service import HistoricoService

def historico_view(page: ft.Page) -> ft.Container:
    user_id = getattr(page, 'casastock_user_id', 1)
    lista_compras_ui = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def carregar_historico():
        lista_compras_ui.controls.clear()
        compras = HistoricoService.listar_compras(user_id)
        
        for c in compras:
            card = ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.RECEIPT, color=ft.Colors.TEAL),
                            title=ft.Text(f"{c.mercado if c.mercado else 'Mercado não informado'}", weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"Data: {c.data} | Pagamento: {c.forma_pagamento}"),
                            trailing=ft.Text(f"R$ {c.valor_total:.2f}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN)
                        ),
                        ft.TextButton("Ver Itens", icon=ft.Icons.LIST, on_click=lambda e, cid=c.id: mostrar_itens(cid))
                    ])
                )
            )
            lista_compras_ui.controls.append(card)
        page.update()

    def mostrar_itens(compra_id):
        itens = HistoricoService.obter_detalhes_compra(compra_id, user_id)
        
        lv = ft.ListView(expand=True, spacing=10)
        for i in itens:
            lv.controls.append(
                ft.ListTile(
                    title=ft.Text(i['nome']),
                    subtitle=ft.Text(f"{i['quantidade']} {i['unidade']} x R$ {i['valor_unitario']:.2f}"),
                    trailing=ft.Text(f"R$ {i['valor_total']:.2f}")
                )
            )
            
        dialog = ft.AlertDialog(
            title=ft.Text("Itens da Compra"),
            content=ft.Container(content=lv, width=400, height=300),
            actions=[
                ft.TextButton("Fechar", on_click=lambda e: fechar_dialog(dialog))
            ]
        )
        page.show_dialog(dialog)

    def fechar_dialog(dialog):
        page.pop_dialog()
        page.update()

    carregar_historico()

    return ft.Container(content=ft.Column([
            ft.Text("Histórico de Compras", size=30, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            lista_compras_ui
        ], scroll=ft.ScrollMode.AUTO, expand=True), padding=20, expand=True)
