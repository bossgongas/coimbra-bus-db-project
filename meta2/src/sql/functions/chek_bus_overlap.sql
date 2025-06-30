---CHECK IF BUS IS OVERLAPPPING 
CREATE OR REPLACE FUNCTION check_bus_overlap(
	matricula TEXT,
	start_time TIMESTAMP,
    end_time TIMESTAMP
) RETURNS BOOLEAN AS $$

DECLARE 
	v_count INT;

BEGIN
    SELECT COUNT(*)
    INTO v_count
    FROM viagens
    WHERE autocarros_matricula = matricula
    AND OVERLAPS (viagens.hora_partida, viagens.hora_chegada, start_time, end_time);

    IF v_count > 0 THEN
        RETURN FALSE;
    ELSE
        RETURN TRUE;
    END IF;
	
END; $$  LANGUAGE plpgsql; 