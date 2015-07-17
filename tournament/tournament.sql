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
    contestant integer REFERENCES players (id) ON DELETE CASCADE,
    opponent integer REFERENCES players (id) ON DELETE CASCADE,
    result text,
    points integer,
    match_id serial PRIMARY KEY
		-- UNIQUE   (id1, id2)
);

CREATE VIEW games AS (
  SELECT id,
    count(case when results = 'w' then 1 end) as wins,
    count(case when results = 't' then 1 end) as ties,
    count(case when results = 'l' then 1 end) as loses,
    sum(pionts) as points,
    count(*) as played
  FROM (
    SELECT players.id,
      matches.result as results,
      matches.contestant,
      matches.points as pionts
    FROM PLAYERS LEFT JOIN MATCHES
    ON players.id = matches.contestant
  ) s GROUP BY id
);

CREATE VIEW standings AS (
  SELECT
    players.id,
    players.name,
    games.wins,
    games.ties,
    games.loses,
    games.played,
    games.points,
    players.tournament
  FROM PLAYERS
    INNER JOIN GAMES USING (id)
  ORDER BY points DESC
);


CREATE VIEW omw AS (
  SELECT id,
  sum(win) as omw
  FROM (
    SELECT matches.contestant as id ,
    matches.opponent,
    standings.wins as win
    FROM matches LEFT JOIN standings
    ON matches.opponent = standings.id
  ) s GROUP by  id
);
-- ALTER VIEW standings ADD COLUMN pionts integer;
-- DROP VIEW standings;
-- INSERT INTO players (name) VALUES ('Paul');
-- INSERT INTO players VALUES ('test2');
-- INSERT INTO players VALUES ('test3');

SELECT * from players;
SELECT * from MATCHES;
SELECT * from games;
SELECT * from standings;

select *
  from (
    SELECT contestant, count(case when result = 'w' then 1 end) as wins
    FROM matches
    group by contestant;
  ) as test
