import customtkinter as ctk
import sys
import subprocess  # Importar subprocess para executar outros arquivos Python


# Função para montar o menu com base no tipo de usuário
def montar_menu(nome_usuario, tipo_usuario):
    # Exibir boas-vindas
    label_bemvindo.configure(text=f"Bem-vindo(a), {nome_usuario}!")

    # Definindo os botões comuns
    botoes_comuns = [
        {"texto": "Reservar Exemplar", "link": "reserva_livro.py"},  # Alterando para o script Python
        {"texto": "Editar/Cancelar Reserva", "link": "editar_reserva.html"},
        {"texto": "Registrar Venda/Empréstimo", "link": "movimentacao.html"},
        {"texto": "Histórico por Cliente", "link": "historico.html"},
        {"texto": "Logout", "link": "login.html"}
    ]

    # Definindo os botões específicos do gerente
    botoes_gerente = [
        {"texto": "Cadastrar Livro", "link": "cadastro_livro.py"},  # Modificar aqui
        {"texto": "Relatório por Período", "link": "relatorio.html"}
    ]

    # Montando o menu de acordo com o tipo de usuário
    botoes = botoes_comuns
    if tipo_usuario == "gerente":
        botoes += botoes_gerente

    # Criando os botões
    for btn in botoes:
        botao = ctk.CTkButton(frame_menu, text=btn["texto"], command=lambda link=btn["link"]: abrir_link(link))
        botao.pack(pady=5)


# Função para abrir o link ou executar o arquivo Python
def abrir_link(link):
    if link.endswith(".py"):
        # Se o link for um arquivo Python, executa o script
        subprocess.Popen([sys.executable, link])  # Executa o arquivo Python
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
