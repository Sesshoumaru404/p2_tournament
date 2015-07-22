#!/usr/bin/env python
#
# Test cases for tournament.py

import math
import random
from tournament import *

contestant = (
    "Jeff",
    "John",
    "Sue",
    "Tiffany"
    # "Nina",
    # "Connor",
    # "Simone",
    # "Bryon",
    # "Paul"
)
findLog = math.log(len(contestant), 2)
totalRounds = math.ceil(findLog)


def addContestants(contestants, tournament):
    '''
    Create table for registered contestants
    '''
    if tournament is None or contestants is None:
        raise TypeError("Must have tournament name and contestants")
    for players in contestants:
        registerPlayer(players, tournament)
    playerStandings(tournament)
    print "Tournament %s with will last %d rounds." % (tournament,
                                                       totalRounds,)


def simtournament(contestants, tournament):
    '''
    This function is use to simulate a swiss pairing tournament.
    Take two arguements contestants which is a list of players and
    tournament which is the name of the tournament
    '''
    addContestants(contestants, tournament)
    for x in range(0, int(totalRounds)):
        pairings = swissPairings(tournament)
        for pairs in pairings:
            if pairs[2] == "bye":
                reportMatch(pairs[0], pairs[2], 'w')
                continue
            shuffle = ['w', 'l', 't']
            random.shuffle(shuffle)
            reportMatch(pairs[0], pairs[2], shuffle[0])
        # players = findtournament(tournament)
    final = findtournament(tournament)
    print "Final Results"
    for position, standings in enumerate(final):
        print "%r. %s with a record of w:%s t:%s l:%s" % (position + 1,
                                                          standings[1],
                                                          standings[2],
                                                          standings[3],
                                                          standings[4],)

simtournament(contestant, 'Fake_Tournament')

# clearTournament('Fake_Tournament')
