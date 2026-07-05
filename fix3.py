import os
import glob
import re

for file in glob.glob('**/*.py', recursive=True):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix snackbar in dialogs.py
    if 'page.overlay.append(snack)
    snack.open = True
    page.update()' in content:
        content = content.replace('page.overlay.append(snack)
    snack.open = True
    page.update()', 'page.overlay.append(snack)\n    snack.open = True\n    page.update()')
    
    # Fix dialogs
    content = content.replace('page.show_dialog(dialog)', 'page.show_dialog(dialog)')
    content = content.replace('page.show_dialog(dialog_form)', 'page.show_dialog(dialog_form)')
    content = content.replace('page.show_dialog(dialog_add)', 'page.show_dialog(dialog_add)')
    content = content.replace('page.show_dialog(dialog_finalizar)', 'page.show_dialog(dialog_finalizar)')
    
    content = content.replace('page.pop_dialog()', 'page.pop_dialog()')
    content = content.replace('page.pop_dialog()', 'page.pop_dialog()')
    content = content.replace('page.pop_dialog()', 'page.pop_dialog()')
    content = content.replace('page.pop_dialog()', 'page.pop_dialog()')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
