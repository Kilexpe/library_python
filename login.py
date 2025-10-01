import customtkinter as ctk
import mysql.connector
from mysql.connector import Error
import subprocess


# Função para conectar ao banco de dados MySQL
def conectar_banco():
    try:
        conn = mysql.connector.connect(
            host='localhost',  # Substitua pelo seu host
            database='library_db',  # Substitua pelo seu nome de banco de dados
            user='root',  # Substitua pelo seu usuário do MySQL
            password='123456'  # Substitua pela sua senha
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


# Função para verificar o login
def verificar_login():
    email = entry_email.get()
    senha = entry_senha.get()

    conn = conectar_banco()

    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE email = %s AND senha = %s", (email, senha))
        usuario = cursor.fetchone()

        if usuario:
            # Salva os dados do usuário
            nome_usuario = usuario[1]
            tipo_usuario = usuario[4]

            label_status.configure(text="Login bem-sucedido!", text_color="green")
            app.quit()  # Fecha a janela de login

            # Passa os dados para o dashboard via linha de comando
            subprocess.Popen(['python', 'dashboard.py', nome_usuario, tipo_usuario])

        else:
            label_status.configure(text="Credenciais inválidas. Tente novamente.", text_color="red")

        cursor.close()
        conn.close()
    else:
        label_status.configure(text="Erro ao conectar ao banco de dados.", text_color="red")


# Configuração da interface gráfica
app = ctk.CTk()
app.title("Login")
app.geometry("400x300")

# Labels e entradas
label_email = ctk.CTkLabel(app, text="E-mail:")
label_email.pack(pady=10)

entry_email = ctk.CTkEntry(app)
entry_email.pack(pady=10)

label_senha = ctk.CTkLabel(app, text="Senha:")
label_senha.pack(pady=10)

entry_senha = ctk.CTkEntry(app, show="*")
entry_senha.pack(pady=10)

# Botão de login
botao_entrar = ctk.CTkButton(app, text="Entrar", command=verificar_login)
botao_entrar.pack(pady=20)

# Label para mostrar o status do login
label_status = ctk.CTkLabel(app, text="")
label_status.pack(pady=10)

# Iniciar a interface
app.mainloop()
