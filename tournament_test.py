#!/usr/bin/env python
#
# Test cases for tournament.py

# Citation: I looked at this project : https://github.com/samfrances/udacity-swiss-system-tournament
# to get guidance regarding write unit tests for the extra credit cases only.

from tournament import *

def testDeleteMatches():
    deleteMatches()
    print("1. Old matches can be deleted.")

def testDelete():
    deleteMatches()
    deletePlayers()
    print("2. Player records can be deleted.")

def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print("3. After deleting, countPlayers() returns zero.")

def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print("4. After registering a player, countPlayers() returns 1.")


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print("5. Players can be registered and deleted.")


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    player1 = registerPlayer("Melpomene Murray")
    player2 = registerPlayer("Randy Schwartz")
    tournament1 = createTournament("tournament1")
    standings = playerStandings(tournament1)
    if len(standings) != 0:
        raise ValueError("Players should not appear in tournament before being added to a one.")
    print("6. Players do not appear in a tournament's standing before being added to a one.")

    addPlayerToTournament(player1, tournament1)
    addPlayerToTournament(player2, tournament1)
    standings = playerStandings(tournament1)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print("7. Newly registered players appear in the standings with no matches.")


def testReportMatches():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament1 = createTournament("tournament1")
    player1 = registerPlayer("Bruno Walton")
    player2 = registerPlayer("Boots O'Neal")
    player3 = registerPlayer("Cathy Burton")
    player4 = registerPlayer("Diane Grant")
    addPlayerToTournament(player1, tournament1)
    addPlayerToTournament(player2, tournament1)
    addPlayerToTournament(player3, tournament1)
    addPlayerToTournament(player4, tournament1)

    standings = playerStandings(tournament1)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, tournament1)
    reportMatch(id3, id4, tournament1)
    standings = playerStandings(tournament1)
    for (i, n, w, m) in standings:

        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print("7. After a match, players have updated standings.")


def testPairings():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament1 = createTournament("tournament1")
    player1 = registerPlayer("Twilight Sparkle")
    player2 = registerPlayer("Fluttershy")
    player3 = registerPlayer("Applejack")
    player4 = registerPlayer("Pinkie Pie")
    addPlayerToTournament(player1, tournament1)
    addPlayerToTournament(player2, tournament1)
    addPlayerToTournament(player3, tournament1)
    addPlayerToTournament(player4, tournament1)

    standings = playerStandings(tournament1)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, tournament1)
    reportMatch(id3, id4, tournament1)
    pairings = swissPairings(tournament1)

    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print("9. After one match, players with one win are paired.")

def testDeleteTournaments():
    deleteTournaments()
    print("10. Old tournaments can be deleted.")

    # Check that there are no tournaments in the table
    db, cursor = connect()
    number_of_tournaments_query = "SELECT COUNT(*) FROM tournaments;"
    cursor.execute(number_of_tournaments_query)
    count = cursor.fetchall()[0][0]
    db.close()
    if count != 0:
        raise ValueError("After running deleteTournaments(), there should be 0 tournaments.")
    print("11. After running deleteTournament(), there are 0 tournaments.")

def testCreateTournament():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament_id = createTournament("Dummy Tournament 1")

    # Check that createTournament returns the tournament id
    if not isinstance(tournament_id, int):
        raise ValueError("createTournament() should return an integer id.")
    print("12. createTournament() returns an integer id.")

    # Check that there is only one tournament in the table
    count = getCurrentTournamentsCount()
    if count != 1:
        raise ValueError("After running createTournament(), there should be 1 tournament in the database.")
    print("13. After running createTournament(), there is only 1 tournament in the database.")

    createTournament("Dummy Tournament 2")

    count = getCurrentTournamentsCount()
    if count != 2:
        raise ValueError("After running createTournament() again, there should be 2 tournaments in the database.")
    print("14. After running createTournament() again, 2 tournaments exists in the database.")

def getCurrentTournamentsCount():
    db, cursor = connect()
    number_of_tournaments_query = "SELECT COUNT(*) FROM tournaments;"
    cursor.execute(number_of_tournaments_query)
    count = cursor.fetchall()[0][0]
    db.close()
    return count

def testAddPlayerToTournament():
    deleteMatches()
    deletePlayers()
    deleteTournaments()

    tournament1 = createTournament("tournament1")
    tournament2 = createTournament("tournament2")
    player1 = registerPlayer("Mark")
    player2 = registerPlayer("Angelina")
    player3 = registerPlayer("Tom")

    addPlayerToTournament(player1, tournament1)
    addPlayerToTournament(player2, tournament2)
    addPlayerToTournament(player3, tournament2)

    # test tournament1
    db, cursor = connect()
    get_players_in_tournament_query = "SELECT * FROM players_in_tournaments WHERE tournament_id=(%s)"
    cursor.execute(get_players_in_tournament_query, (tournament1,))
    rows = cursor.fetchall()

    if len(rows) != 1:
        raise ValueError("One entry should exist only in tournament1.")
    print("15. One entry exists only in tournament1.")

    if rows[0][0] != player1:
        raise ValueError("The id of the player added to tournament 1 should equal {0}".format(player1))
    print("16. Correct player added to tournament1.")

    # test tournament 2
    cursor.execute(get_players_in_tournament_query, (tournament2,))
    rows = cursor.fetchall()

    if len(rows) != 2:
        raise ValueError("Two entries should exist only in tournament2.")
    print("17. Two entries exist in tournament2.")

    if set([rows[0][0], rows[1][0]]) != set([player2, player3]):
        raise ValueError("The id of the players added to tournament 2 should equal {0} and {1}".format(player2, player3))
    print("18. Correct players added to tournament2.")

def testCountByTournament():
    deleteMatches()
    deletePlayers()
    deleteTournaments()

    tournament1 = createTournament("tournament1")
    tournament2 = createTournament("tournament2")
    player1 = registerPlayer("Mark")
    player2 = registerPlayer("Angelina")
    player3 = registerPlayer("Ali")

    if countPlayers(tournament1) > 0:
        raise ValueError("Tournament 1 should have 0 entries.")
    if countPlayers(tournament2) > 0:
        raise ValueError("Tournament 2 should have 0 entries.")

    addPlayerToTournament(player1, tournament1)

    if countPlayers(tournament1) != 1:
        raise ValueError("Tournament 1 should have 1 entries.")
    if countPlayers(tournament2) > 0:
        raise ValueError("Tournament 2 should have 0 entries.")

    addPlayerToTournament(player2, tournament2)

    if countPlayers(tournament1) != 1:
        raise ValueError("Tournament 1 should have 1 entries.")
    if countPlayers(tournament2) != 1:
        raise ValueError("Tournament 2 should have 1 entries.")

    addPlayerToTournament(player3, tournament2)

    if countPlayers(tournament1) != 1:
        raise ValueError("Tournament 1 should have 1 entries.")
    if countPlayers(tournament2) != 2:
        raise ValueError("Tournament 2 should have 2 entries.")

    print "19. countPlayers returns the right number for each tournament's players."

def testStandingsBeforeMatchesByTournament():
    deleteMatches()
    deletePlayers()
    deleteTournaments()

    player1 = registerPlayer("Sam")
    player2 = registerPlayer("Randy")
    player3 = registerPlayer("Bob")
    tournament1 = createTournament("tournament1")
    tournament2 = createTournament("tournament2")

    # Test that standings are empty before players enter tournaments
    standings_t1 = playerStandings(tournament1)
    standings_t2 = playerStandings(tournament2)
    if len(standings_t1) != 0 or len(standings_t2) != 0:
        raise ValueError("Players should not appear in a tournament's standings before they have entered any tournaments")
    print "20. Players do not appear in a tournament's standings before they enter a tournament"

    addPlayerToTournament(player1, tournament1)
    addPlayerToTournament(player2, tournament1)
    addPlayerToTournament(player2, tournament2)
    addPlayerToTournament(player3, tournament2)

    standings = playerStandings(tournament1)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Sam", "Randy"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")

    standings = playerStandings(tournament2)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Randy", "Bob"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")

    print "21. Newly registered players appear in the standings with no matches, for any tournaments entered."

def testReportMatchesByTournament():
    # Modified to work with a database allowing multiple tournaments
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament1 = createTournament("t1")
    tournament2 = createTournament("t2")
    player1 = registerPlayer("Bruno Walton")
    player2 = registerPlayer("Boots O'Neal")
    player3 = registerPlayer("Cathy Burton")
    player4 = registerPlayer("Diane Grant")
    player5 = registerPlayer("Joe Malik")
    player6 = registerPlayer("Ted, son of Ed")
    addPlayerToTournament(player1, tournament1)
    addPlayerToTournament(player2, tournament1)
    addPlayerToTournament(player3, tournament1)
    addPlayerToTournament(player4, tournament1)
    addPlayerToTournament(player2, tournament2)
    addPlayerToTournament(player3, tournament2)
    addPlayerToTournament(player4, tournament2)
    addPlayerToTournament(player5, tournament2)

    reportMatch(player1, player2, tournament1)
    reportMatch(player3, player4, tournament1)

    reportMatch(player3, player4, tournament2)
    reportMatch(player5, player2, tournament2)

    if len(getPlayedMatches(tournament1)) != 2 or len(getPlayedMatches(tournament2)) != 2:
        raise ValueError("There should be two matches in each tournament")

    for (i, n, w, m) in playerStandings(tournament1):
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (player1, player3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (player2, player4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")

    for (i, n, w, m) in playerStandings(tournament2):
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (player3, player5) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (player4, player2) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")

    print "22. After a match, players have updated standings for the relevant tournament."

def testDeleteMatchesByTournament():
    # Clean out database
    deleteMatches()
    deletePlayers()
    deleteTournaments()

    tournament1 = createTournament("t1")
    tournament2 = createTournament("t2")
    player1 = registerPlayer("Bob")
    player2 = registerPlayer("Tim")
    player3 = registerPlayer("Dave")

    addPlayerToTournament(player1, tournament1)
    addPlayerToTournament(player2, tournament1)
    addPlayerToTournament(player3, tournament1)
    addPlayerToTournament(player1, tournament2)
    addPlayerToTournament(player2, tournament2)
    addPlayerToTournament(player3, tournament2)

    reportMatch(player1, player2, tournament1)
    reportMatch(player2, player3, tournament2)

    if getPlayedMatches(tournament1) != [(player1, player2)] or getPlayedMatches(tournament2) != [(player2, player3)]:
        raise ValueError("Match reporting not working")

    deleteMatches(tournament2)

    if getPlayedMatches(tournament1) != [(player1, player2)]:
        raise ValueError("deleteMatches() has deleted too much")

    if getPlayedMatches(tournament2) != []:
        raise ValueError("deleteMatches() has not deleted the matches from tournament t2")

    print "23. deleteMatches can delete matches from a named tournament, leaving the matches of other tournaments in place"

def testPlayerStandings():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament1 = createTournament("t1")
    tournament2 = createTournament("t2")
    p1 = registerPlayer("Bruno Walton")
    p2 = registerPlayer("Boots O'Neal")
    p3 = registerPlayer("Cathy Burton")
    p4 = registerPlayer("Diane Grant")
    p5 = registerPlayer("Bob, son of Tim")
    p6 = registerPlayer("Ted, son of Ed")

    addPlayerToTournament(p1, tournament1)
    addPlayerToTournament(p2, tournament1)
    addPlayerToTournament(p3, tournament1)
    addPlayerToTournament(p4, tournament1)

    addPlayerToTournament(p3, tournament2)
    addPlayerToTournament(p4, tournament2)
    addPlayerToTournament(p5, tournament2)
    addPlayerToTournament(p6, tournament2)

    # Tests
    reportMatch(p1, p4, tournament1)
    standings_t1 = iter(playerStandings(tournament1))
    if next(standings_t1) != (p1, "Bruno Walton", 1, 1):
        raise ValueError('The first row in the standings for tournament t1 should be ({0}, "Bruno Walton", 1, 1)'.format(p1))
    for row in standings_t1:
        if row[2] != 0:
            raise ValueError('{0} should have zero wins'.format(row[1]))
        if row[0] == p4:
            if row[3] != 1:
                raise ValueError('{0} should have a match count of 1'.format(row[1]))
        else:
            if row[3] != 0:
                raise ValueError('{0} should have a match count of 0'.format(row[1]))

    reportMatch(p3, p1, tournament1)
    standings_t1 = playerStandings(tournament1)
    if set(standings_t1) != set([(p1, "Bruno Walton", 1, 2),
                                 (p3, "Cathy Burton", 1, 1),
                                 (p2, "Boots O'Neal", 0, 0),
                                 (p4, "Diane Grant", 0, 1)]):
        raise ValueError("Player standings for tournament t1 are incorrect.")

    reportMatch(p4, p2, tournament1)
    standings_t1 = playerStandings(tournament1)
    if set(standings_t1) != set([(p1, "Bruno Walton", 1, 2),
                                 (p3, "Cathy Burton", 1, 1),
                                 (p2, "Boots O'Neal", 0, 1),
                                 (p4, "Diane Grant", 1, 2)]):
        raise ValueError("Player standings for tournament t1 are incorrect.")

    reportMatch(p3, p4, tournament2)
    standings_t2 = iter(playerStandings(tournament2))
    if next(standings_t2) != (p3, "Cathy Burton", 1, 1):
        raise ValueError('The first row in the standings for tournament t2 should be ({0}, "Cathy Burton", 1, 1)'.format(p3))
    for row in standings_t2:
        if row[2] != 0:
            raise ValueError('{0} should have zero wins'.format(row[1]))
        if row[0] == p4:
            if row[3] != 1:
                raise ValueError('{0} should have a match count of 1'.format(row[1]))
        else:
            if row[3] != 0:
                raise ValueError('{0} should have a match count of 0'.format(row[1]))

    reportMatch(p2, p1, tournament1)
    standings_t1 = playerStandings(tournament1)
    if set(standings_t1) != set([(p1, "Bruno Walton", 1, 3),
                                 (p3, "Cathy Burton", 1, 1),
                                 (p2, "Boots O'Neal", 1, 2),
                                 (p4, "Diane Grant", 1, 2)]):
        raise ValueError("Player standings for tournament t1 are incorrect.")

    reportMatch(p6, p3, tournament2)
    standings_t2 = playerStandings(tournament2)
    if set(standings_t2) != set([(p3, "Cathy Burton", 1, 2),
                                 (p4, "Diane Grant", 0, 1),
                                 (p5, "Bob, son of Tim", 0, 0),
                                 (p6, "Ted, son of Ed", 1, 1)]):
        raise ValueError("Player standings for tournament t2 are incorrect.")

    reportMatch(p3, p4, tournament1)
    standings_t1 = playerStandings(tournament1)
    if set(standings_t1) != set([(p1, "Bruno Walton", 1, 3),
                                 (p3, "Cathy Burton", 2, 2),
                                 (p2, "Boots O'Neal", 1, 2),
                                 (p4, "Diane Grant", 1, 3)]):
        raise ValueError("Player standings for tournament t1 are incorrect.")

    print "24. playerStandings() tracks match reporting accurately for multiple tournaments."

def testPairingByTournament():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament1 = createTournament("t1")
    tournament2 = createTournament("t2")
    p1 = registerPlayer("Twilight Sparkle")
    p2 = registerPlayer("Fluttershy")
    p3 = registerPlayer("Applejack")
    p4 = registerPlayer("Pinkie Pie")
    p5 = registerPlayer("Cathy Burton")
    p6 = registerPlayer("Diane Grant")
    p7 = registerPlayer("Bob, son of Tim")
    addPlayerToTournament(p1, tournament1)
    addPlayerToTournament(p2, tournament1)
    addPlayerToTournament(p3, tournament1)
    addPlayerToTournament(p4, tournament1)
    addPlayerToTournament(p4, tournament2)
    addPlayerToTournament(p5, tournament2)
    addPlayerToTournament(p6, tournament2)
    addPlayerToTournament(p7, tournament2)

    reportMatch(p1, p2, tournament1)
    reportMatch(p3, p4, tournament1)

    reportMatch(p4, p5, tournament2)
    reportMatch(p6, p7, tournament2)

    pairings1 = swissPairings(tournament1)
    if len(pairings1) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings1
    correct_pairs = set([frozenset([p1, p3]), frozenset([p2, p4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")

    pairings2 = swissPairings(tournament2)
    if len(pairings2) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings2
    correct_pairs = set([frozenset([p4, p6]), frozenset([p5, p7])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")

    print "25. After one match in each of two tournaments, players with one win are paired."

if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()

    testDeleteTournaments()
    testCreateTournament()
    testAddPlayerToTournament()
    testCountByTournament()
    testStandingsBeforeMatchesByTournament()
    testReportMatchesByTournament()
    testDeleteMatchesByTournament()
    testPlayerStandings()
    testPairingByTournament()
    print("Success!  All tests pass!")


