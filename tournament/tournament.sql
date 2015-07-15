-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- use in psql to \i tournament.sql of read file

CREATE DATABASE p2_tournament;

\c p2_tournament;

DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;

CREATE TABLE players (
    name text,
    tournament text DEFAULT 'no name',
    id serial PRIMARY KEY
);

-- Setup table for all matches
-- id1, name1, id2, name2
CREATE TABLE matches ( 
    id1 integer REFERENCES players (id) ON DELETE CASCADE,
    id2 integer REFERENCES players (id) ON DELETE CASCADE,
    winner integer REFERENCES players (id),
    match_id serial PRIMARY KEY
		-- UNIQUE   (id1, id2)
);

CREATE VIEW games AS (
  SELECT id,
    count(case when WINNER = id then 1 end) as wins,
    count(*) as played
  FROM (
    SELECT players.id,
      matches.winner as WINNER,
      matches.id1,
      matches.id2
    FROM PLAYERS LEFT JOIN MATCHES
    ON players.id = matches.id1 OR players.id = matches.id2
  ) s GROUP BY id
);


CREATE VIEW standings AS (
  SELECT
    players.id,
    players.name,
    games.wins,
    games.played,
    players.tournament
  FROM PLAYERS INNER JOIN GAMES USING (id)
  ORDER BY wins DESC
);
-- ALTER VIEW standings ADD COLUMN pionts integer;
-- DROP VIEW standings;
INSERT INTO players (name) VALUES ('Paul');
INSERT INTO players VALUES ('test2');
INSERT INTO players VALUES ('test3');

SELECT * from players;
SELECT * from MATCHES;
SELECT * from games;
SELECT * from standings;
