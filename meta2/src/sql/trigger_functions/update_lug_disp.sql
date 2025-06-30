CREATE OR REPLACE FUNCTION update_lug_disp() RETURNS TRIGGER AS $$
	DECLARE
		est_res VARCHAR(512);
	BEGIN
    	UPDATE viagens
    	SET lugares_disp = lugares_disp - 1
    	WHERE id_viagem = NEW.viagens_id_viagem;
		
		--excessao no caso de a reserva nao estar concluida
		SELECT estado INTO est_res
		FROM reservas
		WHERE viagens_id_viagem = NEW.viagens_id_viagem;
		
		IF NOT FOUND THEN
        	-- lançar exceção se nenhum registro encontrado
        	RAISE EXCEPTION 'Não foi encontrada uma reserva correspondente';
    	ELSIF est_res = 'espera' THEN
        -- lançar exceção
        	RAISE EXCEPTION 'A reserva esta em espera';
    	END IF;
		
		RETURN NEW;
	END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER atualizar_lugares_disp
AFTER INSERT ON reservas
FOR EACH ROW
execute FUNCTION update_lug_disp();