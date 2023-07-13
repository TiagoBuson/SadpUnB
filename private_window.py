import tkinter as tk
from tkinter import ttk
from dbpostgres import Database
from tkinter import messagebox, PhotoImage
from PIL import ImageTk, Image
import io

db = Database()

class PrivateWindow(tk.Toplevel):

    def __init__(self, parent, usuario_global):
        super().__init__(parent)

        self.geometry('1400x600')
        self.title('SADPUnB')

        tabControl = ttk.Notebook(self)

        tab_conta = ttk.Frame(tabControl)
        tab_estudantes = ttk.Frame(tabControl)
        tab_turmas = ttk.Frame(tabControl)

        tabControl.add(tab_conta, text='Minha Conta')
        tabControl.add(tab_estudantes, text='Estudantes')
        tabControl.add(tab_turmas, text='Turmas')

        tabControl.pack(expand=1, fill='both')

        def clear_text():
            nome_entry.delete(0, tk.END)
            senha_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            matricula_entry.delete(0, tk.END)
            curso_entry.delete(0, tk.END)
            radio_btn_aluno.selection_clear
            radio_btn_admin.selection_clear
            avaliacao_entry.delete(0, tk.END)
            nota_entry.delete(0, tk.END)
            denuncia_entry.delete(0, tk.END)
            denuncia_avaliacao_entry.delete(0, tk.END)

        # MINHA CONTA
        user = db.fetch_usuario_global(usuario_global)
        linha = 0
        ttk.Label(tab_conta, text='Minha Conta', font=20).grid(row=linha, column=0, pady=10, sticky=tk.W)
        linha += 1
        ttk.Label(tab_conta, text='Nome: ', font=14).grid(row=linha, column=0, pady=10, sticky=tk.W)
        ttk.Label(tab_conta, text=user[0][1], font=14).grid(row=linha, column=1, pady=10, sticky=tk.W)
        linha += 1
        ttk.Label(tab_conta, text='Email: ', font=14).grid(row=linha, column=0, pady=10, sticky=tk.W)
        ttk.Label(tab_conta, text=user[0][2], font=14).grid(row=linha, column=1, pady=10, sticky=tk.W)
        linha += 1
        ttk.Label(tab_conta, text='Senha: ', font=14).grid(row=linha, column=0, pady=10, sticky=tk.W)
        ttk.Label(tab_conta, text=user[0][3], font=14).grid(row=linha, column=1, pady=10, sticky=tk.W)
        linha += 1
        ttk.Label(tab_conta, text='Matricula: ', font=14).grid(row=linha, column=0, pady=10, sticky=tk.W)
        ttk.Label(tab_conta, text=user[0][4], font=14).grid(row=linha, column=1, pady=10, sticky=tk.W)
        linha += 1
        ttk.Label(tab_conta, text='Curso: ', font=14).grid(row=linha, column=0, pady=10, sticky=tk.W)
        ttk.Label(tab_conta, text=user[0][5], font=14).grid(row=linha, column=1, pady=10, sticky=tk.W)
        linha += 1
        ttk.Label(tab_conta, text='Imagem de Perfil: ', font=14).grid(row=linha, column=0, pady=10, sticky=tk.W)
        # image = tk.PhotoImage(file=user[0][7])
        img = Image.open(io.BytesIO(user[0][7]))
        img = ImageTk.PhotoImage(img)
        img_label = tk.Label(tab_conta, image=img)
        img_label.grid(row=linha, column=0)
        linha += 1

        # ESTUDANTES
        linha = 0
        ttk.Label(tab_estudantes, text='Estudantes', font=20).grid(row=linha, column=0, pady=10, sticky=tk.W)
        linha += 1

        def select_estudante(event):
            try:
                global selected_estudante
                index = lista_estudantes.curselection()[0]
                selected_estudante = lista_estudantes.get(index)

                clear_text()
                nome_entry.insert(tk.END, selected_estudante[1])
                email_entry.insert(tk.END, selected_estudante[2])
                senha_entry.insert(tk.END, selected_estudante[3])
                matricula_entry.insert(tk.END, selected_estudante[4])
                curso_entry.insert(tk.END, selected_estudante[5])
                if selected_estudante[6] == 1:
                    radio_btn_aluno.select()
                if selected_estudante[6] == 2:
                    radio_btn_admin.select()
                
            except IndexError:
                pass

        # Lista
        lista_estudantes_label = ttk.Label(tab_estudantes, text='ID / Nome / Email / Senha / Matricula / Curso').grid(row=linha, column=0, pady=10)
        linha += 1
        lista_estudantes = tk.Listbox(tab_estudantes, height=8, width=100, border=0)
        lista_estudantes.grid(row=linha, column=0, columnspan=3, rowspan=2, padx=20)
        linha += 1

        def populate_lista_estudantes():
            lista_estudantes.delete(0, tk.END)
            for row in db.fetch_usuario():
                lista_estudantes.insert(tk.END, row)

        def add_estudante():
            if nome_text.get() == '' or senha_text.get() == '' or email_text.get() == '' or matricula_text.get() == '' or curso_text.get() == '' or var2.get() == 0:
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return
            db.insert_usuario(nome_text.get(), senha_text.get(), email_text.get(), matricula_text.get(), curso_text.get(), var2.get(), '')
            clear_text()
            populate_lista_estudantes()
            
        def remove_estudante():
            db.remove_usuario(selected_estudante[0])
            clear_text()
            populate_lista_estudantes()

        def update_estudante():
            if nome_text.get() == '' or senha_text.get() == '' or email_text.get() == '' or matricula_text.get() == '' or curso_text.get() == '' or var2.get() == 0:
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return
            db.update_usuario(selected_estudante[0], nome_text.get(), email_text.get(), senha_text.get(), matricula_text.get(), curso_text.get(), var2.get())
            populate_lista_estudantes()


        populate_lista_estudantes()

        # Create Scrollbar
        scrollbar_estudantes = tk.Scrollbar(tab_estudantes)
        scrollbar_estudantes.grid(row=linha, column=3)
        linha += 1

        # Set scroll to listbox
        lista_estudantes.configure(yscrollcommand=scrollbar_estudantes.set)
        scrollbar_estudantes.configure(command=lista_estudantes.yview)

        # Bind select
        lista_estudantes.bind('<<ListboxSelect>>', select_estudante)

        # nome
        nome_linha = linha
        nome_text = tk.StringVar()
        nome_label = tk.Label(tab_estudantes, text='Nome', font=('bold', 14))
        nome_label.grid(row=nome_linha, column=0, sticky=tk.W)
        nome_entry = tk.Entry(tab_estudantes, textvariable=nome_text)
        nome_entry.grid(row=linha, column=1, sticky=tk.W)
        linha += 1

        # Senha
        senha_text = tk.StringVar()
        senha_label = tk.Label(tab_estudantes, text='Senha', font=('bold', 14))
        senha_label.grid(row=linha, column=0, sticky=tk.W)
        senha_entry = tk.Entry(tab_estudantes, textvariable=senha_text)
        senha_entry.grid(row=linha, column=1, sticky=tk.W)
        linha += 1

        # Email
        email_text = tk.StringVar()
        email_label = tk.Label(tab_estudantes, text='Email', font=('bold', 14))
        email_label.grid(row=linha, column=0, sticky=tk.W)
        email_entry = tk.Entry(tab_estudantes, textvariable=email_text)
        email_entry.grid(row=linha, column=1, sticky=tk.W)
        linha += 1

        # Matricula
        matricula_text = tk.StringVar()
        matricula_label = tk.Label(tab_estudantes, text='Matricula', font=('bold', 14))
        matricula_label.grid(row=linha, column=0, sticky=tk.W)
        matricula_entry = tk.Entry(tab_estudantes, textvariable=matricula_text)
        matricula_entry.grid(row=linha, column=1, sticky=tk.W)
        linha += 1

        # Curso
        curso_text = tk.StringVar()
        curso_label = tk.Label(tab_estudantes, text='Curso', font=('bold', 14))
        curso_label.grid(row=linha, column=0, sticky=tk.W)
        curso_entry = tk.Entry(tab_estudantes, textvariable=curso_text)
        curso_entry.grid(row=linha, column=1, sticky=tk.W)
        linha += 1

        # Radio Button USUARIO
        var2 = tk.IntVar()
        radio_btn_aluno = tk.Radiobutton(tab_estudantes, text='Usuário', variable=var2, value=1)
        radio_btn_aluno.grid(row=linha, column=0, sticky=tk.W)
        linha += 1

        # Radio Button ADMIN
        radio_btn_admin = tk.Radiobutton(tab_estudantes, text='Admin', variable=var2, value=2)
        radio_btn_admin.grid(row=linha, column=0, sticky=tk.W)
        linha += 1
        
        # Buttons
        add_estudante_btn = tk.Button(tab_estudantes, text="Criar Estudante", width=20, command=add_estudante)
        add_estudante_btn.grid(row=nome_linha, column=2)

        remove_estudante_btn = tk.Button(tab_estudantes, text='Remover Estudante', width=20, command=remove_estudante)
        remove_estudante_btn.grid(row=nome_linha+1, column=2)

        update_estudante_btn = tk.Button(tab_estudantes, text='Atualizar Estudante', width=20, command=update_estudante)
        update_estudante_btn.grid(row=nome_linha+2, column=2)

        clear_estudante_btn = tk.Button(tab_estudantes, text='Limpar', width=20, command=clear_text)
        clear_estudante_btn.grid(row=nome_linha+3, column=2)

        # TURMAS
        linha = 0
        ttk.Label(tab_turmas, text='Turmas', font=20).grid(row=linha, column=0, pady=10, sticky=tk.W)
        linha += 1
        
        def select_turma(event):
            try:
                global selected_turma
                index = lista_turmas.curselection()[0]
                selected_turma = lista_turmas.get(index)

                clear_text()
                populate_lista_aval(selected_turma[0])
                # nome_entry.insert(tk.END, selected_turma[1])
                # email_entry.insert(tk.END, selected_turma[2])
                # senha_entry.insert(tk.END, selected_turma[3])
                # matricula_entry.insert(tk.END, selected_turma[4])
                # curso_entry.insert(tk.END, selected_turma[5])
                # if selected_turma[6] == 1:
                #     radio_btn_aluno.select()
                # if selected_turma[6] == 2:
                #     radio_btn_admin.select()
                
            except IndexError:
                pass

        # Lista
        lista_turmas_label = ttk.Label(tab_turmas, text='ID / Turma / Periodo / Horario / Vagas Ocupadas / Total de Vagas / Local / Disciplina / Departamento / Professor').grid(row=linha, column=0, pady=10)
        linha += 1
        lista_turmas = tk.Listbox(tab_turmas, height=8, width=200, border=0)
        lista_turmas.grid(row=linha, column=0, columnspan=3, rowspan=2, padx=20)
        linha += 1
        # Create Scrollbar
        scrollbar_turmas = tk.Scrollbar(tab_turmas)
        scrollbar_turmas.grid(row=linha, column=3)
        linha += 1

        # Set scroll to listbox
        lista_turmas.configure(yscrollcommand=scrollbar_turmas.set)
        scrollbar_turmas.configure(command=lista_turmas.yview)

        # Bind select
        lista_turmas.bind('<<ListboxSelect>>', select_turma)

        def populate_lista_turmas():
            lista_turmas.delete(0, tk.END)
            for row in db.fetch_turma():
                lista_turmas.insert(tk.END, row)

        populate_lista_turmas()

        # Avaliação

        def select_aval(event):
            try:
                global selected_aval
                index = lista_aval.curselection()[0]
                selected_aval = lista_aval.get(index)

                clear_text()
                avaliacao_entry.insert(tk.END, selected_aval[5])
                nota_entry.insert(tk.END, selected_aval[6])
                # nome_entry.insert(tk.END, selected_turma[1])
                # email_entry.insert(tk.END, selected_turma[2])
                # senha_entry.insert(tk.END, selected_turma[3])
                # matricula_entry.insert(tk.END, selected_turma[4])
                # curso_entry.insert(tk.END, selected_turma[5])
                # if selected_turma[6] == 1:
                #     radio_btn_aluno.select()
                # if selected_turma[6] == 2:
                #     radio_btn_admin.select()
                populate_lista_denuncia(selected_aval[0])
                
            except IndexError:
                pass

        def add_avaliacao():
            if avaliacao_text.get() == '' or nota_text.get() == '':
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return
            db.insert_avaliacao(usuario_global, selected_turma[0], selected_turma[10], avaliacao_text.get(), nota_text.get())
            clear_text()
            populate_lista_aval(selected_turma[0])
            
        def remove_avaliacao():
            user = db.fetch_usuario_global(usuario_global)
            if user[0][6] == 1:
                messagebox.showerror("Erro", "Você precisa de permissões de administrador para remover avaliações!")
                return
            db.remove_avaliacao(selected_aval[0])
            clear_text()
            populate_lista_aval(selected_turma[0])
            populate_lista_denuncia(selected_aval[0])

        def update_avaliacao():
            if avaliacao_text.get() == '' or nota_text.get() == '':
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return
            db.update_avaliacao(selected_aval[0], avaliacao_text.get(), nota_text.get())
            populate_lista_aval(selected_turma[0])

        avaliacao_label = ttk.Label(tab_turmas, text='Avaliações', font=20).grid(row=linha, column=0, pady=10, sticky=tk.W)
        linha += 1

        # Lista de avaliações
        lista_avaliacoes_label = ttk.Label(tab_turmas, text='Aluno / Periodo / Professor / Disciplina / Avaliação / Nota').grid(row=linha, column=0, pady=10)
        linha += 1
        lista_aval = tk.Listbox(tab_turmas, height=8, width=200, border=0)
        lista_aval.grid(row=linha, column=0, columnspan=3, rowspan=2, padx=20)
        linha += 1
        # Create Scrollbar
        scrollbar_aval = tk.Scrollbar(tab_turmas)
        scrollbar_aval.grid(row=linha, column=3)
        linha += 1

        # Set scroll to listbox
        lista_aval.configure(yscrollcommand=scrollbar_aval.set)
        scrollbar_aval.configure(command=lista_aval.yview)

        # Bind select
        lista_aval.bind('<<ListboxSelect>>', select_aval)

        def populate_lista_aval(cod_turma):
            lista_aval.delete(0, tk.END)
            for row in db.fetch_avaliacao(cod_turma):
                lista_aval.insert(tk.END, row)

        linha += 1
        # avaliacao
        avaliacao_text = tk.StringVar()
        avaliacao_label = tk.Label(tab_turmas, text='Avaliação', font=('bold', 14))
        avaliacao_label.grid(row=linha, column=0, sticky=tk.W)
        avaliacao_entry = tk.Entry(tab_turmas, textvariable=avaliacao_text, width=50)
        avaliacao_entry.grid(row=linha, column=1, sticky=tk.W)
        linha += 1

        # nota
        nota_text = tk.StringVar()
        nota_label = tk.Label(tab_turmas, text='Nota (1-5)', font=('bold', 14))
        nota_label.grid(row=linha, column=0, sticky=tk.W)
        nota_entry = tk.Entry(tab_turmas, textvariable=nota_text)
        nota_entry.grid(row=linha, column=1, sticky=tk.W)
        linha += 1

        # Buttons
        add_avaliacao_btn = tk.Button(tab_turmas, text="Criar avaliacao", width=20, command=add_avaliacao)
        add_avaliacao_btn.grid(row=linha-2, column=2)

        remove_avaliacao_btn = tk.Button(tab_turmas, text='Remover avaliacao', width=20, command=remove_avaliacao)
        remove_avaliacao_btn.grid(row=linha-1, column=2)

        update_avaliacao_btn = tk.Button(tab_turmas, text='Atualizar avaliacao', width=20, command=update_avaliacao)
        update_avaliacao_btn.grid(row=linha, column=2)
        linha += 1

        clear_avaliacao_btn = tk.Button(tab_turmas, text='Limpar', width=20, command=clear_text)
        clear_avaliacao_btn.grid(row=linha, column=2)

        # Denuncias

        def select_denuncia(event):
            try:
                global selected_denuncia
                index = lista_denuncia.curselection()[0]
                selected_denuncia = lista_denuncia.get(index)

                clear_text()
                denuncia_entry.insert(tk.END, selected_denuncia[2])
                if selected_denuncia[3] != 'None':
                    denuncia_avaliacao_entry.insert(tk.END, selected_denuncia[3])
                # nome_entry.insert(tk.END, selected_turma[1])
                # email_entry.insert(tk.END, selected_turma[2])
                # senha_entry.insert(tk.END, selected_turma[3])
                # matricula_entry.insert(tk.END, selected_turma[4])
                # curso_entry.insert(tk.END, selected_turma[5])
                # if selected_turma[6] == 1:
                #     radio_btn_aluno.select()
                # if selected_turma[6] == 2:
                #     radio_btn_admin.select()
                
            except IndexError:
                pass

        def add_denuncia():
            user = db.fetch_usuario_global(usuario_global)
            if user[0][6] == 1 and denuncia_avaliacao_text.get() != '':
                messagebox.showerror("Erro", "Você precisa de permissões de administrador para avaliar denuncias!")
                return
            if denuncia_text.get() == '':
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return
            db.insert_denuncia(selected_aval[0], denuncia_text.get())
            clear_text()
            populate_lista_denuncia(selected_aval[0])
            
        def remove_denuncia():
            user = db.fetch_usuario_global(usuario_global)
            if user[0][6] == 1:
                messagebox.showerror("Erro", "Você precisa de permissões de administrador para remover denuncias!")
                return
            db.remove_denuncia(selected_denuncia[0])
            clear_text()
            populate_lista_denuncia(selected_aval[0])

        def update_denuncia():
            user = db.fetch_usuario_global(usuario_global)
            if user[0][6] == 1 and denuncia_avaliacao_text.get() != '':
                messagebox.showerror("Erro", "Você precisa de permissões de administrador para avaliar denuncias!")
                return
            if denuncia_text.get() == '':
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return
            db.update_denuncia(selected_denuncia[0], denuncia_text.get(), denuncia_avaliacao_text.get())
            populate_lista_denuncia(selected_aval[0])

        denuncia_label = ttk.Label(tab_turmas, text='Denuncias', font=20).grid(row=linha, column=0, pady=10, sticky=tk.W)
        linha += 1

        # Lista de denuncias
        lista_denuncias_label = ttk.Label(tab_turmas, text='ID / Denuncia / Avaliação').grid(row=linha, column=0, pady=10)
        linha += 1
        lista_denuncia = tk.Listbox(tab_turmas, height=8, width=200, border=0)
        lista_denuncia.grid(row=linha, column=0, columnspan=3, rowspan=2, padx=20)
        linha += 1
        # Create Scrollbar
        scrollbar_denuncia = tk.Scrollbar(tab_turmas)
        scrollbar_denuncia.grid(row=linha, column=3)
        linha += 1

        # Set scroll to listbox
        lista_denuncia.configure(yscrollcommand=scrollbar_denuncia.set)
        scrollbar_denuncia.configure(command=lista_denuncia.yview)

        # Bind select
        lista_denuncia.bind('<<ListboxSelect>>', select_denuncia)

        def populate_lista_denuncia(cod_aval):
            lista_denuncia.delete(0, tk.END)
            for row in db.fetch_denuncia(cod_aval):
                lista_denuncia.insert(tk.END, row)

        linha += 1
        # denuncia
        denuncia_text = tk.StringVar()
        denuncia_label = tk.Label(tab_turmas, text='Denuncia', font=('bold', 14))
        denuncia_label.grid(row=linha, column=0, sticky=tk.W)
        denuncia_entry = tk.Entry(tab_turmas, textvariable=denuncia_text, width=50)
        denuncia_entry.grid(row=linha, column=1, sticky=tk.W)
        linha += 1

        # Avaliacao
        denuncia_avaliacao_text = tk.StringVar()
        denuncia_avaliacao_label = tk.Label(tab_turmas, text='Avaliação da Denuncia', font=('bold', 14))
        denuncia_avaliacao_label.grid(row=linha, column=0, sticky=tk.W)
        denuncia_avaliacao_entry = tk.Entry(tab_turmas, textvariable=denuncia_avaliacao_text, width=50)
        denuncia_avaliacao_entry.grid(row=linha, column=1, sticky=tk.W)
        linha += 1

        # Buttons
        add_denuncia_btn = tk.Button(tab_turmas, text="Criar denuncia", width=20, command=add_denuncia)
        add_denuncia_btn.grid(row=linha-2, column=2)

        update_denuncia_btn = tk.Button(tab_turmas, text='Atualizar denuncia', width=20, command=update_denuncia)
        update_denuncia_btn.grid(row=linha-1, column=2)

        remove_denuncia_btn = tk.Button(tab_turmas, text='Ignorar denuncia', width=20, command=remove_denuncia)
        remove_denuncia_btn.grid(row=linha, column=2)
        linha += 1

        accept_denuncia_btn = tk.Button(tab_turmas, text='Remover Avaliação', width=20, command=remove_avaliacao)
        accept_denuncia_btn.grid(row=linha, column=2)
        linha += 1

        clear_denuncia_btn = tk.Button(tab_turmas, text='Limpar', width=20, command=clear_text)
        clear_denuncia_btn.grid(row=linha, column=2)
        











