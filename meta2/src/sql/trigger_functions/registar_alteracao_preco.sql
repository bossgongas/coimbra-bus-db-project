CREATE OR REPLACE FUNCTION registar_alteracao_preco()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se houve alteração no preço
    IF NEW.preco <> OLD.preco THEN
        -- Inserir os dados na tabela hist_alteracoes
        INSERT INTO hist_alteracoes (dara_alteracao, preco_antigo, viagens_id_viagem)
        VALUES (CURRENT_DATE, OLD.preco, NEW.id_viagem);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Criar o trigger para executar a função após um update na tabela viagens
CREATE TRIGGER atualizar_preco_viagem
BEFORE UPDATE ON viagens
FOR EACH ROW
EXECUTE FUNCTION registar_alteracao_preco();