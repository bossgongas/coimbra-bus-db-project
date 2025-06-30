CREATE OR REPLACE FUNCTION open_messages(topic VARCHAR(255), nif BIGINT)
RETURNS TABLE (id_msg INTEGER, cont TEXT, lid BOOLEAN)
AS $$
BEGIN
    UPDATE leitura SET lida = true
    WHERE clientes_pessoas_nif = nif AND mensagens_id_mensagem IN (
        SELECT id_mensagem FROM mensagens WHERE topico = topic
    );

    RETURN QUERY SELECT m.id_mensagem, m.conteudo, l.lida
    FROM mensagens m
    JOIN leitura l ON m.id_mensagem = l.mensagens_id_mensagem
    WHERE m.topico = topic AND l.clientes_pessoas_nif = nif;
END;
$$ LANGUAGE plpgsql;
