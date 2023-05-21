import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import parso
import autopep8
import javalang
from clang import cindex

def corrigir_indentacao(codigo, linguagem):
    if linguagem == 'Python':
        return corrigir_indentacao_python(codigo)
    elif linguagem == 'Java':
        return corrigir_indentacao_java(codigo)
    elif linguagem == 'C':
        return corrigir_indentacao_c(codigo)
    else:
        return codigo



def corrigir_indentacao_python(codigo):
    try:
        # Corrighe a indentação do código
        fixed_code = autopep8.fix_code(codigo)
        fixed_code_lines = fixed_code.split('\n')

        fixed_lines = fixed_code.split('\n')
        for i in range(1, len(fixed_code_lines)):
            if fixed_code_lines[i].strip().startswith("return"):
                fixed_code_lines[i] = ' ' * 4 + fixed_code_lines[i]

        # Une as linhas corrigidas
        return '\n'.join(fixed_lines)

    except SyntaxError as e:
        return False

def corrigir_indentacao_java(codigo):
    tree = javalang.parse.parse(codigo)
    return tree.accept(IndentVisitor())


def corrigir_indentacao_c(codigo):
    return cindex.format(codigo)


class IndentVisitor:
    def __init__(self):
        super().__init__()
        self.indentation_level = 0

    def visit(self, node):
        node._modified_indentation_level = self.indentation_level
        super().visit(node)

    def visit_ClassDeclaration(self, node):
        self.generic_visit(node)
        self.indentation_level += 1

    def visit_MethodDeclaration(self, node):
        self.generic_visit(node)
        self.indentation_level += 1

    def visit_BlockStatement(self, node):
        self.generic_visit(node)
        self.indentation_level -= 1

    def visit_IfStatement(self, node):
        self.generic_visit(node)
        self.indentation_level += 1

    def visit_ElseStatement(self, node):
        self.generic_visit(node)
        self.indentation_level -= 1

    def visit_ForStatement(self, node):
        self.generic_visit(node)
        self.indentation_level += 1

    def visit_WhileStatement(self, node):
        self.generic_visit(node)
        self.indentation_level += 1

    def visit_DoStatement(self, node):
        self.generic_visit(node)
        self.indentation_level += 1

    def visit_SwitchStatement(self, node):
        self.generic_visit(node)
        self.indentation_level += 1

    def visit_CaseGroup(self, node):
        self.generic_visit(node)
        self.indentation_level -= 1

    def visit_BreakStatement(self, node):
        self.generic_visit(node)
        self.indentation_level -= 1

    def visit_ReturnStatement(self, node):
        self.generic_visit(node)
        self.indentation_level -= 1

    def visit_ContinueStatement(self, node):
        self.generic_visit(node)
        self.indentation_level -= 1

    def visit_ThrowStatement(self, node):
        self.generic_visit(node)
        self.indentation_level -= 1

    def visit_TryStatement(self, node):
        self.generic_visit(node)
        self.indentation_level += 1

    def visit_CatchClause(self, node):
        self.generic_visit(node)
        self.indentation_level -= 1

    def visit_FinallyClause(self, node):
        self.generic_visit(node)
        self.indentation_level -= 1


def verificar_codigo(codigo):
    try:
        parso.parse(codigo)
        return None  # Retorna None quando não há erro de sintaxe
    except parso.ParserSyntaxError as e:
        return e.start_pos[0], e.start_pos[1], e.text



def corrigir_e_verificar_codigo(codigo, linguagem):
    global codigo_corrigido
    codigo_corrigido = corrigir_indentacao(codigo, linguagem)
    erro_sintaxe = verificar_codigo(codigo_corrigido)

    if codigo_corrigido:
        verificar_codigo(codigo_corrigido)
        codigo_text.delete('1.0', 'end')
        codigo_text.insert('1.0', codigo_corrigido)
        feedback_label.config(text="Código corrigido", fg="green")
    else:
        linha, coluna, texto = erro_sintaxe
        feedback_label.config(text=f"Erro de sintaxe na linha {linha}, coluna {coluna}: {texto}", fg="red")
        codigo_text.tag_configure("error", foreground="red")
        codigo_text.delete('1.0', 'end')
        codigo_text.insert('1.0', codigo_corrigido)
        codigo_text.tag_add("error", f"{linha}.{coluna}", f"{linha}.{coluna + len(texto)}")


def abrir_arquivo():
    arquivo = filedialog.askopenfilename(filetypes=[('Arquivos Python', '*.py')])
    if arquivo:
        with open(arquivo, 'r') as file:
            codigo = file.read()
        codigo_text.delete('1.0', 'end')
        codigo_text.insert('1.0', codigo)


def salvar_arquivo():
    arquivo = filedialog.asksaveasfilename(filetypes=[('Arquivos Python', '*.py')])
    if arquivo:
        if not arquivo.endswith('.py'):
            arquivo += '.py'
        with open(arquivo, 'w') as file:
            file.write(codigo_text.get('1.0', 'end-1c'))
        feedback_label.config(text="Código corrigido salvo", fg="green")


def limpar_codigo():
    codigo_text.delete('1.0', 'end')


def copiar_codigo():
    codigo = codigo_text.get('1.0', 'end-1c')
    janela.clipboard_clear()
    janela.clipboard_append(codigo)


# Cria a janela principal
janela = tk.Tk()
janela.title('Correção Automática de Código')

# Cria uma caixa de texto para inserir o código
codigo_text = tk.Text(janela, height=20, width=80)
codigo_text.pack()

# Cria a barra de rolagem para a caixa de texto
scrollbar = tk.Scrollbar(janela)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
codigo_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=codigo_text.yview)

# Crie um estilo
style = ttk.Style()
style.configure('TButton', font=('Arial', 12))
style.configure('TLabel', font=('Arial', 12))

# Cria os botões
corrigir_button = ttk.Button(janela, text='Corrigir', command=lambda: corrigir_e_verificar_codigo(codigo_text.get('1.0', 'end-1c'), linguagem_combobox.get()))
abrir_button = ttk.Button(janela, text='Abrir Arquivo', command=abrir_arquivo)
salvar_button = ttk.Button(janela, text='Salvar Arquivo', command=salvar_arquivo)
limpar_button = ttk.Button(janela, text='Limpar', command=limpar_codigo)
copiar_button = ttk.Button(janela, text='Copiar', command=copiar_codigo)

# Cria um rótulo para exibir o feedback
feedback_label = tk.Label(janela, text="", fg="green")
feedback_label.pack()

# Cria a lista suspensa para selecionar a linguagem
linguagem_label = ttk.Label(janela, text="Linguagem:")
linguagem_combobox = ttk.Combobox(janela, values=["Python", "Java", "C"], state="readonly")
linguagem_combobox.current(0)  # Define o valor padrão da lista suspensa
linguagem_label.pack()
linguagem_combobox.pack(pady=5)

# Defina um tamanho mínimo para a janela
janela.minsize(400, 300)

# Ajuste o espaçamento entre os elementos
codigo_text.pack(pady=10)
corrigir_button.pack(pady=5)
abrir_button.pack(pady=5)
salvar_button.pack(pady=5)
limpar_button.pack(pady=5)
copiar_button.pack(pady=5)
feedback_label.pack(pady=10)


# Inicia o loop principal da janela
janela.mainloop()
