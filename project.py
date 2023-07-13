import tkinter as tk
from tkinter import messagebox, filedialog
from private_window import PrivateWindow
from dbpostgres import Database
import psycopg2

db = Database()
global usuario_global

# Login Window
login_window = tk.Tk()
login_window.title('SADPUnB - Login')
login_window.geometry('700x350')

# Sign In
def signIn():
    if usuario_text.get() == '' or senha_text.get() == '':
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return
    
    all_usuarios = db.fetch_usuario()
    matriculas = [sublist[4] for sublist in all_usuarios]
    if usuario_text.get() not in matriculas:
        messagebox.showerror("Erro", "Usuário não encontrado!")
        return
    
    indexMatricula = matriculas.index(usuario_text.get())
    senhas = [sublist[3] for sublist in all_usuarios]

    if senha_text.get() != senhas[indexMatricula]:
        messagebox.showerror("Erro", "Senha incorreta para esta matricula!")
        return
    



    usuario_global = usuario_text.get()
    private_window = PrivateWindow(login_window, usuario_global)
    private_window.grab_set()

# Sign Up
def signUp():
    if nome_text.get() == '' or create_senha_text.get() == '' or email_text.get() == '' or matricula_text.get() == '' or curso_text.get() == '' or var2.get() == 0:
        messagebox.showerror("Erro", "Preencha todos os campos da criação de conta!")
        print(nome_text.get() + senha_text.get() + email_text.get() + matricula_text.get() + curso_text.get() + str(var2.get()))
        return
    db.insert_usuario(nome_text.get(), email_text.get(), create_senha_text.get(), matricula_text.get(), curso_text.get(), var2.get(), filename)
    usuario_global = matricula_text.get()
    private_window = PrivateWindow(login_window, usuario_global)
    private_window.grab_set()

# Upload Image
def upload(event=None):
    global filename
    filepath = filedialog.askopenfilename()
    print(filepath)
    drawing = open(filepath, 'rb').read()
    filename = psycopg2.Binary(drawing)
    print("Selecionado:", filename)

linha = 0
# Login Label
login_label = tk.Label(login_window, text='LOGIN', font=('bold', 20), pady=20)
login_label.grid(row=linha, column=0, sticky=tk.W)

# Sign In Label
signIn_label = tk.Label(login_window, text='CRIAR CONTA', font=('bold', 20), pady=20, padx=100)
signIn_label.grid(row=linha, column=2, sticky=tk.E, columnspan=2)

linha += 1

# Usuario
usuario_text = tk.StringVar()
usuario_label = tk.Label(login_window, text='Matricula', font=('bold', 14))
usuario_label.grid(row=linha, column=0, sticky=tk.W)
usuario_entry = tk.Entry(login_window, textvariable=usuario_text)
usuario_entry.grid(row=linha, column=1)
# nome
nome_text = tk.StringVar()
nome_label = tk.Label(login_window, text='Nome', font=('bold', 14))
nome_label.grid(row=linha, column=2, sticky=tk.E)
nome_entry = tk.Entry(login_window, textvariable=nome_text)
nome_entry.grid(row=linha, column=3, sticky=tk.W)
linha += 1

# Senha
senha_text = tk.StringVar()
senha_label = tk.Label(login_window, text='Senha', font=('bold', 14))
senha_label.grid(row=linha, column=0, sticky=tk.W)
senha_entry = tk.Entry(login_window, textvariable=senha_text)
senha_entry.grid(row=linha, column=1)

# Email
email_text = tk.StringVar()
email_label = tk.Label(login_window, text='Email', font=('bold', 14))
email_label.grid(row=linha, column=2, sticky=tk.E)
email_entry = tk.Entry(login_window, textvariable=email_text)
email_entry.grid(row=linha, column=3, sticky=tk.W)
linha += 1

# Create Senha
create_senha_text = tk.StringVar()
create_senha_label = tk.Label(login_window, text='Senha', font=('bold', 14))
create_senha_label.grid(row=linha, column=2, sticky=tk.E)
create_senha_entry = tk.Entry(login_window, textvariable=create_senha_text)
create_senha_entry.grid(row=linha, column=3, sticky=tk.W)
linha += 1

# Matricula
matricula_text = tk.StringVar()
matricula_label = tk.Label(login_window, text='Matricula', font=('bold', 14))
matricula_label.grid(row=linha, column=2, sticky=tk.E)
matricula_entry = tk.Entry(login_window, textvariable=matricula_text)
matricula_entry.grid(row=linha, column=3, sticky=tk.W)
linha += 1

# Sign In Button
signIn_btn = tk.Button(login_window, text='Entrar', command=signIn)
signIn_btn.grid(row=linha, column=0, sticky=tk.W)

# Curso
curso_text = tk.StringVar()
curso_label = tk.Label(login_window, text='Curso', font=('bold', 14))
curso_label.grid(row=linha, column=2, sticky=tk.E)
curso_entry = tk.Entry(login_window, textvariable=curso_text)
curso_entry.grid(row=linha, column=3, sticky=tk.W)
linha += 1

# Radio Button USUARIO
var2 = tk.IntVar()
radio_btn_aluno = tk.Radiobutton(login_window, text='Usuário', variable=var2, value=1)
radio_btn_aluno.grid(row=linha, column=2, sticky=tk.E)
linha += 1

# Radio Button ADMIN
radio_btn_admin = tk.Radiobutton(login_window, text='Admin', variable=var2, value=2)
radio_btn_admin.grid(row=linha, column=2, sticky=tk.E)
linha += 1

# Adicionar foto Button
add_img_button = tk.Button(login_window, text='Adicionar Imagem de Perfil', command=upload)
add_img_button.grid(row=linha, column=2, sticky=tk.E)
linha += 1

# Sign Up Button
signUp_btn = tk.Button(login_window, text='Criar Conta', command=signUp)
signUp_btn.grid(row=linha, column=2, sticky=tk.E)
linha += 1



# Build
login_window.mainloop()