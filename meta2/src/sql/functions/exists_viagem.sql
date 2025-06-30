CREATE OR REPLACE FUNCTION exists_viagem( 
	
	viagem_id INT 
	
) RETURNS BOOLEAN AS $$ 

DECLARE 
	v_count INT;

BEGIN 
	SELECT COUNT(*) INTO v_count FROM viagens 
	WHERE viagens.id_viagem = viagem_id;
	
	IF v_count > 0 THEN 
		RETURN TRUE; 
	ELSE 
		RETURN FALSE; 
	END IF; 
END; $$ LANGUAGE plpgsql; 