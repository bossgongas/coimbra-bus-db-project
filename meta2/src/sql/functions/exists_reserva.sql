CREATE OR REPLACE FUNCTION exists_reserva( 
	
	reserva_id INT,
	nif_cliente INT
	
) RETURNS BOOLEAN AS $$ 

DECLARE 
	v_count INT;

BEGIN 
	SELECT COUNT(*) INTO v_count FROM reservas 
	WHERE reservas.clientes_pessoas_nif = nif_cliente AND reservas.viagens_id_viagem = reserva_id;
	
	IF v_count > 0 THEN 
		RETURN TRUE; 
	ELSE 
		RETURN FALSE; 
	END IF; 
END; $$ LANGUAGE plpgsql; 