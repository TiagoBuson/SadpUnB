CREATE or REPLACE PROCEDURE procedure_insert_user(
    nome, email, senha, matricula, curso, isAdm)
AS $$
begin

    INSERT INTO usuario(nome, email, senha, matricula, curso, isAdm, img) VALUES (nome, email, senha, matricula, curso, isAdm, img);

END;
$$
LANGUAGE PLPGSQL;
