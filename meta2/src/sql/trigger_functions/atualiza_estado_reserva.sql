CREATE OR REPLACE FUNCTION atualiza_estado_reserva()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM reservas
        WHERE viagens_id_viagem = OLD.viagens_id_viagem
        AND estado = 'espera'
        AND id_reserva != OLD.id_reserva
    ) THEN
		--atualiza o estado
        UPDATE reservas
        SET estado = 'OK' 
        WHERE viagens_id_viagem = OLD.viagens_id_viagem
        AND estado = 'espera';
		--ATUALIZA OS LUGARES
		UPDATE viagens
    	SET lugares_disp = lugares_disp - 1
    	WHERE id_viagem = OLD.viagens_id_viagem;
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_fila_espera
AFTER DELETE ON reservas
FOR EACH ROW
EXECUTE FUNCTION atualiza_estado_reserva();