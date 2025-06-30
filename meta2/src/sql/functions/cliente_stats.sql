CREATE OR REPLACE FUNCTION stats_cliente(
	cliente INTEGER) 
RETURNS TABLE (total_viagens INTEGER, viagens_ida INTEGER, viagens_volta INTEGER, total_gasto FLOAT) AS $$
BEGIN

    SELECT COUNT(*) INTO total_viagens FROM reservas WHERE reservas.clientes_nif = cliente AND reservas.tipo='Reserva';
	
	SELECT SUM(preco) INTO total_gasto FROM viagens v
	INNER JOIN reservas r ON r.viagens_id_viagem=v.id_viagem
	WHERE r.clientes_nif = cliente;

    SELECT COUNT(*) INTO viagens_ida FROM reservas r 
    INNER JOIN viagens v ON r.viagens_id_viagem = v.id_viagem
	INNER JOIN inforota i ON i.id_rota = v.inforota_id_rota
    WHERE r.clientes_nif = cliente AND i.dest_origem = 'Coimbra';

    SELECT COUNT(*) INTO viagens_ida FROM reservas r 
    INNER JOIN viagens v ON r.viagens_id_viagem = v.id_viagem
	INNER JOIN inforota i ON i.id_rota = v.inforota_id_rota
    WHERE r.clientes_nif = cliente AND i.dest_chegada = 'Coimbra'; 

    RETURN QUERY SELECT total_viagens, viagens_ida, viagens_volta;
END;
$$ LANGUAGE plpgsql;