CREATE OR REPLACE FUNCTION update_lug_disp_after_cancel() RETURNS TRIGGER AS $$
	BEGIN
    	UPDATE viagens
    	SET lugares_disp = lugares_disp + 1
    	WHERE id_viagem = NEW.viagens_id_viagem;
		
		RETURN NEW;
	END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER update_lug_disp_after_cancel
AFTER DELETE ON reservas
FOR EACH ROW
execute FUNCTION update_lug_disp_after_cancel();