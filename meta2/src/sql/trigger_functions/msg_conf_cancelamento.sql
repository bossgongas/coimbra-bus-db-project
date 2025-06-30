CREATE OR REPLACE FUNCTION msg_conf_cancelamento() RETURNS TRIGGER AS $$
DECLARE
    mensagem TEXT;
	id_msg INTEGER;
	destinatario BIGINT;
BEGIN
    SELECT 'Cancelamento  ' || v.inforota_id_rota || 'Confirmado!' INTO mensagem

    FROM reservas r
    INNER JOIN viagens v ON r.viagens_id_viagem = v.id_viagem
    WHERE r.clientes_pessoas_nif = OLD.clientes_pessoas_nif;
	
	SELECT clientes_pessoas_nif INTO destinatario
	FROM reservas r
    INNER JOIN viagens v ON r.viagens_id_viagem = v.id_viagem
    WHERE r.clientes_pessoas_nif = OLD.clientes_pessoas_nif;
	
	INSERT INTO mensagens(topico,conteudo) 
	VALUES ('Cancelamento', mensagem);
	
	SELECT max(id_mensagem) FROM mensagens INTO id_msg;
	
	INSERT INTO leitura (clientes_pessoas_nif, mensagens_id_mensagem,lida) 
	VALUES (destinatario, id_msg, False);
	
	RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER enviar_confirmacao_cancelamento
AFTER DELETE ON reservas
FOR EACH ROW
execute FUNCTION msg_conf_cancelamento();