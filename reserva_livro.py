import customtkinter as ctk
import mysql.connector
from tkinter import messagebox


# Função para conectar ao banco de dados MySQL
def conectar_banco():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Substitua pelo seu host
            database="library_db",  # Substitua pelo nome do seu banco de dados
            user="root",  # Substitua pelo seu usuário do MySQL
            password="123456"  # Substitua pela sua senha
        )
        if conn.is_connected():
            return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None


# Função para realizar a reserva
def reservar_exemplar():
    cliente_nome = combo_cliente.get()  # Nome do cliente selecionado
    livro_nome = combo_livro.get()      # Nome do livro selecionado
    data_reserva = entry_data.get()     # Data da reserva

    # Validação dos campos
    if not cliente_nome or not livro_nome or not data_reserva:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return

    # Encontrar o ID do cliente a partir do nome
    cliente_id = None
    for id_cliente, nome in clientes.items():
        if nome == cliente_nome:
            cliente_id = id_cliente
            break

    if cliente_id is None:
        messagebox.showerror("Erro", "Cliente selecionado inválido.")
        return

    # Conectar ao banco de dados
    conn = conectar_banco()
    if conn:
        cursor = conn.cursor()

        # Consultar o id_livro baseado no nome do livro
        cursor.execute("SELECT id_livro, quantidade_estoque FROM livro WHERE titulo = %s", (livro_nome,))
        livro = cursor.fetchone()

        if not livro:
            messagebox.showerror("Erro", "Livro não encontrado.")
            conn.close()
            return

        livro_id = livro[0]
        quantidade_estoque = livro[1]

        if quantidade_estoque < 1:
            messagebox.showerror("Erro", f"O livro '{livro_nome}' está indisponível no momento.")
            conn.close()
            return

        # Registra a reserva
        cursor.execute("INSERT INTO reserva (id_cliente, id_livro, data_reserva) VALUES (%s, %s, %s)",
                       (cliente_id, livro_id, data_reserva))
        conn.commit()

        # Atualiza o estoque do livro
        cursor.execute("UPDATE livro SET quantidade_estoque = quantidade_estoque - 1 WHERE id_livro = %s", (livro_id,))
        conn.commit()

        # Sucesso
        messagebox.showinfo("Sucesso", "Reserva realizada com sucesso!")

        # Limpa os campos
        combo_cliente.set("")
        combo_livro.set("")
        entry_data.delete(0, 'end')

        cursor.close()
        conn.close()



# Criação da interface gráfica
app = ctk.CTk()
app.title("Reservar Exemplar")
app.geometry("500x400")

# Dados de clientes (simulados)
clientes = {
    "1": "Carlos Silva",
    "2": "Ana Souza"
}

# Conectar ao banco para obter os livros
conn = conectar_banco()
if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT id_livro, titulo FROM livro")
    livros_db = cursor.fetchall()
    cursor.close()
    conn.close()

# Preparando dados para exibir no combo de livros
# Mapeamos id_livro como chave e título como valor para exibição
livros = {livro[1]: str(livro[0]) for livro in livros_db}  # chave é o título e valor é o id_livro
print(livros)
# Container para o formulário
container = ctk.CTkFrame(app)
container.pack(padx=20, pady=20, expand=True)

# Label e combo de cliente
label_cliente = ctk.CTkLabel(container, text="Cliente:")
label_cliente.pack(pady=5)
combo_cliente = ctk.CTkComboBox(container, values=[cliente for cliente in clientes.values()])
combo_cliente.pack(pady=5)

# Label e combo de livro
label_livro = ctk.CTkLabel(container, text="Livro:")
label_livro.pack(pady=5)

# A lista de livros é criada exibindo o título, mas o valor será o id_livro
combo_livro = ctk.CTkComboBox(container, values=[titulo for titulo in livros.keys()])
combo_livro.pack(pady=5)

# Label e input de data
label_data = ctk.CTkLabel(container, text="Data da Reserva:")
label_data.pack(pady=5)
entry_data = ctk.CTkEntry(container, placeholder_text="Escolha a data")
entry_data.pack(pady=5)

# Botão de confirmação de reserva
botao_confirmar = ctk.CTkButton(container, text="Confirmar Reserva", command=reservar_exemplar)
botao_confirmar.pack(pady=20)

# Iniciar a interface
app.mainloop()
