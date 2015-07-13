#!/usr/bin/env python
#
# Test cases for tournament.py

import math
import random
from tournament import *

contestants = (
    "Bob",
    "Billy",
    "Bill",
    "tere",
    "paul"
)


findLog = math.log(len(contestants),2)
totalRounds = math.ceil(findLog)

def addContestants(tournament):
    if tournament is None:
        raise TypeError("Must name tournament")
    for players in contestants:
        registerPlayer(players, tournament)
    playerStandings(tournament)
    playerCount = len(contestants)
    print "Tournament %s with will last %d rounds." % (tournament, totalRounds,)

def simtournament(tournament):
    addContestants(tournament)
    players = findtournament(tournament)
    # pairings = swissPairings(tournament)
    for x in range(0, int(totalRounds)):
        pairings = swissPairings(tournament)
        print pairings
        for pairs in pairings:
            if pairs[0] == "bye":
                reportMatch(pairs[2],pairs[0])
                continue
            if pairs[2] == "bye":
                reportMatch(pairs[0],pairs[2])
                continue
            shuffle = [pairs[0], pairs[2]]
            random.shuffle(shuffle)
            reportMatch(shuffle[0], shuffle[1])
        players = findtournament(tournament)

simtournament('fake')
