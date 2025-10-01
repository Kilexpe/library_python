import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import tkinter.ttk as ttk

# Configuração CustomTkinter
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


# Função para buscar movimentações por período
def buscar_movimentacoes():
    data_ini = entry_data_ini.get()
    data_fim = entry_data_fim.get()

    # Validação das datas
    try:
        dt_ini = datetime.strptime(data_ini, "%Y-%m-%d")
        dt_fim = datetime.strptime(data_fim, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Erro", "Digite datas válidas no formato YYYY-MM-DD.")
        return

    conn = conectar_bd()
    cursor = conn.cursor()
    query = """
        SELECT c.nome, l.titulo, m.tipo, m.valor, m.data_operacao, m.prazo_devolucao, m.status
        FROM movimentacao m
        JOIN cliente c ON m.id_cliente = c.id_cliente
        JOIN livro l ON m.id_livro = l.id_livro
        WHERE m.data_operacao BETWEEN %s AND %s
        ORDER BY m.data_operacao ASC
    """
    cursor.execute(query, (dt_ini, dt_fim))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    # Limpar tabela
    for row in tabela.get_children():
        tabela.delete(row)

    if not resultados:
        mensagem_label.configure(text="Nenhuma movimentação encontrada nesse período.")
        return

    # Preencher tabela
    for nome, titulo, tipo, valor, data_op, prazo_dev, status in resultados:
        data_str = data_op.strftime("%Y-%m-%d %H:%M:%S") if isinstance(data_op, datetime) else str(data_op)
        prazo_str = prazo_dev.strftime("%Y-%m-%d") if isinstance(prazo_dev, datetime) else (
            str(prazo_dev) if prazo_dev else "")
        valor_str = f"R$ {valor:.2f}" if valor else ""
        tabela.insert("", "end",
                      values=(nome, titulo, tipo.capitalize(), valor_str, data_str, prazo_str, status.capitalize()))

    mensagem_label.configure(text=f"{len(resultados)} movimentação(ões) encontradas.")


# Janela principal
root = ctk.CTk()
root.title("Relatório de Movimentações por Período")
root.geometry("900x500")

# Frame principal
frame = ctk.CTkFrame(root, corner_radius=10)
frame.pack(padx=20, pady=20, fill="both", expand=True)

# Inputs de data
ctk.CTkLabel(frame, text="Data Inicial (YYYY-MM-DD):").pack(anchor="w")
entry_data_ini = ctk.CTkEntry(frame)
entry_data_ini.pack(fill="x", pady=(0, 10))

ctk.CTkLabel(frame, text="Data Final (YYYY-MM-DD):").pack(anchor="w")
entry_data_fim = ctk.CTkEntry(frame)
entry_data_fim.pack(fill="x", pady=(0, 10))

# Botão de buscar
btn_buscar = ctk.CTkButton(frame, text="Gerar Relatório", command=buscar_movimentacoes)
btn_buscar.pack(pady=10)

# Tabela
tabela = ttk.Treeview(frame, columns=("Cliente", "Livro", "Tipo", "Valor", "Data", "Prazo Devolução", "Status"),
                      show="headings")
for col in tabela["columns"]:
    tabela.heading(col, text=col)
tabela.pack(fill="both", expand=True, pady=10)

# Mensagem
mensagem_label = ctk.CTkLabel(frame, text="", text_color="#666")
mensagem_label.pack(anchor="w", pady=5)

root.mainloop()
