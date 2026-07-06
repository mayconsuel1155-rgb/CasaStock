import flet as ft
from services.estoque_service import EstoqueService
from services.compra_service import CompraService
from database.models import Produto
from components.dialogs import mostrar_snackbar, mostrar_confirmacao
from components.botoes import botao_primario, botao_icone

def estoque_view(page: ft.Page) -> ft.Container:
    lista_produtos_ui = ft.ResponsiveRow()
    
    # Campos Formulário
    tf_id = ft.TextField(visible=False)
    tf_nome = ft.TextField(label="Nome", expand=True)
    tf_categoria = ft.TextField(label="Categoria", expand=True)
    tf_qtde = ft.TextField(label="Qtde Atual", value="0", expand=True, keyboard_type=ft.KeyboardType.NUMBER)
    tf_qtde_min = ft.TextField(label="Qtde Mínima", value="0", expand=True, keyboard_type=ft.KeyboardType.NUMBER)
    tf_unidade = ft.TextField(label="Unidade (ex: un, kg, L)", expand=True)
    tf_local = ft.TextField(label="Local", expand=True)
    tf_obs = ft.TextField(label="Observações", multiline=True)

    def carregar_produtos(e=None):
        lista_produtos_ui.controls.clear()
        produtos = EstoqueService.listar_produtos()
        for p in produtos:
            
            # Checar se precisa sugerir lista de compras (RN004)
            cor_estoque = ft.Colors.GREEN
            if p.quantidade == 0:
                cor_estoque = ft.Colors.RED
            elif p.quantidade <= p.quantidade_minima:
                cor_estoque = ft.Colors.ORANGE
                
            card = ft.Container(
                content=ft.Container(
                    padding=15,
                    bgcolor=ft.Colors.SURFACE,
                    border_radius=8,
                    border=ft.border.Border(
                        top=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                        bottom=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                        left=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                        right=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT)
                    ),
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.INVENTORY_2, color=cor_estoque, size=30),
                            title=ft.Text(p.nome, weight=ft.FontWeight.BOLD, size=18),
                            subtitle=ft.Text(f"{p.categoria}\nQtde: {p.quantidade} {p.unidade} (Mín: {p.quantidade_minima})"),
                            trailing=ft.Row([
                                botao_icone(ft.Icons.EDIT, lambda e, prod=p: abrir_form(prod), cor=ft.Colors.BLUE),
                                botao_icone(ft.Icons.DELETE, lambda e, prod=p: confirmar_exclusao(prod.id), cor=ft.Colors.RED),
                            ], tight=True)
                        ),
                        # Botão para adicionar a lista caso estoque baixo
                        ft.Row([
                            ft.OutlinedButton("Comprar", icon=ft.Icons.ADD_SHOPPING_CART, 
                                          on_click=lambda e, pid=p.id: adicionar_lista(pid))
                        ], alignment=ft.MainAxisAlignment.END, visible=(p.quantidade <= p.quantidade_minima))
                    ])
                ),
                col={"sm": 12, "md": 6, "lg": 4}
            )
            lista_produtos_ui.controls.append(card)
        page.update()

    def adicionar_lista(produto_id):
        CompraService.adicionar_a_lista(produto_id)
        mostrar_snackbar(page, "Item adicionado à lista de compras!")
        carregar_produtos()

    def confirmar_exclusao(produto_id):
        mostrar_confirmacao(page, "Excluir Produto", "Tem certeza que deseja excluir este produto?", lambda: excluir_produto(produto_id))

    def excluir_produto(produto_id):
        EstoqueService.excluir_produto(produto_id)
        mostrar_snackbar(page, "Produto excluído com sucesso!")
        carregar_produtos()

    def salvar_produto_submit(e):
        if not tf_nome.value:
            mostrar_snackbar(page, "O nome do produto é obrigatório!", ft.Colors.RED)
            return
            
        try:
            qtde = float(tf_qtde.value.replace(',', '.'))
            qtde_min = float(tf_qtde_min.value.replace(',', '.'))
        except ValueError:
            mostrar_snackbar(page, "Quantidade deve ser um número!", ft.Colors.RED)
            return

        p = Produto(
            id=int(tf_id.value) if tf_id.value else None,
            nome=tf_nome.value,
            categoria=tf_categoria.value,
            quantidade=qtde,
            quantidade_minima=qtde_min,
            unidade=tf_unidade.value,
            local=tf_local.value,
            observacoes=tf_obs.value,
            data_cadastro=""
        )
        EstoqueService.salvar_produto(p)
        page.pop_dialog()
        mostrar_snackbar(page, "Produto salvo com sucesso!")
        carregar_produtos()

    dialog_form = ft.AlertDialog(
        title=ft.Text("Produto"),
        content=ft.Column([
            tf_id,
            tf_nome,
            tf_categoria,
            ft.Row([tf_qtde, tf_qtde_min]),
            ft.Row([tf_unidade, tf_local]),
            tf_obs
        ], width=400, tight=True),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: fechar_form()),
            botao_primario("Salvar", salvar_produto_submit)
        ],
    )

    def fechar_form():
        page.pop_dialog()
        page.update()

    def abrir_form(produto=None):
        if produto:
            tf_id.value = str(produto.id)
            tf_nome.value = produto.nome
            tf_categoria.value = produto.categoria
            tf_qtde.value = str(produto.quantidade)
            tf_qtde_min.value = str(produto.quantidade_minima)
            tf_unidade.value = produto.unidade
            tf_local.value = produto.local
            tf_obs.value = produto.observacoes
        else:
            tf_id.value = ""
            tf_nome.value = ""
            tf_categoria.value = ""
            tf_qtde.value = "0"
            tf_qtde_min.value = "0"
            tf_unidade.value = "un"
            tf_local.value = ""
            tf_obs.value = ""
            
        page.show_dialog(dialog_form)

    carregar_produtos()

    return ft.Container(content=ft.Column([
            ft.Row([
                ft.Text("Estoque", size=30, weight=ft.FontWeight.BOLD),
                botao_primario("Novo Produto", lambda e: abrir_form(), ft.Icons.ADD)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
            ft.Column([lista_produtos_ui], scroll=ft.ScrollMode.AUTO, expand=True)
        ], expand=True), padding=20, expand=True)
