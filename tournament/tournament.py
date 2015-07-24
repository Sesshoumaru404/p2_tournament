#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=p2_tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches;")
    conn.commit()
    conn.close()


def deletePlayers(tournament=None):
    """
    Remove all the player records from the database.
    And if statement to pass all project tests.
    """
    if tournament is None:
        erase = "DELETE FROM players;"
    else:
        erase = "DELETE FROM players WHERE tournament = %s;", (tournament,)
    conn = connect()
    c = conn.cursor()
    c.execute(erase)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM players;")
    posts = c.rowcount
    conn.close()
    return posts


def registerPlayer(name, tournament=None):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name, tournament) VALUES (%s, %s)",
              (name, tournament,))
    conn.commit()
    conn.close()


def playerStandings(tournament=None):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    conn = connect()
    c = conn.cursor()
    if tournament is None:
        loadTable = "SELECT id, name, wins, played FROM standings;"
    else:
        x = "CREATE VIEW %s AS SELECT * FROM standings WHERE tournament = '%s';"
        tableCreate = x % (tournament, tournament,)
        loadTable = "SELECT * FROM %s;" % tournament
        c.execute(tableCreate)
    c.execute(loadTable)
    table = c.fetchall()
    conn.commit()
    conn.close()
    return table


def findtournament(tournament):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM %s;"  % tournament)
    currentTournament = c.fetchall()
    conn.close()
    return currentTournament


def checkrematch(id1, id2):
    """
    Use to check if players have already played if other
    """
    if id2 == None:
        findMatch = "SELECT * FROM matches where contestant = %s " \
            " and opponent IS NULL;" % (id1,)
    else:
        findMatch = "SELECT * FROM matches where contestant = %s " \
            " and opponent = %s;" % (id1, id2,)
    conn = connect()
    c = conn.cursor()
    c.execute(findMatch)
    match = c.fetchall()
    conn.close()
    return len(match) == 1


def reportMatch(contestant, opponent, result):
    """
    Records the outcome of a single match between two players.
    Reads as contestant faced opponent and result was

    Args:
      contestant:  the id number of the player who won
      opponent:  the id number of the player who lost
      result: result of the match
    """
    if contestant is None:
        result == 'l'
    if result == 'w':
        contestantResult = 'w'
        contestantPoints = 3
        opponentResult = 'l'
        opponentPoints = 0
    if result == 'l':
        contestantResult = 'l'
        contestantPoints = 0
        opponentResult = 'w'
        opponentPoints = 3
    if result == 't':
        contestantResult = opponentResult = 't'
        contestantPoints = opponentPoints = 1
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches VALUES (%s,%s,%s,%s);",\
              (contestant, opponent, contestantResult, contestantPoints),)
    c.execute("INSERT INTO matches VALUES (%s,%s,%s,%s);",\
              (opponent, contestant, opponentResult, opponentPoints),)
    conn.commit()
    conn.close()


def findplayed(player):
    if player[0] == None:
        findplayed = "SELECT opponent FROM matches where " \
                  "contestant is null;"
    else:
        findplayed = "SELECT opponent FROM matches where " \
              "contestant = %s ;" % player[0]
    return findplayed


def tournamentfind(tournament):
    if tournament is None:
        test2 = "SELECT * FROM standings ORDER BY points ASC, omw ASC;"
    else:
        test2 = "SELECT * FROM %s ORDER BY points ASC, omw ASC;" % tournament
    return test2


def swissPairings(tournament=None):
    """
    Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    shuffleCount = 0
    tuples = ()
    conn = connect()
    c = conn.cursor()
    c.execute(tournamentfind(tournament))
    playerPool = c.fetchall()
    if len(playerPool) % 2 != 0:
        playerPool.insert(0, (None, None,))
    while len(playerPool) > 0:
        player = playerPool[0]
        c.execute(findplayed(player))
        cantPlay = c.fetchall()
        cantPlay.append((player[0],))
        canPlay = [x for x in playerPool if x[0] not in [i[0] for i in cantPlay]]
        if not canPlay:
            redo = tuples[-1]
            if shuffleCount > 3:
                tuples = tuples[:-1]
                redo = redo + tuples[-1]
            while redo:
                playerPool.append(redo[0:2])
                redo = redo[2:]
            tuples = tuples[:-1]
            shuffleCount +=1
            continue
        player2 = canPlay[0]
        playerPool.remove(player2)
        playerPool.remove(player)
        tuples = tuples + ((player[0], player[1], player2[0], player2[1],),)
    conn.close()
    return tuples


def clearTournament(tournament):
    """
    Use to remove a tournament  and player in that specfic tournament
    from database
    """
    delTournament = "DROP VIEW IF EXISTS %s CASCADE;" % tournament
    delP = "DELETE FROM players CASCADE WHERE tournament = '%s';" % tournament
    conn = connect()
    c = conn.cursor()
    c.execute(delTournament)
    c.execute(delP)
    conn.commit()
    conn.close()
