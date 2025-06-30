BEGIN;
-- Inserir dados na tabela inforota
INSERT INTO inforota (dest_origem, dest_chegada, distancia, duracao)
VALUES
    ('Coimbra', 'Porto', 122.00, '01:20:00'),
    ('Coimbra', 'Lisboa', 202.00, '02:10:00'),
    ('Porto', 'Coimbra', 122.00, '01:20:00');
	
-- Inserir dados na tabela autocarros
INSERT INTO autocarros (matricula, lotacao)
VALUES
    ('11-AA-22', 50),
    ('22-BB-33', 40),
    ('33-CC-44', 30);
	
-- Inserir dados na tabela viagens
INSERT INTO viagens (hora_partida, hora_chegada, preco, inforota_id_rota, autocarros_matricula, lugares_disp)
VALUES
    ('2023-05-15 10:00:00', '2023-05-15 12:00:00', 50.00, 1, '11-AA-22', 50),
    ('2023-05-16 14:00:00', '2023-05-16 16:00:00', 70.00, 2, '22-BB-33', 40),
    ('2023-05-17 18:00:00', '2023-05-17 20:00:00', 60.00, 3, '33-CC-44', 30);
	
-- Inserir dados na tabela pessoas
INSERT INTO pessoas (nome, nif, n_tel, mail, pass)
VALUES
    ('Gonçalo Bastos', 123456789, 123456789, 'eusouadmin@example.com', crypt('senha123', gen_salt('bf')) ),
    ('Leo Cordeiro', 987654321, 987654321, 'eusoucliente@example.com', crypt('senha456',gen_salt('bf')) ),
    ('Pedro Almeida', 555555555, 555555555, 'pedro.almeida@example.com', crypt('senha789',gen_salt('bf')) );

-- Inserir dados na tabela admins
INSERT INTO admins (pessoas_nif)
VALUES
    (123456789);

-- Inserir dados na tabela clientes
INSERT INTO clientes (gold, pessoas_nif)
VALUES
    (FALSE, 987654321),
    (TRUE, 555555555);

COMMIT;