#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="p2_tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()

    query = "DELETE FROM matches;"
    cursor.execute(query)

    db.close()

def deletePlayers(tournament=None):
    """
    Remove all the player records from the database.
    And if statement to pass all project tests.
    """
    if tournament is None:
        query = "DELETE FROM players;"
        parameter = None
    else:
        query = "DELETE FROM players CASCADE WHERE tournament = '%s';"
        parameter = tournament

    db, cursor = connect()

    cursor.execute(query, parameter)

    db.commit()
    db.close()


def deleteTournament(tournament):
    """
    Remove a tournament and all the player records from the database.
    """
    delTournament = "DROP VIEW IF EXISTS %s CASCADE;" % tournament
    conn = connect()
    c = conn.cursor()
    c.execute(delTournament)
    deletePlayers(tournament)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()

    query = "SELECT * FROM players;"
    cursor.execute(query)

    db.close()


def registerPlayer(name, tournament=None):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()
    query = "INSERT INTO players (name, tournament) VALUES (%s, %s)",
    parameter = (name, tournament,)

    cursor.execute(query, parameter)
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
    '''
    Finds the current standings of for the named tournament.

    Args:
      Tournament: The tournament name which is a none required argument.
      Should be a single string, two word example
    '''
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM %s;" % tournament)
    currentTournament = c.fetchall()
    conn.close()
    return currentTournament


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
        contestantResult, contestantPoints = 'w', 3
        opponentResult, opponentPoints = 'l', 0
    if result == 'l':
        contestantResult, contestantPoints = 'l', 0
        opponentResult, opponentPoints = 'w', 3
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
    """
    Used make seach wording for finding players depeding case.
    """
    if player[0] == None:
        findplayed = "SELECT opponent FROM matches where contestant is null;"
    else:
        findplayed = "SELECT opponent FROM matches where " \
              "contestant = %s ;" % player[0]
    return findplayed


def tournamentfind(tournament):
    """
    Used make seach wording for getting a tournament depeding case.
    Returns players in lowerest to highest order, because bye matches are
    paired first and lower ranked players should play byes first.
    """
    if tournament is None:
        findT = "SELECT * FROM standings ORDER BY points ASC, omw ASC;"
    else:
        findT = "SELECT * FROM %s ORDER BY points ASC, omw ASC;" % tournament
    return findT


def swissPairings(tournament=None):
    """
    Returns a list of pairs of players for the next round of a match.

    Each player appears exactly once in the pairings.  Each player is paired
    with another player with an equal or nearly-equal win record, that is, a
    player adjacent to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    shuffleCount = 0
    pairings = ()
    conn = connect()
    c = conn.cursor()
    c.execute(tournamentfind(tournament))
    playerPool = c.fetchall()
    # Add fake player if odd players
    if len(playerPool) % 2 != 0:
        playerPool.insert(0, (None, None,))
    while len(playerPool) > 0:
        player = playerPool[0]
        c.execute(findplayed(player))
        cantPlay = c.fetchall()
        cantPlay.append((player[0],))
        canPlay = [x for x in playerPool if x[0] not in
                   [i[0] for i in cantPlay]]
        if not canPlay:
            redoPair = pairings[-1]
            if shuffleCount > 3:
                pairings = pairings[:-1]
                redoPair = redoPair + pairings[-1]
            while redoPair:
                playerPool.append(redoPair[0:2])
                redoPair = redoPair[2:]
            pairings = pairings[:-1]
            shuffleCount += 1
            continue
        player2 = canPlay[0]
        playerPool.remove(player2)
        playerPool.remove(player)
        pairings = pairings + ((player[0], player[1], player2[0],
                                player2[1],),)
    conn.close()
    return pairings
