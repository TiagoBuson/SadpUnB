INSERT INTO usuario (nome, email, senha, matricula, curso, isAdm, img) values ('Nome1', 'Email1', 'Senha1', 'Matricula1', 'Curso1', '2', '')
INSERT INTO usuario (nome, email, senha, matricula, curso, isAdm, img) values ('Nome2', 'Email2', 'Senha2', 'Matricula2', 'Curso2', '2', '')
INSERT INTO usuario (nome, email, senha, matricula, curso, isAdm, img) values ('Nome3', 'Email3', 'Senha3', 'Matricula3', 'Curso3', '2', '')

INSERT INTO avaliacao (cod_usuario, cod_turma, cod_professor, texto, nota) VALUES ('1', '1', '1', 'Avaliacao1', 5)
INSERT INTO avaliacao (cod_usuario, cod_turma, cod_professor, texto, nota) VALUES ('1', '1', '1', 'Avaliacao2', 5)
INSERT INTO avaliacao (cod_usuario, cod_turma, cod_professor, texto, nota) VALUES ('1', '1', '1', 'Avaliacao3', 5)

INSERT INTO denuncia (cod_avaliacao, denuncia) VALUES ('1', 'Denuncia1')
INSERT INTO denuncia (cod_avaliacao, denuncia) VALUES ('1', 'Denuncia2')
INSERT INTO denuncia (cod_avaliacao, denuncia) VALUES ('1', 'Denuncia3')