/*adicionar novo admin*/
--INSERT INTO pessoas (nome, nif, n_tel, mail, pass) VALUES ('Goncalo', 123456789, 912837465, 'eusouadmin@gmail.com', crypt('pass123', gen_salt('bf')));
--INSERT INTO admins (pessoas_nif) VALUES (123456789);

/*eliminar admins*/
--DELETE FROM clientes WHERE pessoas_nif = 246813579;
--DELETE FROM PESSOAS WHERE NIF = 246813579;

/*pessoas e id's*/
/*
SELECT pessoas.nome, pessoas.nif, clientes.id_cliente, admins.id_admin, pessoas.mail, pessoas.pass
FROM pessoas 
LEFT JOIN admins ON pessoas.nif = admins.pessoas_nif 
LEFT JOIN clientes ON pessoas.nif = clientes.pessoas_nif */

/*adicionar id cliente*/
--INSERT INTO clientes (id_cliente, pessoas_nif) VALUES (3, 12938476)

/*print dos clientes*/
--SELECT pessoas.nome, pessoas.nif, clientes.id_cliente FROM pessoas,clientes WHERE pessoas.nif = clientes.pessoas_nif

/*ATRIBUIR GOLD*/
--UPDATE clientes SET gold = False WHERE pessoas_nif = 123456798

/*Alterar tabela inforota*/
--ALTER TABLE inforota DROP COLUMN duracao;
--ALTER TABLE inforota ADD COLUMN duracao TIME;
/*Remover id_rota pois nao e necessario visto que e FK*/
--ALTER TABLE viagens DROP COLUMN id_rota

/*ALterar a coluna id_mensagem para SERIAL id_msg*/
--ALTER TABLE mensagens DROP COLUMN id_mensagem CASCADE 
--ALTER TABLE mensagens ADD COLUMN id_msg SERIAL PRIMARY KEY

/*remove primary key from lida in leitura*/
--ALTER TABLE leitura DROP COLUMN lida CASCADE;
--ALTER TABLE leitura ADD COLUMN lida BOOLEAN;
--INSERT INTO leitura (clientes_pessoas_nif, mensagens_id_mensagem,lida) VALUES (123456798, 1, False);

/*printar mensagens - com destinatario e origem*/
--select m.id_mensagem, m.topico, m.conteudo, a.admins_pessoas_nif, c.clientes_pessoas_nif from mensagens as m, admins_mensagens as a, leitura as c;

/*printar viagens*/
/*SELECT *
FROM viagens 
FULL OUTER JOIN inforota ON viagens.inforota_id_rota = inforota.id_rota
WHERE viagens.inforota_id_rota = inforota.id_rota */

/*adicionar extensao para encpritar as passes*/
--CREATE EXTENSION IF NOT EXISTS pgcrypto;

/*adicionar a coluna lugares_disp a tabela viagens*/
--ALTER TABLE viagens ADD COLUMN lugares_disp INTEGER
/*BEGIN;
UPDATE viagens set lugares_disp = 50 WHERE id_viagem = 3;
COMMIT;*/

/*mostrar tudo sobre uma reserva*/
/*select * 
FROM reservas as r 
LEFT JOIN viagens ON  r.viagens_id_viagem = viagens.id_viagem
LEFT JOIN inforota ON viagens.inforota_id_rota = inforota.id_rota
*/
--para testar o delete de reservas e seus triggers
/*
Update reservas
set estado = 'em espera'
where clientes_pessoas_nif = 246897531*/

/*mensagens manuais*/
/*
select mensagens.id_mensagem,
		mensagens.topico,
		mensagens.conteudo,
		leitura.lida,
	    admins_mensagens.admins_pessoas_nif as De,
		leitura.clientes_pessoas_nif as Para
from mensagens
JOIN leitura ON mensagens.id_mensagem = leitura.mensagens_id_mensagem
JOIN admins_mensagens ON mensagens.id_mensagem = admins_mensagens.mensagens_id_mensagem
*/

/*mensagens automaticas*/
/*
select mensagens.id_mensagem,
		mensagens.topico,
		mensagens.conteudo,
		leitura.lida,
		leitura.clientes_pessoas_nif as Para
from mensagens
JOIN leitura ON mensagens.id_mensagem = leitura.mensagens_id_mensagem
*/

SELECT * FROM pessoas;
