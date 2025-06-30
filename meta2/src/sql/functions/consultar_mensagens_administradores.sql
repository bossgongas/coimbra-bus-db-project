CREATE OR REPLACE FUNCTION consultar_mensagens_administradores(cliente_nif IN clientes.pessoas_nif%TYPE)
RETURNS TABLE (
    id_msg INTEGER,
    topic TEXT,
    conteudo TEXT,
    remetente text,
	lda	BOOL
)
AS $$
BEGIN
	UPDATE leitura SET lida = true
    WHERE clientes_pessoas_nif = cliente_nif;

    RETURN QUERY
    SELECT m.id_mensagem, m.topico, m.conteudo, p.nome, l.lida
    FROM mensagens m
	JOIN admins_mensagens am ON m.id_mensagem = am.mensagens_id_mensagem
    JOIN admins a ON am.admins_pessoas_nif = a.pessoas_nif
	JOIN pessoas p ON p.nif = a.pessoas_nif
    JOIN leitura l ON m.id_mensagem = l.mensagens_id_mensagem
    WHERE l.clientes_pessoas_nif = cliente_nif;
END;
$$ LANGUAGE plpgsql;
