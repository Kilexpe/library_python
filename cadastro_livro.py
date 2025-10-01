import customtkinter as ctk
import mysql.connector
from mysql.connector import Error

# Função para conectar ao banco de dados MySQL
def conectar_banco():
    try:
        conn = mysql.connector.connect(
            host='localhost',       # Substitua pelo seu host
            database='library_db',   # Substitua pelo seu nome de banco de dados
            user='root',     # Substitua pelo seu usuário do MySQL
            password='123456'    # Substitua pela sua senha
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para salvar os dados do livro no banco de dados
def salvar_livro():
    titulo = entry_titulo.get().strip()
    autor = entry_autor.get().strip()
    isbn = entry_isbn.get().strip()
    quantidade = entry_quantidade.get()
    observacoes = entry_observacoes.get().strip()

    if not titulo or not quantidade.isdigit() or int(quantidade) < 1:
        label_mensagem.configure(text="Preencha corretamente os campos obrigatórios.", text_color="red")
        return

    # Conectar ao banco de dados e inserir os dados
    conn = conectar_banco()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO livro (titulo, autor, isbn, quantidade_estoque, observacoes)
                VALUES (%s, %s, %s, %s, %s)
            """, (titulo, autor, isbn, int(quantidade), observacoes))
            conn.commit()
            label_mensagem.configure(text="Livro cadastrado com sucesso!", text_color="green")
            # Limpar os campos após salvar
            entry_titulo.delete(0, 'end')
            entry_autor.delete(0, 'end')
            entry_isbn.delete(0, 'end')
            entry_quantidade.delete(0, 'end')
            entry_observacoes.delete(0, 'end')
        except Error as e:
            label_mensagem.configure(text=f"Erro ao salvar o livro: {e}", text_color="red")
        finally:
            cursor.close()
            conn.close()
    else:
        label_mensagem.configure(text="Erro ao conectar ao banco de dados.", text_color="red")

# Criação da interface gráfica com customtkinter
app = ctk.CTk()
app.title("Cadastro de Livro")
app.geometry("400x400")

# Container do formulário
frame_formulario = ctk.CTkFrame(app)
frame_formulario.pack(padx=20, pady=20, expand=True)

# Labels e campos de entrada
label_titulo = ctk.CTkLabel(frame_formulario, text="Título")
label_titulo.pack(pady=5)
entry_titulo = ctk.CTkEntry(frame_formulario)
entry_titulo.pack(pady=5)

label_autor = ctk.CTkLabel(frame_formulario, text="Autor")
label_autor.pack(pady=5)
entry_autor = ctk.CTkEntry(frame_formulario)
entry_autor.pack(pady=5)

label_isbn = ctk.CTkLabel(frame_formulario, text="ISBN")
label_isbn.pack(pady=5)
entry_isbn = ctk.CTkEntry(frame_formulario)
entry_isbn.pack(pady=5)

label_quantidade = ctk.CTkLabel(frame_formulario, text="Quantidade em estoque")
label_quantidade.pack(pady=5)
entry_quantidade = ctk.CTkEntry(frame_formulario)
entry_quantidade.pack(pady=5)

label_observacoes = ctk.CTkLabel(frame_formulario, text="Observações (opcional)")
label_observacoes.pack(pady=5)
entry_observacoes = ctk.CTkEntry(frame_formulario)
entry_observacoes.pack(pady=5)

# Botão de salvar
botao_salvar = ctk.CTkButton(frame_formulario, text="Salvar", command=salvar_livro)
botao_salvar.pack(pady=20)

# Mensagem de feedback
label_mensagem = ctk.CTkLabel(frame_formulario, text="")
label_mensagem.pack(pady=10)

# Iniciar a interface
app.mainloop()
