from tkinter import *
import psycopg2

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(database="faculdade", user="postgres", password="postgres", host="localhost")
            print("Conectado!")
        except:
            print("Não foi possivel conectar com o servidor!")


        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS usuario (id serial PRIMARY KEY, nome VARCHAR(50), email VARCHAR(50), senha VARCHAR(50), matricula VARCHAR(50), curso VARCHAR(50), isAdm INT, img BYTEA);")
        self.cur.execute("CREATE TABLE IF NOT EXISTS professor (id serial PRIMARY KEY, cod_professor VARCHAR(50), nome VARCHAR(75));")
        self.cur.execute("CREATE TABLE IF NOT EXISTS disciplina (id serial PRIMARY KEY, cod VARCHAR(25), nome VARCHAR(150), cod_depto VARCHAR(50));")
        self.cur.execute("CREATE TABLE IF NOT EXISTS turma (id serial PRIMARY KEY, turma INT, periodo VARCHAR(50), horario VARCHAR(300), vagas_ocupadas INT,total_vagas INT,local VARCHAR(70),cod_disciplina VARCHAR(50),cod_depto VARCHAR(50), cod_professor VARCHAR(50));")
        self.cur.execute("CREATE TABLE IF NOT EXISTS departamento (id serial PRIMARY KEY, cod VARCHAR(50), nome VARCHAR(150));")
        self.cur.execute("CREATE TABLE IF NOT EXISTS avaliacao (id serial PRIMARY KEY, cod_usuario VARCHAR(50), cod_turma INT, cod_professor VARCHAR(50), texto VARCHAR(100), nota INT);")
        self.cur.execute("CREATE TABLE IF NOT EXISTS denuncia (id serial PRIMARY KEY, cod_avaliacao INT, denuncia VARCHAR(150), avaliacao VARCHAR(150))")

        # VIEWs

        self.cur.execute('CREATE or REPLACE VIEW view_turmas as select turma.id, turma.turma, turma.periodo, horario, vagas_ocupadas, total_vagas, local, disciplina.nome as "disciplina", departamento.nome as "departamento", professor.nome as "professor", professor.cod_professor from turma inner join professor using (cod_professor) inner join disciplina on disciplina.cod = turma.cod_disciplina inner join departamento on departamento.cod = turma.cod_depto;')
        self.conn.commit()
    # FETCHS
    def fetch_usuario(self):
        self.cur.execute("Select * from usuario")
        rows = self.cur.fetchall()
        return rows
    
    def fetch_usuario_global(self, matricula):
        self.cur.execute("Select * from usuario where matricula = %s", (matricula,))
        user = self.cur.fetchall()
        return user
    
    def fetch_professor(self):
        self.cur.execute("Select * from professor")
        rows = self.cur.fetchall()
        return rows
    
    def fetch_disciplina(self):
        self.cur.execute("Select * from disciplina")
        rows = self.cur.fetchall()
        return rows
    
    def fetch_turma(self):
        self.cur.execute('Select * from view_turmas;')
        rows = self.cur.fetchall()
        return rows
    
    def fetch_departamento(self):
        self.cur.execute("Select * from departamento")
        rows = self.cur.fetchall()
        return rows
    
    def fetch_avaliacao(self, cod_turma):
        self.cur.execute("Select * from avaliacao where cod_turma=%s", (cod_turma,))
        rows = self.cur.fetchall()
        return rows
    
    def fetch_avaliacao(self, cod_turma):
        self.cur.execute("select avaliacao.id, usuario.nome, turma.periodo, professor.nome as professor, disciplina.nome as disciplina, texto, nota from avaliacao inner join usuario on usuario.matricula = avaliacao.cod_usuario inner join professor using (cod_professor) inner join turma on turma.id = avaliacao.cod_turma inner join disciplina on disciplina.cod = turma.cod_disciplina where cod_turma=%s", (cod_turma,))
        rows = self.cur.fetchall()
        return rows
    
    def fetch_denuncia(self, cod_avaliacao):
        self.cur.execute("Select * from denuncia where cod_avaliacao=%s", (cod_avaliacao,))
        rows = self.cur.fetchall()
        return rows
    
    # INSERTS
    def insert_usuario(self, nome, email, senha, matricula, curso, isAdm, filename):
        self.cur.execute('CALL procedure_insert_user(%s, %s, %s, %s, %s, %s, %s)', (nome, email, senha, matricula, curso, isAdm, filename))
        self.conn.commit()

    def insert_avaliacao(self, cod_usuario, cod_turma, cod_professor, texto, nota):
        self.cur.execute("INSERT INTO avaliacao (cod_usuario, cod_turma, cod_professor, texto, nota) VALUES (%s, %s, %s, %s, %s)", (cod_usuario, cod_turma, cod_professor, texto, nota))
        self.conn.commit()

    def insert_denuncia(self, cod_avaliacao, denuncia):
        self.cur.execute("INSERT INTO denuncia (cod_avaliacao, denuncia) VALUES (%s, %s)", (cod_avaliacao, denuncia))
        self.conn.commit()


    # REMOVEs
    def remove_usuario(self, id):
        self.cur.execute("DELETE FROM usuario WHERE id=%s", (id,))
        self.conn.commit()

    def remove_avaliacao(self, id):
        self.cur.execute("DELETE FROM avaliacao WHERE id=%s", (id,))
        self.conn.commit()

    def remove_denuncia(self, id):
        self.cur.execute("DELETE FROM denuncia WHERE id=%s", (id,))
        self.conn.commit()


    # UPDATEs
    def update_usuario(self, id, nome, email, senha, matricula, curso, isAdm):
        self.cur.execute("UPDATE usuario SET nome = %s, email = %s, senha = %s, matricula = %s, curso = %s, isAdm = %s WHERE id = %s", (nome, email, senha, matricula, curso, isAdm, id))
        # self.cur.execute('call procedure_update_user(nome, email, senha, matricula, curso, isAdm, id)')
        self.conn.commit()

    def update_avaliacao(self, id, texto, nota):
        self.cur.execute("UPDATE avaliacao SET texto = %s, nota = %s WHERE id = %s", (texto, nota, id))
        self.conn.commit()

    def update_denuncia(self, id, denuncia, avaliacao):
        self.cur.execute("UPDATE denuncia SET denuncia = %s, avaliacao = %s WHERE id = %s", (denuncia, avaliacao, id))
        self.conn.commit()

    
    def __del__(self):
        self.conn.close()