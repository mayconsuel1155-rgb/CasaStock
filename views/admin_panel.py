import flet as ft
from services.auth_service import AuthService
from database.banco import get_connection
from components.dialogs import mostrar_snackbar, mostrar_alerta
from components.botoes import botao_primario

def admin_panel_view(page: ft.Page) -> ft.Container:
    
    def listar_usuarios():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role, data_cadastro FROM Usuarios ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
        
    def carregar_tabela():
        tabela.rows.clear()
        usuarios = listar_usuarios()
        for u in usuarios:
            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(u['id']))),
                        ft.DataCell(ft.Text(u['username'])),
                        ft.DataCell(ft.Text(u['role'])),
                        ft.DataCell(ft.Text(u['data_cadastro'])),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(ft.Icons.PASSWORD, tooltip="Alterar Senha", on_click=lambda e, user=u['username']: abrir_modal_senha(user)),
                            ])
                        )
                    ]
                )
            )
        page.update()

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Usuário")),
            ft.DataColumn(ft.Text("Papel (Role)")),
            ft.DataColumn(ft.Text("Data Cadastro")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[]
    )

    # Modal Adicionar Cliente
    tf_novo_user = ft.TextField(label="Nome de Usuário (Cliente)")
    tf_nova_senha = ft.TextField(label="Senha Temporária", password=True, can_reveal_password=True)
    
    def salvar_novo_cliente(e):
        if not tf_novo_user.value or not tf_nova_senha.value:
            mostrar_snackbar(page, "Preencha todos os campos!", ft.Colors.RED)
            return
            
        if AuthService.register(tf_novo_user.value, tf_nova_senha.value):
            mostrar_snackbar(page, "Cliente registrado com sucesso!")
            page.pop_dialog()
            carregar_tabela()
        else:
            mostrar_snackbar(page, "Usuário já existe!", ft.Colors.RED)

    dialog_add = ft.AlertDialog(
        title=ft.Text("Novo Cliente"),
        content=ft.Column([tf_novo_user, tf_nova_senha], height=150),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
            botao_primario("Cadastrar", salvar_novo_cliente)
        ]
    )

    # Modal Alterar Senha
    tf_senha_reset = ft.TextField(label="Nova Senha", password=True, can_reveal_password=True)
    user_to_reset = None

    def salvar_reset_senha(e):
        if not tf_senha_reset.value:
            return
        if AuthService.update_password(user_to_reset, tf_senha_reset.value):
            mostrar_snackbar(page, "Senha alterada com sucesso!")
            page.pop_dialog()
        else:
            mostrar_snackbar(page, "Erro ao alterar senha.", ft.Colors.RED)

    dialog_senha = ft.AlertDialog(
        title=ft.Text("Alterar Senha do Cliente"),
        content=tf_senha_reset,
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
            botao_primario("Salvar Nova Senha", salvar_reset_senha)
        ]
    )

    def abrir_modal_add(e):
        tf_novo_user.value = ""
        tf_nova_senha.value = ""
        page.show_dialog(dialog_add)

    def abrir_modal_senha(username):
        nonlocal user_to_reset
        user_to_reset = username
        tf_senha_reset.value = ""
        page.show_dialog(dialog_senha)

    carregar_tabela()

    return ft.Container(
        content=ft.Column(
            [
                ft.Row([
                    ft.Text("Painel de Administração (SaaS)", size=30, weight=ft.FontWeight.BOLD),
                    botao_primario("Novo Cliente", abrir_modal_add, icone=ft.Icons.PERSON_ADD)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                ft.Container(
                    content=tabela,
                    padding=20,
                    bgcolor=ft.Colors.SURFACE,
                    border_radius=8,
                    border=ft.border.Border(
                        top=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                        bottom=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                        left=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                        right=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT)
                    )
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        ),
        padding=20,
        expand=True
    )
