-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- use in psql to \i tournament.sql of read file

-- SELECT pg_terminate_backend(procpid) FROM pg_stat_activity WHERE datname = 'p2_tournament';
-- DROP DATABASE p2_tournament;
CREATE DATABASE p2_tournament;

\c p2_tournament;

DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;

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

CREATE VIEW win_lose AS (
  SELECT
    players.id,
    count(matches.winner) as wins
  FROM PLAYERS LEFT JOIN MATCHES
  ON players.id = matches.winner
  -- order by id desc
  GROUP BY players.id
  -- HAVING id = matches.winner
);

CREATE VIEW games AS (
  SELECT
    players.id,
    count(matches.match_id) as played
  FROM PLAYERS LEFT JOIN MATCHES
  ON players.id = matches.id1 OR players.id = matches.id2
  -- order by id desc
  GROUP BY players.id
  -- HAVING id = matches.winner
);


CREATE VIEW standings AS (
  SELECT
    players.id,
    players.name,
    win_lose.wins,
    games.played
  FROM PLAYERS INNER JOIN GAMES USING (id)
  INNER JOIN WIN_LOSE USING (id)
  ORDER BY wins DESC
);
-- DROP VIEW standings;
INSERT INTO players (name) VALUES ('Paul');
INSERT INTO players VALUES ('test2');
INSERT INTO players VALUES ('test3');
-- INSERT INTO matches VALUES (1,3,1);
-- INSERT INTO matches VALUES (3,1,3);
-- INSERT INTO matches VALUES (1,3,1);
-- INSERT INTO matches VALUES (1,2,1);
-- INSERT INTO matches VALUES (2,3,3);

SELECT * from players;
SELECT * from MATCHES;
SELECT * from win_lose;
SELECT * from games;
SELECT * from standings;
