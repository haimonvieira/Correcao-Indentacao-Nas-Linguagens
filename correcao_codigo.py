import tkinter as tk
from tkinter import ttk
import parso
import autopep8


def corrigir_indentacao(codigo, linguagem):
    if linguagem == 'Python':
        return corrigir_indentacao_python(codigo)
    elif linguagem == 'Java' or linguagem == 'C':
        return corrigir_indentacao_c_java(codigo)
    else:
        return codigo

def corrigir_indentacao_python(codigo):
    try:
        fixed_code = autopep8.fix_code(codigo)
        return fixed_code
    except SyntaxError as e:
        return ""

def corrigir_indentacao_c_java(codigo):
    codigo_corrigido = ""
    nivel_indentacao = 0
    linhas = codigo.split('\n')
    for i in range(len(linhas)):
        linha = linhas[i].strip()

        if linha.endswith("}") or linha.endswith("};"):
            nivel_indentacao -= 1

        if linha:
            codigo_corrigido += "    " * nivel_indentacao + linha + "\n"

        if "{" in linha and not linha.endswith("}") and not linha.endswith("};"):
            nivel_indentacao += 1
    return codigo_corrigido

def copiar_codigo():
    root.clipboard_clear()
    root.clipboard_append(codigo_text.get('1.0', 'end'))

def toggle_dark_mode():
    if dark_var.get():
        root.configure(background='#2b2b2b')
        mainframe.configure(background='#2b2b2b')
        codigo_text.configure(bg='#2b2b2b', fg='#ffffff')
        style.configure('TCombobox', fieldbackground='#2b2b2b', foreground='#ffffff', background='#2b2b2b')
        style.configure("BW.TButton", foreground="#ffffff", background="#2b2b2b")
        style.map("BW.TButton", foreground=[('pressed', 'red'), ('active', 'blue')],
             background=[('pressed', '!disabled', 'black'), ('active', 'white')])
    else:
        root.configure(background='#f0f0f0')
        mainframe.configure(background='#f0f0f0')
        codigo_text.configure(bg='#ffffff', fg='#000000')
        style.configure('TCombobox', fieldbackground='#ffffff', foreground='#000000', background='#f0f0f0')
        style.configure("BW.TButton", foreground="black", background="#f0f0f0")
        style.map("BW.TButton", foreground=[('pressed', 'red'), ('active', 'blue')],
             background=[('pressed', '!disabled', 'black'), ('active', 'white')])


root = tk.Tk()
root.title("Corretor de Código")

style = ttk.Style()
style.theme_use("clam")
style.configure(".", font=("Helvetica", 16))
style.configure("BW.TButton", foreground="black", background="#f0f0f0")
style.map("BW.TButton", foreground=[('pressed', 'red'), ('active', 'blue')],
             background=[('pressed', '!disabled', 'black'), ('active', 'white')])

mainframe = tk.Frame(root, background='#f0f0f0', padx=10, pady=10)
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

codigo_text = tk.Text(mainframe, wrap=tk.NONE, width=80, height=20, font=("Helvetica", 16))
codigo_text.grid(column=0, row=1, sticky=(tk.W, tk.E, tk.N, tk.S))

scrollbar_y = ttk.Scrollbar(mainframe, orient=tk.VERTICAL, command=codigo_text.yview)
scrollbar_y.grid(column=1, row=1, sticky=(tk.N, tk.S))

scrollbar_x = ttk.Scrollbar(mainframe, orient=tk.HORIZONTAL, command=codigo_text.xview)
scrollbar_x.grid(column=0, row=2, sticky=(tk.W, tk.E))

codigo_text.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

linguagem_var = tk.StringVar()
linguagem_combobox = ttk.Combobox(mainframe, textvariable=linguagem_var, values=["Python", "Java", "C"], state="readonly", font=("Helvetica", 16))
linguagem_combobox.set("Python")
linguagem_combobox.grid(column=0, row=4, sticky=(tk.W, tk.E, tk.N, tk.S))

corrigir_button = ttk.Button(mainframe, text="Corrigir e Verificar", command=lambda: (codigo_text.get('1.0', 'end'), linguagem_var.get()), style="BW.TButton")
corrigir_button.grid(column=0, row=5, sticky=(tk.W, tk.E, tk.N, tk.S))

copiar_button = ttk.Button(mainframe, text="Copiar Código", command=copiar_codigo, style="BW.TButton")
copiar_button.grid(column=0, row=6, sticky=(tk.W, tk.E, tk.N, tk.S))

dark_var = tk.BooleanVar()
dark_mode_checkbutton = tk.Checkbutton(mainframe, text="Modo Noturno", variable=dark_var, command=toggle_dark_mode, font=("Helvetica", 16))
dark_mode_checkbutton.grid(column=0, row=7, sticky=(tk.W, tk.E, tk.N, tk.S))

root.mainloop()
