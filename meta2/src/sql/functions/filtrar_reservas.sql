CREATE OR REPLACE FUNCTION filtrar_reservas( 
	nif_consultor clientes.pessoas_nif%TYPE,
	split_consulta VARCHAR(512),
	--consulta
	dist IN FLOAT(8),
    h_partida IN DATE,
    h_chegada IN DATE,
    d_origem IN VARCHAR,
    d_chegada IN VARCHAR,
	--ordenacao
    preco_ord IN VARCHAR,
	dist_ord IN VARCHAR,
	h_partida_ord IN VARCHAR,
	h_chegada_ord IN VARCHAR,
	d_origem_ord IN VARCHAR,
	d_chegada_ord IN VARCHAR

) RETURNS TABLE(
	id_r		 INTEGER,
	data_r		 TIMESTAMP,
	tipo_r		 VARCHAR(512),
	estado_r		 VARCHAR(512),
	dest_origem_r	 TEXT,
	dest_chegada_r TEXT,
	distancia_r	 FLOAT(8),
	hora_partida_r	 TIMESTAMP,
	hora_chegada_r	 TIMESTAMP,
	preco_r		 FLOAT(8)
) AS $$
BEGIN
	IF split_consulta = 'pas' then
        RETURN QUERY
        SELECT id_reserva, data_res, tipo, estado, dest_origem, dest_chegada,distancia, hora_partida, hora_chegada ,preco 
        FROM reservas as r 
        LEFT JOIN viagens ON  r.viagens_id_viagem = viagens.id_viagem
		LEFT JOIN inforota ON viagens.inforota_id_rota = inforota.id_rota
        --consulta
		WHERE (DATE(hora_partida) < CURRENT_DATE)
		  AND (h_partida IS NULL OR  DATE(hora_partida) = h_partida)
          AND (h_chegada IS NULL OR  DATE(hora_chegada) = h_chegada)
          AND (d_origem IS NULL OR dest_origem = d_origem)
          AND (d_chegada IS NULL OR dest_chegada = d_chegada)
		  AND (dist IS NULL OR dist = distancia)
		  AND r.clientes_pessoas_nif = nif_consultor
        --ordenacao
		ORDER BY 
          CASE  WHEN preco_ord='asc' THEN preco END ASC,
          CASE  WHEN preco_ord='desc' THEN preco END DESC,
		  CASE  WHEN dist_ord='asc' THEN distancia END ASC,
		  CASE  WHEN dist_ord='desc' THEN distancia END DESC,
		  CASE  WHEN h_partida_ord='asc' THEN hora_partida END ASC,
		  CASE  WHEN h_partida_ord='desc' THEN hora_partida END DESC,
		  CASE  WHEN h_chegada_ord='asc' THEN hora_chegada END ASC,
		  CASE  WHEN h_chegada_ord='desc' THEN hora_chegada END DESC,
		  CASE  WHEN d_origem_ord='asc' THEN dest_origem END ASC,
		  CASE  WHEN d_origem_ord='desc' THEN dest_origem END DESC,
		  CASE  WHEN d_chegada_ord='asc' THEN dest_chegada END ASC,
		  CASE  WHEN d_chegada_ord='desc' THEN dest_chegada END DESC,
          CASE  WHEN preco_ord is NULL 
		  		AND dist_ord is NULL
				AND h_partida_ord is NULL
				AND h_chegada_ord is NULL
				AND d_origem_ord is NULL
				AND d_chegada_ord is NULL
				THEN id_viagem END ASC;
	ELSIF split_consulta = 'fut' then
        RETURN QUERY
        SELECT id_reserva, data_res, tipo, estado, dest_origem, dest_chegada,distancia, hora_partida, hora_chegada ,preco 
        FROM reservas as r 
        LEFT JOIN viagens ON  r.viagens_id_viagem = viagens.id_viagem
		LEFT JOIN inforota ON viagens.inforota_id_rota = inforota.id_rota
        --consulta
		WHERE (DATE(hora_partida) >= CURRENT_DATE)
		  AND (h_partida IS NULL OR  DATE(hora_partida) = h_partida)
          AND (h_chegada IS NULL OR  DATE(hora_chegada) = h_chegada)
          AND (d_origem IS NULL OR dest_origem = d_origem)
          AND (d_chegada IS NULL OR dest_chegada = d_chegada)
		  AND (dist IS NULL OR dist = distancia)
		  AND r.clientes_pessoas_nif = nif_consultor
        --ordenacao
		ORDER BY 
          CASE  WHEN preco_ord='asc' THEN preco END ASC,
          CASE  WHEN preco_ord='desc' THEN preco END DESC,
		  CASE  WHEN dist_ord='asc' THEN distancia END ASC,
		  CASE  WHEN dist_ord='desc' THEN distancia END DESC,
		  CASE  WHEN h_partida_ord='asc' THEN hora_partida END ASC,
		  CASE  WHEN h_partida_ord='desc' THEN hora_partida END DESC,
		  CASE  WHEN h_chegada_ord='asc' THEN hora_chegada END ASC,
		  CASE  WHEN h_chegada_ord='desc' THEN hora_chegada END DESC,
		  CASE  WHEN d_origem_ord='asc' THEN dest_origem END ASC,
		  CASE  WHEN d_origem_ord='desc' THEN dest_origem END DESC,
		  CASE  WHEN d_chegada_ord='asc' THEN dest_chegada END ASC,
		  CASE  WHEN d_chegada_ord='desc' THEN dest_chegada END DESC,
          CASE  WHEN preco_ord is NULL 
		  		AND dist_ord is NULL
				AND h_partida_ord is NULL
				AND h_chegada_ord is NULL
				AND d_origem_ord is NULL
				AND d_chegada_ord is NULL
				THEN id_viagem END ASC;
	ELSIF split_consulta = 'all' then
        RETURN QUERY
        SELECT id_reserva, data_res, tipo, estado, dest_origem, dest_chegada,distancia, hora_partida, hora_chegada ,preco 
        FROM reservas as r 
        LEFT JOIN viagens ON  r.viagens_id_viagem = viagens.id_viagem
		LEFT JOIN inforota ON viagens.inforota_id_rota = inforota.id_rota
        --consulta
		WHERE (h_partida IS NULL OR  DATE(hora_partida) = h_partida)
          AND (h_chegada IS NULL OR  DATE(hora_chegada) = h_chegada)
          AND (d_origem IS NULL OR dest_origem = d_origem)
          AND (d_chegada IS NULL OR dest_chegada = d_chegada)
		  AND (dist IS NULL OR dist = distancia)
		  AND r.clientes_pessoas_nif = nif_consultor
        --ordenacao
		ORDER BY 
          CASE  WHEN preco_ord='asc' THEN preco END ASC,
          CASE  WHEN preco_ord='desc' THEN preco END DESC,
		  CASE  WHEN dist_ord='asc' THEN distancia END ASC,
		  CASE  WHEN dist_ord='desc' THEN distancia END DESC,
		  CASE  WHEN h_partida_ord='asc' THEN hora_partida END ASC,
		  CASE  WHEN h_partida_ord='desc' THEN hora_partida END DESC,
		  CASE  WHEN h_chegada_ord='asc' THEN hora_chegada END ASC,
		  CASE  WHEN h_chegada_ord='desc' THEN hora_chegada END DESC,
		  CASE  WHEN d_origem_ord='asc' THEN dest_origem END ASC,
		  CASE  WHEN d_origem_ord='desc' THEN dest_origem END DESC,
		  CASE  WHEN d_chegada_ord='asc' THEN dest_chegada END ASC,
		  CASE  WHEN d_chegada_ord='desc' THEN dest_chegada END DESC,
          CASE  WHEN preco_ord is NULL 
		  		AND dist_ord is NULL
				AND h_partida_ord is NULL
				AND h_chegada_ord is NULL
				AND d_origem_ord is NULL
				AND d_chegada_ord is NULL
				THEN id_viagem END ASC;
	END IF;
END;

$$ LANGUAGE plpgsql;