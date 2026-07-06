import flet as ft
import shutil
import os
from components.dialogs import mostrar_snackbar, mostrar_alerta
from services.auth_service import AuthService
from components.botoes import botao_primario
from services.historico_service import HistoricoService

def configuracoes_view(page: ft.Page) -> ft.Container:
    user_id = getattr(page, 'casastock_user_id', 1)
    
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

    def zerar_gastos_mes(e):
        def confirmar():
            HistoricoService.zerar_historico_mes(user_id)
            page.pop_dialog()
            mostrar_alerta(page, "Sucesso", "Os gastos e o histórico de compras deste mês foram apagados!")
            page.update()
            
        from components.dialogs import mostrar_confirmacao
        mostrar_confirmacao(page, "Zerar Gastos", "Tem certeza que deseja apagar todo o histórico de compras deste mês? Esta ação não pode ser desfeita.", confirmar)

    tf_nova_senha = ft.TextField(label="Nova Senha", password=True, can_reveal_password=True, width=300)
    
    def confirmar_senha(e):
        if not tf_nova_senha.value:
            mostrar_snackbar(page, "Digite a nova senha!", ft.Colors.RED)
            return
            
        username = getattr(page, 'casastock_user', 'admin')
        if AuthService.update_password(username, tf_nova_senha.value):
            page.pop_dialog()
            mostrar_alerta(page, "Sucesso", "Senha alterada com sucesso!")
        else:
            mostrar_snackbar(page, "Erro ao alterar senha.", ft.Colors.RED)

    dialog_senha = ft.AlertDialog(
        title=ft.Text("Alterar Senha"),
        content=tf_nova_senha,
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
            botao_primario("Salvar", confirmar_senha)
        ]
    )

    def abrir_modal_senha(e):
        tf_nova_senha.value = ""
        page.show_dialog(dialog_senha)

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
                ),
                ft.Divider(),
                ft.ListTile(
                    leading=ft.Icon(icon=ft.Icons.DELETE_SWEEP, color=ft.Colors.RED),
                    title=ft.Text("Zerar Gastos do Mês"),
                    subtitle=ft.Text("Apaga o histórico de compras deste mês"),
                    on_click=zerar_gastos_mes
                ),
                ft.Divider(),
                ft.ListTile(
                    leading=ft.Icon(icon=ft.Icons.PASSWORD, color=ft.Colors.ORANGE),
                    title=ft.Text("Alterar Senha"),
                    on_click=abrir_modal_senha
                ),
                ft.ListTile(
                    leading=ft.Icon(icon=ft.Icons.LOGOUT, color=ft.Colors.RED),
                    title=ft.Text("Sair da Conta (Logout)"),
                    on_click=lambda e: page.logout()
                )
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        ),
        padding=20,
        expand=True
    )
