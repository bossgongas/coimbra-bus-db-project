CREATE OR REPLACE FUNCTION filtrar_viagens( 
    h_partida IN DATE,
    h_chegada IN DATE,
    d_origem IN VARCHAR,
    d_chegada IN VARCHAR,
    preco_ord IN VARCHAR

    ) RETURNS REFCURSOR AS $$

DECLARE 
    ref1 REFCURSOR := 'mycursor'; 

BEGIN
        OPEN ref1 FOR
        SELECT id_viagem, hora_partida, hora_chegada, preco, dest_origem, dest_chegada, duracao, distancia  
        FROM viagens as v 
        LEFT JOIN inforota ON  v.inforota_id_rota = inforota.id_rota
        WHERE (h_partida IS NULL OR  DATE(hora_partida) = h_partida)
          AND (h_chegada IS NULL OR  DATE(hora_chegada) = h_chegada)
          AND (d_origem IS NULL OR dest_origem = d_origem)
          AND (d_chegada IS NULL OR dest_chegada = d_chegada)
          ORDER BY 
              CASE  WHEN preco_ord='asc' THEN preco END ASC,
            CASE  WHEN preco_ord='desc' THEN preco END DESC,
            CASE  WHEN preco_ord is NULL THEN id_viagem END ASC;
    RETURN ref1;
END;

$$ LANGUAGE plpgsql;