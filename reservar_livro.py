import customtkinter as ctk
import mysql.connector
from tkinter import messagebox

# ----------------------------
# Função para conectar ao banco
# ----------------------------
def conectar_banco():
    try:
        conn = mysql.connector.connect(
            host="localhost",      # Ajuste conforme seu ambiente
            database="library_db", # Nome do banco
            user="root",           # Usuário
            password=""            # Senha
        )
        if conn.is_connected():
            return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

# ----------------------------
# Função para realizar reserva
# ----------------------------
def reservar_exemplar():
    cliente_nome = combo_cliente.get()
    livro_nome = combo_livro.get()
    data_reserva = entry_data.get()

    # Validação
    if not cliente_nome or not livro_nome or not data_reserva:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return

    # Obter ID do cliente
    cliente_id = None
    for id_cliente, nome in clientes.items():
        if nome == cliente_nome:
            cliente_id = int(id_cliente)  # garantir inteiro
            break

    if cliente_id is None:
        messagebox.showerror("Erro", "Cliente inválido.")
        return

    # Conectar banco
    conn = conectar_banco()
    if conn:
        cursor = conn.cursor()

        # Obter id_livro e estoque
        cursor.execute("SELECT id_livro, quantidade_estoque FROM livro WHERE titulo = %s", (livro_nome,))
        livro = cursor.fetchone()

        if not livro:
            messagebox.showerror("Erro", "Livro não encontrado.")
            conn.close()
            return

        livro_id, quantidade_estoque = livro

        if quantidade_estoque < 1:
            messagebox.showerror("Erro", f"O livro '{livro_nome}' está indisponível no momento.")
            conn.close()
            return

        try:
            # Inserir reserva
            cursor.execute(
                "INSERT INTO reserva (id_cliente, id_livro, data_reserva) VALUES (%s, %s, %s)",
                (cliente_id, livro_id, data_reserva)
            )
            conn.commit()

            # Atualizar estoque
            cursor.execute(
                "UPDATE livro SET quantidade_estoque = quantidade_estoque - 1 WHERE id_livro = %s",
                (livro_id,)
            )
            conn.commit()

            messagebox.showinfo("Sucesso", "Reserva realizada com sucesso!")

            # Reset campos
            combo_cliente.set("")
            combo_livro.set("")
            entry_data.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("Erro", str(e))

        cursor.close()
        conn.close()

# ----------------------------
# Interface
# ----------------------------
app = ctk.CTk()
app.title("Reservar Exemplar")
app.geometry("500x400")

# Clientes simulados (pode vir de tabela 'cliente')
clientes = {
    "1": "Carlos Silva",
    "2": "Ana Souza"
}

# Buscar livros do banco
livros_db = []
conn = conectar_banco()
if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT id_livro, titulo FROM livro")
    livros_db = cursor.fetchall()
    cursor.close()
    conn.close()

# Montar dicionário {titulo: id}
livros = {titulo: str(id_livro) for id_livro, titulo in livros_db}

# ----------------------------
# Widgets
# ----------------------------
container = ctk.CTkFrame(app)
container.pack(padx=20, pady=20, expand=True)

label_cliente = ctk.CTkLabel(container, text="Cliente:")
label_cliente.pack(pady=5)
combo_cliente = ctk.CTkComboBox(container, values=[cliente for cliente in clientes.values()])
combo_cliente.pack(pady=5)

label_livro = ctk.CTkLabel(container, text="Livro:")
label_livro.pack(pady=5)
combo_livro = ctk.CTkComboBox(container, values=[titulo for titulo in livros.keys()])
combo_livro.pack(pady=5)

label_data = ctk.CTkLabel(container, text="Data da Reserva (YYYY-MM-DD):")
label_data.pack(pady=5)
entry_data = ctk.CTkEntry(container, placeholder_text="2025-10-01")
entry_data.pack(pady=5)

botao_confirmar = ctk.CTkButton(container, text="Confirmar Reserva", command=reservar_exemplar)
botao_confirmar.pack(pady=20)

# ----------------------------
# Rodar apenas quando chamado
# ----------------------------
if __name__ == "__main__":
    app.mainloop()
