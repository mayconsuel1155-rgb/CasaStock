import flet as ft
from services.compra_service import CompraService
from services.estoque_service import EstoqueService
from components.dialogs import mostrar_snackbar, mostrar_alerta
from components.botoes import botao_primario, botao_secundario

def compras_view(page: ft.Page) -> ft.Container:
    lista_compras_ui = ft.ResponsiveRow()
    itens_compra_atual = []

    def carregar_lista():
        lista_compras_ui.controls.clear()
        itens_lista = CompraService.listar_itens_lista()
        itens_compra_atual.clear()
        
        if not itens_lista:
            lista_compras_ui.controls.append(ft.Text("A lista de compras está vazia.", size=16, italic=True))
        else:
            for item in itens_lista:
                p = item['produto']
                
                tf_qtde_comprada = ft.TextField(label="Qtde", value=str(item['quantidade_lista']), width=100, keyboard_type=ft.KeyboardType.NUMBER)
                tf_valor_unit = ft.TextField(label="R$ Unitário", value="0.00", width=120, keyboard_type=ft.KeyboardType.NUMBER)
                
                item_dict = {
                    'id_produto': p.id,
                    'nome': p.nome,
                    'tf_qtde': tf_qtde_comprada,
                    'tf_valor': tf_valor_unit,
                    'lista_id': item['lista_id']
                }
                itens_compra_atual.append(item_dict)

                card = ft.Container(
                    content=ft.Container(
                        padding=15,
                        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
                        border_radius=15,
                        border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
                        shadow=ft.BoxShadow(
                            spread_radius=1, blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK), offset=ft.Offset(0, 4)
                        ),
                        content=ft.Column([
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.SHOPPING_BAG, color=ft.Colors.ORANGE, size=30),
                                title=ft.Text(p.nome, weight=ft.FontWeight.BOLD, size=18),
                                subtitle=ft.Text(f"Estoque: {p.quantidade} {p.unidade} | Mín: {p.quantidade_minima}"),
                                trailing=ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=lambda e, lid=item['lista_id']: remover_lista(lid))
                            ),
                            ft.Row([
                                tf_qtde_comprada,
                                tf_valor_unit
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ])
                    ),
                    col={"sm": 12, "md": 6, "lg": 4}
                )
                lista_compras_ui.controls.append(card)
        page.update()

    def remover_lista(lista_id):
        CompraService.remover_da_lista(lista_id)
        mostrar_snackbar(page, "Item removido da lista!")
        carregar_lista()

    dd_produto = ft.Dropdown(label="Selecione um Produto", expand=True)
    tf_qtde_add = ft.TextField(label="Qtde", value="1", width=100, keyboard_type=ft.KeyboardType.NUMBER)

    def carregar_produtos_dropdown():
        dd_produto.options.clear()
        for p in EstoqueService.listar_produtos():
            dd_produto.options.append(ft.dropdown.Option(str(p.id), p.nome))
        page.update()

    def adicionar_manual(e):
        if not dd_produto.value:
            mostrar_snackbar(page, "Selecione um produto!", ft.Colors.RED)
            return
        
        try:
            qtde = float(tf_qtde_add.value.replace(',', '.'))
        except:
            qtde = 1.0
            
        CompraService.adicionar_a_lista(int(dd_produto.value), qtde)
        page.pop_dialog()
        mostrar_snackbar(page, "Item adicionado à lista!")
        carregar_lista()

    dialog_add = ft.AlertDialog(
        title=ft.Text("Adicionar Item Manualmente"),
        content=ft.Row([dd_produto, tf_qtde_add], width=400),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: fechar_dialog(dialog_add)),
            botao_primario("Adicionar", adicionar_manual)
        ]
    )

    def abrir_add_manual(e):
        carregar_produtos_dropdown()
        page.show_dialog(dialog_add)

    def fechar_dialog(dialog):
        page.pop_dialog()
        page.update()

    tf_mercado = ft.TextField(label="Mercado", expand=True)
    dd_pagamento = ft.Dropdown(label="Pagamento", options=[
        ft.dropdown.Option("Dinheiro"),
        ft.dropdown.Option("Cartão de Crédito"),
        ft.dropdown.Option("Cartão de Débito"),
        ft.dropdown.Option("PIX"),
        ft.dropdown.Option("Vale Alimentação"),
    ], value="Cartão de Crédito", expand=True)
    tf_obs_compra = ft.TextField(label="Observações da Compra", multiline=True)

    def finalizar_compra(e):
        if not itens_compra_atual:
            mostrar_snackbar(page, "A lista de compras está vazia!", ft.Colors.RED)
            return

        itens_para_salvar = []
        for i in itens_compra_atual:
            try:
                qtde = float(i['tf_qtde'].value.replace(',', '.'))
                valor = float(i['tf_valor'].value.replace(',', '.'))
                if qtde > 0 and valor > 0:
                    itens_para_salvar.append({
                        'id_produto': i['id_produto'],
                        'quantidade': qtde,
                        'valor_unitario': valor
                    })
            except:
                pass
        
        if not itens_para_salvar:
            mostrar_snackbar(page, "Para finalizar, preencha valor unitário > 0 nos itens comprados.", ft.Colors.RED)
            return
            
        sucesso = CompraService.registrar_compra(
            mercado=tf_mercado.value,
            forma_pagamento=dd_pagamento.value,
            observacoes=tf_obs_compra.value,
            itens=itens_para_salvar
        )
        
        if sucesso:
            page.pop_dialog()
            mostrar_alerta(page, "Sucesso", "Compra registrada e estoque atualizado!")
            carregar_lista()
        else:
            mostrar_snackbar(page, "Erro ao registrar compra.", ft.Colors.RED)

    dialog_finalizar = ft.AlertDialog(
        title=ft.Text("Finalizar Compra"),
        content=ft.Column([tf_mercado, dd_pagamento, tf_obs_compra], width=400, tight=True),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: fechar_dialog(dialog_finalizar)),
            botao_primario("Confirmar Compra", finalizar_compra)
        ]
    )

    def abrir_finalizar(e):
        page.show_dialog(dialog_finalizar)

    carregar_lista()

    return ft.Container(
        content=ft.Column(
            [
                ft.Row([
                    ft.Text("Lista de Compras", size=30, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        botao_secundario("Add Manual", abrir_add_manual, ft.Icons.ADD),
                        botao_primario("Finalizar Compra", abrir_finalizar, ft.Icons.CHECK)
                    ])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
                ft.Column([lista_compras_ui], scroll=ft.ScrollMode.AUTO, expand=True)
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        ),
        padding=20,
        expand=True
    )
