CREATE OR REPLACE FUNCTION viagens_stats(
    inicio DATE, 
    fim DATE
) RETURNS stats_tipo AS $$
DECLARE 
    stats stats_tipo;
BEGIN 
    SELECT COUNT(*) INTO stats.n_viagens FROM viagens WHERE DATE(viagens.hora_partida) BETWEEN inicio AND fim; 
    
    SELECT SUM(id_reserva) INTO stats.n_lugares_vendidos FROM reservas WHERE DATE(reservas.data_res) BETWEEN inicio AND fim AND tipo='Reserva';
    
    SELECT SUM(preco) INTO stats.receita FROM viagens AS v INNER JOIN reservas as r ON v.id_viagem = r.viagens_id_viagem
    WHERE DATE(v.hora_partida) BETWEEN inicio AND fim;
    
    SELECT COUNT(*) INTO stats.n_lugares_vendidos FROM viagens AS v INNER JOIN reservas as r ON v.id_viagem = r.viagens_id_viagem
    WHERE DATE(v.hora_partida) BETWEEN inicio AND fim;
    
    SELECT COUNT(DISTINCT DATE_TRUNC('day', hora_partida)) INTO stats.num_dias
        FROM viagens
        WHERE hora_partida BETWEEN inicio AND fim;
    
    SELECT COUNT(dest_origem) INTO stats.melhor_partida
        FROM inforota as i INNER JOIN viagens as v 
        ON i.id_rota = v.inforota_id_rota
        WHERE v.hora_partida BETWEEN inicio AND fim
        GROUP BY dest_origem
        ORDER BY COUNT(*) DESC
        LIMIT 1;
    
    SELECT COUNT(dest_chegada) INTO stats.melhor_destino
        FROM inforota as i INNER JOIN viagens as v 
        ON i.id_rota = v.inforota_id_rota
        WHERE v.hora_partida BETWEEN inicio AND fim
        GROUP BY dest_chegada
        ORDER BY COUNT(*) DESC
        LIMIT 1;
    
    stats.preco_medio := stats.receita / stats.n_viagens; 
    stats.receita_media_dia := stats.receita / stats.num_dias; 
    stats.n_lugares_dia := stats.n_lugares_vendidos / stats.num_dias; 
    
    RETURN stats; 
END; 
$$ LANGUAGE plpgsql;