import customtkinter as ctk
import sys
import subprocess
import os

# Função para montar o menu com base no tipo de usuário
def montar_menu(nome_usuario, tipo_usuario):
    label_bemvindo.configure(text=f"Bem-vindo(a), {nome_usuario}!")

    botoes_comuns = [
        {"texto": "Reservar Exemplar", "link": "reservar_livro.py"},
        {"texto": "Editar/Cancelar Reserva", "link": "editar_reserva.py"},
        {"texto": "Registrar Venda/Empréstimo", "link": "movimentacao.py"},
        {"texto": "Histórico por Cliente", "link": "historico_cliente.py"},
        {"texto": "Logout", "link": "logout"}  # link especial para logout
    ]

    botoes_gerente = [
        {"texto": "Cadastrar Livro", "link": "cadastro_livro.py"},
        {"texto": "Relatório por Período", "link": "relatorio.py"}
    ]

    botoes = botoes_comuns
    if tipo_usuario == "gerente":
        botoes += botoes_gerente

    for btn in botoes:
        botao = ctk.CTkButton(frame_menu, text=btn["texto"],
                               command=lambda link=btn["link"]: abrir_link(link))
        botao.pack(pady=5)

# Função para abrir o link ou executar o arquivo Python
def abrir_link(link):
    if link == "logout":
        # Fecha o dashboard
        app.destroy()
        # Abre a tela de login novamente
        login_script = os.path.join(os.path.dirname(__file__), "login.py")
        subprocess.Popen([sys.executable, login_script])
    elif link.endswith(".py"):
        # Executa o outro script Python em paralelo
        subprocess.Popen([sys.executable, link, nome_usuario, tipo_usuario])
    else:
        print(f"Abrindo {link}")

# Criação da interface
app = ctk.CTk()
app.title("Dashboard - Sistema Livraria")
app.geometry("600x400")

# Pega os dados passados na linha de comando
nome_usuario = sys.argv[1]
tipo_usuario = sys.argv[2]

# Container para o conteúdo
frame_principal = ctk.CTkFrame(app)
frame_principal.pack(padx=20, pady=20, expand=True, fill="both")

# Label de boas-vindas
label_bemvindo = ctk.CTkLabel(frame_principal, text="Bem-vindo(a), Usuário!", font=("Arial", 18))
label_bemvindo.pack(pady=20)

# Frame para o menu
frame_menu = ctk.CTkFrame(frame_principal)
frame_menu.pack(pady=20, expand=True)

# Monta o menu com base no tipo de usuário
montar_menu(nome_usuario, tipo_usuario)

# Iniciar a interface
app.mainloop()
