CREATE TABLE pessoas (
	nome	 TEXT,
	nif	 BIGINT,
	n_tel INTEGER,
	mail	 TEXT,
	pass	 TEXT,
	PRIMARY KEY(nif)
);

CREATE TABLE admins (
	id_admin	 SERIAL NOT NULL,
	pessoas_nif BIGINT,
	PRIMARY KEY(pessoas_nif)
);

CREATE TABLE clientes (
	id_cliente	 SERIAL NOT NULL,
	gold	 BOOL,
	pessoas_nif BIGINT,
	PRIMARY KEY(pessoas_nif)
);

CREATE TABLE viagens (
	id_viagem		 SERIAL,
	hora_partida	 TIMESTAMP,
	hora_chegada	 TIMESTAMP,
	preco		 FLOAT(8),
	inforota_id_rota	 INTEGER NOT NULL,
	autocarros_matricula TEXT NOT NULL,
	PRIMARY KEY(id_viagem)
);

CREATE TABLE autocarros (
	matricula TEXT,
	lotacao	 INTEGER,
	PRIMARY KEY(matricula)
);

CREATE TABLE inforota (
	id_rota	 SERIAL,
	dest_origem	 TEXT,
	dest_chegada TEXT,
	duracao	 TIME,
	distancia	 FLOAT(8),
	PRIMARY KEY(id_rota)
);

CREATE TABLE reservas (
	id_reserva		 SERIAL,
	data_res		 TIMESTAMP,
	tipo		 VARCHAR(512),
	estado		 VARCHAR(512),
	clientes_pessoas_nif BIGINT NOT NULL,
	viagens_id_viagem	 INTEGER NOT NULL,
	PRIMARY KEY(id_reserva)
);

CREATE TABLE mensagens (
	id_mensagem SERIAL,
	topico	 TEXT,
	conteudo	 TEXT,
	PRIMARY KEY(id_mensagem)
);

CREATE TABLE leitura (
	lida			 BOOL,
	clientes_pessoas_nif	 BIGINT NOT NULL,
	mensagens_id_mensagem BIGINT NOT NULL
);

CREATE TABLE hist_alteracoes (
	id_alteracao	 SERIAL,
	dara_alteracao	 DATE,
	preco_antigo	 DOUBLE PRECISION,
	viagens_id_viagem INTEGER NOT NULL,
	PRIMARY KEY(id_alteracao)
);

CREATE TABLE admins_autocarros (
	admins_pessoas_nif	 BIGINT,
	autocarros_matricula TEXT,
	PRIMARY KEY(admins_pessoas_nif,autocarros_matricula)
);

CREATE TABLE admins_mensagens (
	admins_pessoas_nif	 BIGINT,
	mensagens_id_mensagem BIGINT,
	PRIMARY KEY(admins_pessoas_nif,mensagens_id_mensagem)
);

CREATE TABLE clientes_viagens (
	clientes_pessoas_nif BIGINT,
	viagens_id_viagem	 INTEGER,
	PRIMARY KEY(clientes_pessoas_nif,viagens_id_viagem)
);

CREATE TABLE admins_viagens (
	admins_pessoas_nif BIGINT,
	viagens_id_viagem	 INTEGER,
	PRIMARY KEY(admins_pessoas_nif,viagens_id_viagem)
);

ALTER TABLE admins ADD CONSTRAINT admins_fk1 FOREIGN KEY (pessoas_nif) REFERENCES pessoas(nif);
ALTER TABLE clientes ADD CONSTRAINT clientes_fk1 FOREIGN KEY (pessoas_nif) REFERENCES pessoas(nif);
ALTER TABLE viagens ADD CONSTRAINT viagens_fk1 FOREIGN KEY (inforota_id_rota) REFERENCES inforota(id_rota);
ALTER TABLE viagens ADD CONSTRAINT viagens_fk2 FOREIGN KEY (autocarros_matricula) REFERENCES autocarros(matricula);
ALTER TABLE reservas ADD CONSTRAINT reservas_fk1 FOREIGN KEY (clientes_pessoas_nif) REFERENCES clientes(pessoas_nif);
ALTER TABLE reservas ADD CONSTRAINT reservas_fk2 FOREIGN KEY (viagens_id_viagem) REFERENCES viagens(id_viagem);
ALTER TABLE leitura ADD CONSTRAINT leitura_fk1 FOREIGN KEY (clientes_pessoas_nif) REFERENCES clientes(pessoas_nif);
ALTER TABLE leitura ADD CONSTRAINT leitura_fk2 FOREIGN KEY (mensagens_id_mensagem) REFERENCES mensagens(id_mensagem);
ALTER TABLE hist_alteracoes ADD CONSTRAINT hist_alteracoes_fk1 FOREIGN KEY (viagens_id_viagem) REFERENCES viagens(id_viagem);
ALTER TABLE admins_autocarros ADD CONSTRAINT admins_autocarros_fk1 FOREIGN KEY (admins_pessoas_nif) REFERENCES admins(pessoas_nif);
ALTER TABLE admins_autocarros ADD CONSTRAINT admins_autocarros_fk2 FOREIGN KEY (autocarros_matricula) REFERENCES autocarros(matricula);
ALTER TABLE admins_mensagens ADD CONSTRAINT admins_mensagens_fk1 FOREIGN KEY (admins_pessoas_nif) REFERENCES admins(pessoas_nif);
ALTER TABLE admins_mensagens ADD CONSTRAINT admins_mensagens_fk2 FOREIGN KEY (mensagens_id_mensagem) REFERENCES mensagens(id_mensagem);
ALTER TABLE clientes_viagens ADD CONSTRAINT clientes_viagens_fk1 FOREIGN KEY (clientes_pessoas_nif) REFERENCES clientes(pessoas_nif);
ALTER TABLE clientes_viagens ADD CONSTRAINT clientes_viagens_fk2 FOREIGN KEY (viagens_id_viagem) REFERENCES viagens(id_viagem);
ALTER TABLE admins_viagens ADD CONSTRAINT admins_viagens_fk1 FOREIGN KEY (admins_pessoas_nif) REFERENCES admins(pessoas_nif);
ALTER TABLE admins_viagens ADD CONSTRAINT admins_viagens_fk2 FOREIGN KEY (viagens_id_viagem) REFERENCES viagens(id_viagem);