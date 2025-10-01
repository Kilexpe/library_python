import customtkinter as ctk
import mysql.connector
from tkinter import messagebox

# Conexão com banco de dados MySQL
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="library_db"
)
cursor = conexao.cursor(dictionary=True)

# Funções
def carregar_reservas():
    for widget in frame_reservas.winfo_children():
        widget.destroy()

    # Busca reservas
    cursor.execute("SELECT * FROM reserva")
    reservas = cursor.fetchall()

    for reserva in reservas:
        frame = ctk.CTkFrame(frame_reservas)
        frame.pack(fill="x", pady=5, padx=5)

        # Mostrando id_cliente e id_livro
        ctk.CTkLabel(frame, text=f"Cliente ID: {reserva['id_cliente']}", width=120).pack(side="left", padx=5)
        ctk.CTkLabel(frame, text=f"Livro ID: {reserva['id_livro']}", width=120).pack(side="left", padx=5)

        # Campo para editar data da reserva
        entry_data = ctk.CTkEntry(frame, width=140)
        entry_data.insert(0, str(reserva["data_reserva"]))
        entry_data.pack(side="left", padx=5)

        # Campo para editar data prevista de retirada
        entry_prevista = ctk.CTkEntry(frame, width=140)
        entry_prevista.insert(0, str(reserva["data_retirada_prevista"]))
        entry_prevista.pack(side="left", padx=5)

        # Status
        ctk.CTkLabel(frame, text=reserva["status"], width=80).pack(side="left", padx=5)

        # Botões
        btn_salvar = ctk.CTkButton(
            frame, text="Salvar",
            fg_color="green",
            command=lambda rid=reserva["id_reserva"], e1=entry_data, e2=entry_prevista: salvar_reserva(rid, e1.get(), e2.get())
        )
        btn_salvar.pack(side="left", padx=5)

        btn_cancelar = ctk.CTkButton(
            frame, text="Cancelar",
            fg_color="orange",
            command=lambda rid=reserva["id_reserva"]: cancelar_reserva(rid)
        )
        btn_cancelar.pack(side="left", padx=5)

        btn_excluir = ctk.CTkButton(
            frame, text="Excluir",
            fg_color="red",
            command=lambda rid=reserva["id_reserva"]: excluir_reserva(rid)
        )
        btn_excluir.pack(side="left", padx=5)


def salvar_reserva(reserva_id, nova_data, nova_prevista):
    try:
        cursor.execute(
            "UPDATE reserva SET data_reserva=%s, data_retirada_prevista=%s WHERE id_reserva=%s",
            (nova_data, nova_prevista, reserva_id)
        )
        conexao.commit()
        messagebox.showinfo("Sucesso", f"Reserva {reserva_id} atualizada.")
        carregar_reservas()
    except Exception as e:
        messagebox.showerror("Erro", str(e))


def cancelar_reserva(reserva_id):
    try:
        cursor.execute(
            "UPDATE reserva SET status='cancelada' WHERE id_reserva=%s",
            (reserva_id,)
        )
        conexao.commit()
        messagebox.showinfo("Sucesso", f"Reserva {reserva_id} foi cancelada.")
        carregar_reservas()
    except Exception as e:
        messagebox.showerror("Erro", str(e))


def excluir_reserva(reserva_id):
    resposta = messagebox.askyesno("Confirmação", f"Deseja realmente excluir a reserva {reserva_id}?")
    if resposta:
        try:
            cursor.execute("DELETE FROM reserva WHERE id_reserva=%s", (reserva_id,))
            conexao.commit()
            messagebox.showinfo("Sucesso", f"Reserva {reserva_id} foi excluída.")
            carregar_reservas()
        except Exception as e:
            messagebox.showerror("Erro", str(e))


# Interface
app = ctk.CTk()
app.title("Editar, Cancelar ou Excluir Reservas")
app.geometry("900x400")

titulo = ctk.CTkLabel(app, text="Gerenciamento de Reservas", font=("Arial", 18, "bold"))
titulo.pack(pady=10)

frame_reservas = ctk.CTkScrollableFrame(app, width=2250, height=300)
frame_reservas.pack(pady=10)

# Carrega reservas ao iniciar
carregar_reservas()

app.mainloop()
