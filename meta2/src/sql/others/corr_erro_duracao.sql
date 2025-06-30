BEGIN;

UPDATE inforota
SET duracao = '01:20:00'
WHERE id_rota = 1;

UPDATE inforota
SET duracao = '02:10:00'
WHERE id_rota = 2;

UPDATE inforota
SET duracao = '01:20:00'
WHERE id_rota = 3;

COMMIT;