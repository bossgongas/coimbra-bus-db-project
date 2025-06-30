---Atualizar o ppreco de uma viagem 

CREATE OR REPLACE FUNCTION atualizar_preco(
	id_viagem_alt IN INT,
	p_novo IN REAL
)RETURNS BOOLEAN AS $$

DECLARE 
	preco_ant REAL;

BEGIN 
	---Guardar o preco antigo 
	SELECT preco INTO preco_ant FROM viagens WHERE viagens.id_viagem = id_viagem_alt; 
	---Atualizar o preco da viagem 
	UPDATE viagens SET preco=p_novo WHERE id_viagem = id_viagem_alt;
	---Registar o preco antigo no historico de alteraçoes 
	RETURN TRUE;

		
END; $$ LANGUAGE plpgsql 



	
		