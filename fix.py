import os
import glob
import re

# Refatorar app.py
with open('app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

app_code = app_code.replace('return dashboard_view(page).controls', 'return dashboard_view(page)')
app_code = app_code.replace('return estoque_view(page).controls', 'return estoque_view(page)')
app_code = app_code.replace('return compras_view(page).controls', 'return compras_view(page)')
app_code = app_code.replace('return historico_view(page).controls', 'return historico_view(page)')
app_code = app_code.replace('return configuracoes_view(page).controls', 'return configuracoes_view(page)')
app_code = app_code.replace('main_container.content = ft.Column(controls, expand=True)', 'main_container.content = controls')
app_code = app_code.replace('def get_view_controls', 'def get_view')
app_code = app_code.replace('controls = get_view_controls(idx)', 'controls = get_view(idx)')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

for file in glob.glob('views/*.py'):
    with open(file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    code = code.replace('-> ft.View:', '-> ft.Container:')
    
    # We replace the exact patterns of return ft.View( ... )
    code = re.sub(r'return ft\.View\(\s*\"/.*?\",\s*\[(.*?)\](?:,\s*scroll=ft\.ScrollMode\.AUTO)?(?:,\s*padding=20)?\s*\)',
                  r'return ft.Container(content=ft.Column([\1], scroll=ft.ScrollMode.AUTO, expand=True), padding=20, expand=True)',
                  code, flags=re.DOTALL)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(code)
