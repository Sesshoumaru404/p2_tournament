-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- use in psql to \i tournament.sql of read file

SELECT pg_terminate_backend(procpid) FROM pg_stat_activity WHERE datname = 'p2_tournament';
DROP DATABASE p2_tournament;
CREATE DATABASE p2_tournament;

\c p2_tournament;

CREATE TABLE players (
    name text,
    id serial PRIMARY KEY
);

-- Setup table for all matches
-- id1, name1, id2, name2
CREATE TABLE matches (
    id1 integer REFERENCES players (id),
    id2 integer REFERENCES players (id),
    winner integer REFERENCES players (id),
    match_id serial PRIMARY KEY
		-- UNIQUE   (id1, id2)
);

CREATE VIEW standings AS (
  SELECT
    players.id,
    players.name,
    count(matches.winner) as wins,
    count(matches.match_id) as played
  FROM PLAYERS LEFT JOIN MATCHES
  ON players.id = matches.id1 OR players.id = matches.id2
  -- order by id desc
  GROUP BY players.id
  -- HAVING id = matches.winner
);
DROP TABLE players;
DROP TABLE matches;
-- DROP VIEW standings;
INSERT INTO players (name) VALUES ('test1');
INSERT INTO players VALUES ('test2');
INSERT INTO players VALUES ('test3');
INSERT INTO matches VALUES (1,3,1);
INSERT INTO matches VALUES (1,3,3);
INSERT INTO matches VALUES (1,3,3);

SELECT * from players;
SELECT * from MATCHES;
SELECT * from standings;
