CREATE OR REPLACE FUNCTION adicionar_reserva (
    cliente IN clientes.pessoas_nif%TYPE,
    viagem IN viagens.id_viagem%TYPE
)RETURNS BOOLEAN AS $$

DECLARE
    v_assento viagens.lugares_disp%TYPE;
BEGIN
    SELECT lugares_disp INTO v_assento
    FROM viagens
    WHERE id_viagem = viagem;

    IF v_assento > 0 THEN
        INSERT INTO reservas (data_res, tipo, estado, clientes_pessoas_nif, viagens_id_viagem)
        VALUES (CURRENT_DATE, 'Reserva','OK', cliente, viagem);
		RETURN TRUE;
    ELSE
        INSERT INTO reservas (data_res, tipo, estado, clientes_pessoas_nif, viagens_id_viagem)
        VALUES (CURRENT_DATE, 'Reserva','espera', cliente, viagem);
		RETURN TRUE;
    END IF;
END;
$$ LANGUAGE plpgsql;