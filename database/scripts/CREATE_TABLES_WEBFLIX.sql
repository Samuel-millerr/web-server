CREATE TABLE nacionalidade(
	id_nacionalidade INTEGER AUTO_INCREMENT UNIQUE,
    nacionalidade VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE diretor(
	id_diretor INTEGER AUTO_INCREMENT UNIQUE,
    nome VARCHAR(100) NOT NULL,
    sobrenome VARCHAR(100) NOT NULL,
    genero ENUM('Masculino', 'Feminino', 'Não Binario') NOT NULL,
	id_nacionalidade INTEGER NOT NULL,
    FOREIGN KEY (id_nacionalidade) REFERENCES nacionalidade(id_nacionalidade)
);

CREATE TABLE ator(
	id_ator INTEGER AUTO_INCREMENT UNIQUE,
    nome VARCHAR(100) NOT NULL,
    sobrenome VARCHAR(100) NOT NULL,
    genero ENUM('Masculino', 'Feminino', 'Não Binario') NOT NULL,
	id_nacionalidade INTEGER NOT NULL,
    FOREIGN KEY (id_nacionalidade) REFERENCES nacionalidade(id_nacionalidade)
);

CREATE TABLE linguagem(
	id_linguagem INTEGER AUTO_INCREMENT UNIQUE,
    linguagem VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE genero(
	id_genero INTEGER AUTO_INCREMENT UNIQUE, 
    genero VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE pais(
	id_pais INTEGER AUTO_INCREMENT UNIQUE,
    pais VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE produtora(
	id_produtora INTEGER AUTO_INCREMENT UNIQUE,
    nome VARCHAR(100) NOT NULL UNIQUE,
    id_pais INTEGER NOT NULL,
    FOREIGN KEY (id_pais) REFERENCES pais(id_pais)
);

CREATE TABLE filme(
	id_filme INTEGER AUTO_INCREMENT UNIQUE,
    titulo VARCHAR(100) NOT NULL UNIQUE, 
    orcamento INTEGER, 
    tempo_duracao TIME NOT NULL,
    ano_publicacao YEAR NOT NULL,
    poster VARCHAR(255) UNIQUE
);

CREATE TABLE filme_diretor(
	id_filme_diretor INTEGER AUTO_INCREMENT UNIQUE,
    id_filme INTEGER NOT NULL,
    id_diretor INTEGER NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
    FOREIGN KEY (id_diretor) REFERENCES diretor(id_diretor)
);

CREATE TABLE filme_ator(
	id_filme_ator INTEGER AUTO_INCREMENT UNIQUE,
    id_filme INTEGER NOT NULL,
    id_ator INTEGER NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
    FOREIGN KEY (id_ator) REFERENCES ator(id_ator)
);

CREATE TABLE filme_linguagem(
	id_filme_linguagem INTEGER AUTO_INCREMENT UNIQUE,
    id_filme INTEGER NOT NULL,
    id_linguagem INTEGER NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
    FOREIGN KEY (id_linguagem) REFERENCES linguagem(id_linguagem)
);

CREATE TABLE filme_genero(
	id_filme_genero INTEGER AUTO_INCREMENT UNIQUE,
    id_filme INTEGER NOT NULL, 
    id_genero INTEGER NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
    FOREIGN KEY (id_genero) REFERENCES genero(id_genero)
);

CREATE TABLE filme_pais(
	id_filme_pais INTEGER AUTO_INCREMENT UNIQUE, 
    id_filme INTEGER NOT NULL,
    id_pais INTEGER NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
    FOREIGN KEY (id_pais) REFERENCES pais(id_pais)
);

CREATE TABLE filme_produtora(
	id_filme_produto INTEGER AUTO_INCREMENT UNIQUE,
    id_filme INTEGER NOT NULL,
    id_produtora INTEGER  NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES filme(id_filme),
    FOREIGN KEY (id_produtora) REFERENCES produtora(id_produtora)
);