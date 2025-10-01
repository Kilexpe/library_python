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


# Carregar clientes do banco
def carregar_clientes():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente, nome FROM cliente")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados


# Buscar histórico de movimentações do cliente
def buscar_historico(cliente_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT l.titulo, m.tipo, m.data_operacao, m.status
        FROM movimentacao m
        JOIN livro l ON m.id_livro = l.id_livro
        WHERE m.id_cliente = %s
        ORDER BY m.data_operacao DESC
    """, (cliente_id,))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados


# Atualizar tabela
def atualizar_tabela(cliente_info):
    cliente_id = cliente_info.split(" - ")[0] if cliente_info else None

    # Limpar tabela
    for row in tabela.get_children():
        tabela.delete(row)

    if not cliente_id:
        mensagem_label.configure(text="")
        return

    historico = buscar_historico(cliente_id)
    if not historico:
        mensagem_label.configure(text="Nenhum histórico encontrado para este cliente.")
        return

    for titulo, tipo, data_op, status in historico:
        data_str = data_op.strftime("%Y-%m-%d %H:%M:%S") if isinstance(data_op, datetime) else str(data_op)
        tabela.insert("", "end", values=(titulo, tipo.capitalize(), data_str, status.capitalize()))

    mensagem_label.configure(text="")


# Janela principal
root = ctk.CTk()
root.title("Histórico de Livros por Cliente")
root.geometry("700x500")

# Frame principal
container = ctk.CTkFrame(root, corner_radius=10)
container.pack(padx=20, pady=20, fill="both", expand=True)

ctk.CTkLabel(container, text="Selecione o Cliente:").pack(anchor="w", pady=(0, 5))

clientes = carregar_clientes()
combo_cliente = ctk.CTkComboBox(container, values=[f"{id} - {nome}" for id, nome in clientes], command=atualizar_tabela)
combo_cliente.pack(fill="x", pady=5)

# Tabela
import tkinter.ttk as ttk

tabela = ttk.Treeview(container, columns=("Livro", "Tipo", "Data", "Status"), show="headings")
tabela.heading("Livro", text="Livro")
tabela.heading("Tipo", text="Tipo")
tabela.heading("Data", text="Data")
tabela.heading("Status", text="Status")
tabela.pack(fill="both", expand=True, pady=10)

# Mensagem
mensagem_label = ctk.CTkLabel(container, text="", text_color="#666")
mensagem_label.pack(anchor="w", pady=5)

root.mainloop()
