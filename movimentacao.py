import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

# Configuração do CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Conexão com o banco MySQL
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="library_db"
    )

# Função para carregar clientes
def carregar_clientes():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente, nome FROM cliente")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados

# Função para carregar livros (sem estoque)
def carregar_livros():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id_livro, titulo FROM livro")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados

# Registrar movimentação
def registrar_movimentacao():
    cliente_info = combo_cliente.get()
    livro_info = combo_livro.get()
    tipo = combo_tipo.get()
    valor = entry_valor.get()
    devolucao = entry_devolucao.get()

    if not cliente_info or not livro_info or not tipo:
        messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
        return

    cliente_id = cliente_info.split(" - ")[0]
    livro_id = livro_info.split(" - ")[0]

    data_operacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = conectar_bd()
    cursor = conn.cursor()

    if tipo == "venda":
        try:
            valor_float = float(valor)
            if valor_float <= 0:
                raise ValueError
        except:
            messagebox.showerror("Erro", "Informe um valor válido para a venda.")
            conn.close()
            return
        cursor.execute(
            "INSERT INTO movimentacao (tipo, id_cliente, id_livro, valor, data_operacao, status) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (tipo, cliente_id, livro_id, valor_float, data_operacao, "finalizado")
        )
    else:  # empréstimo
        if not devolucao:
            messagebox.showerror("Erro", "Informe a data de devolução para o empréstimo.")
            conn.close()
            return
        cursor.execute(
            "INSERT INTO movimentacao (tipo, id_cliente, id_livro, data_operacao, prazo_devolucao, status) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (tipo, cliente_id, livro_id, data_operacao, devolucao, "aberto")
        )

    conn.commit()
    cursor.close()
    conn.close()

    messagebox.showinfo("Sucesso", "Movimentação registrada com sucesso!")
    form_reset()

# Resetar formulário
def form_reset():
    combo_cliente.set("")
    combo_livro.set("")
    combo_tipo.set("")
    entry_valor.delete(0, ctk.END)
    entry_devolucao.delete(0, ctk.END)
    campo_valor.grid_remove()
    campo_devolucao.grid_remove()

# Atualizar campos dependendo do tipo
def atualiza_campos(choice):
    if choice == "venda":
        campo_valor.grid(row=3, column=0, columnspan=2, pady=5)
        campo_devolucao.grid_remove()
    elif choice == "emprestimo":
        campo_devolucao.grid(row=3, column=0, columnspan=2, pady=5)
        campo_valor.grid_remove()
    else:
        campo_valor.grid_remove()
        campo_devolucao.grid_remove()

# Janela principal
root = ctk.CTk()
root.title("Registrar Venda/Empréstimo")
root.geometry("450x400")

# Formulário
form_frame = ctk.CTkFrame(root, corner_radius=10)
form_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Clientes
ctk.CTkLabel(form_frame, text="Cliente:").grid(row=0, column=0, sticky="w", pady=5)
clientes = carregar_clientes()
combo_cliente = ctk.CTkComboBox(form_frame, values=[f"{id} - {nome}" for id, nome in clientes])
combo_cliente.grid(row=0, column=1, pady=5)

# Livros
ctk.CTkLabel(form_frame, text="Livro:").grid(row=1, column=0, sticky="w", pady=5)
livros = carregar_livros()
combo_livro = ctk.CTkComboBox(form_frame, values=[f"{id} - {titulo}" for id, titulo in livros])
combo_livro.grid(row=1, column=1, pady=5)

# Tipo
ctk.CTkLabel(form_frame, text="Tipo:").grid(row=2, column=0, sticky="w", pady=5)
combo_tipo = ctk.CTkComboBox(form_frame, values=["venda", "emprestimo"], command=atualiza_campos)
combo_tipo.grid(row=2, column=1, pady=5)

# Campos dinâmicos
campo_valor = ctk.CTkFrame(form_frame)
ctk.CTkLabel(campo_valor, text="Valor (R$):").pack(side="top", anchor="w", pady=2)
entry_valor = ctk.CTkEntry(campo_valor)
entry_valor.pack(fill="x", pady=2)

campo_devolucao = ctk.CTkFrame(form_frame)
ctk.CTkLabel(campo_devolucao, text="Prazo de Devolução:").pack(side="top", anchor="w", pady=2)
entry_devolucao = ctk.CTkEntry(campo_devolucao)
entry_devolucao.pack(fill="x", pady=2)

# Botão de registrar
btn_registrar = ctk.CTkButton(form_frame, text="Registrar", command=registrar_movimentacao)
btn_registrar.grid(row=4, column=0, columnspan=2, pady=20)

root.mainloop()
