import flet as ft
from services.estoque_service import EstoqueService
from services.compra_service import CompraService
import urllib.request
import json
import urllib.error
from database.models import Produto
from components.dialogs import mostrar_snackbar, mostrar_confirmacao
from components.botoes import botao_primario, botao_icone

def estoque_view(page: ft.Page) -> ft.Container:
    user_id = getattr(page, 'casastock_user_id', 1)
    lista_produtos_ui = ft.ResponsiveRow()
    
    # Campos Formulário
    tf_id = ft.TextField(visible=False)
    
    def buscar_produto_por_codigo(e):
        codigo = tf_codigo_barras.value.strip()
        if not codigo: return
        
        # Tenta buscar no banco local primeiro
        prod_local = EstoqueService.buscar_por_codigo_barras(codigo, user_id)
        if prod_local:
            tf_id.value = str(prod_local.id)
            tf_nome.value = prod_local.nome
            tf_categoria.value = prod_local.categoria
            tf_qtde.value = str(prod_local.quantidade)
            tf_qtde_min.value = str(prod_local.quantidade_minima)
            tf_unidade.value = prod_local.unidade
            tf_local.value = prod_local.local
            tf_obs.value = prod_local.observacoes
            mostrar_snackbar(page, "Produto carregado do estoque local!", ft.Colors.BLUE)
            page.update()
            return
            
        # Se não achou, busca no Open Food Facts
        try:
            url = f"https://world.openfoodfacts.org/api/v2/product/{codigo}.json"
            req = urllib.request.Request(url, headers={'User-Agent': 'CasaStock/1.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                if data.get('status') == 1:
                    produto = data.get('product', {})
                    nome_api = produto.get('product_name_pt') or produto.get('product_name', '')
                    categoria_api = produto.get('categories', '').split(',')[0] if produto.get('categories') else ''
                    if nome_api:
                        tf_nome.value = nome_api
                        tf_categoria.value = categoria_api
                        mostrar_snackbar(page, "Dados encontrados na internet!", ft.Colors.GREEN)
                        page.update()
                    else:
                        mostrar_snackbar(page, "Produto encontrado, mas sem nome em português.", ft.Colors.ORANGE)
                else:
                    mostrar_snackbar(page, "Produto não encontrado na internet. Preencha manualmente.", ft.Colors.ORANGE)
        except urllib.error.URLError:
             mostrar_snackbar(page, "Sem conexão com a internet para buscar o produto.", ft.Colors.RED)
        except Exception:
             mostrar_snackbar(page, "Erro ao buscar produto na internet.", ft.Colors.RED)

    def handle_scan_estoque(code):
        page.dialog = dialog_form
        dialog_form.open = True
        tf_codigo_barras.value = code
        page.update()
        buscar_produto_por_codigo(None)
    page.on_scan_estoque = handle_scan_estoque

    tf_codigo_barras = ft.TextField(label="Código de Barras (Escaneie e dê Enter)", on_submit=buscar_produto_por_codigo, expand=True)
    row_codigo_barras = ft.Row([
        tf_codigo_barras,
        ft.IconButton(icon=ft.Icons.CAMERA_ALT, tooltip="Abrir Câmera", url=ft.Url(url='/scanner.html?mode=estoque', target='_blank'))
    ])
    tf_nome = ft.TextField(label="Nome", expand=True)
    tf_categoria = ft.TextField(label="Categoria", expand=True)
    tf_qtde = ft.TextField(label="Qtde Atual", value="0", expand=True, keyboard_type=ft.KeyboardType.NUMBER)
    tf_qtde_min = ft.TextField(label="Qtde Mínima", value="0", expand=True, keyboard_type=ft.KeyboardType.NUMBER)
    tf_unidade = ft.TextField(label="Unidade (ex: un, kg, L)", expand=True)
    tf_local = ft.TextField(label="Local", expand=True)
    tf_obs = ft.TextField(label="Observações", multiline=True)

    def carregar_produtos(e=None):
        lista_produtos_ui.controls.clear()
        produtos = EstoqueService.listar_produtos(user_id)
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

    def adicionar_lista(produto_id: int):
        CompraService.adicionar_a_lista(user_id, produto_id)
        mostrar_snackbar(page, "Item adicionado à lista de compras!")
        carregar_produtos()

    def confirmar_exclusao(produto_id):
        mostrar_confirmacao(page, "Excluir Produto", "Tem certeza que deseja excluir este produto?", lambda: excluir_produto(produto_id))

    def excluir_produto(produto_id):
        EstoqueService.excluir_produto(produto_id, user_id)
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
            id_usuario=user_id,
            nome=tf_nome.value,
            categoria=tf_categoria.value,
            quantidade=qtde,
            quantidade_minima=qtde_min,
            unidade=tf_unidade.value,
            local=tf_local.value,
            observacoes=tf_obs.value,
            data_cadastro="",
            codigo_barras=tf_codigo_barras.value.strip()
        )
        EstoqueService.salvar_produto(p)
        page.pop_dialog()
        mostrar_snackbar(page, "Produto salvo com sucesso!")
        carregar_produtos()

    dialog_form = ft.AlertDialog(
        title=ft.Text("Produto"),
        content=ft.Column([
            tf_id,
            row_codigo_barras,
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
            tf_codigo_barras.value = getattr(produto, 'codigo_barras', '')
            tf_nome.value = produto.nome
            tf_categoria.value = produto.categoria
            tf_qtde.value = str(produto.quantidade)
            tf_qtde_min.value = str(produto.quantidade_minima)
            tf_unidade.value = produto.unidade
            tf_local.value = produto.local
            tf_obs.value = produto.observacoes
        else:
            tf_id.value = ""
            tf_codigo_barras.value = ""
            tf_nome.value = ""
            tf_categoria.value = ""
            tf_qtde.value = "0"
            tf_qtde_min.value = "0"
            tf_unidade.value = "un"
            tf_local.value = ""
            tf_obs.value = ""
            
        page.dialog = dialog_form
        dialog_form.open = True
        page.update()

    carregar_produtos()

    return ft.Container(content=ft.Column([
            ft.Row([
                ft.Text("Estoque", size=30, weight=ft.FontWeight.BOLD),
                botao_primario("Novo Produto", lambda e: abrir_form(), ft.Icons.ADD)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
            ft.Column([lista_produtos_ui], scroll=ft.ScrollMode.AUTO, expand=True)
        ], expand=True), padding=20, expand=True)
