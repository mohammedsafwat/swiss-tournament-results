#Description#
A Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.
The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated,
and each player should be paired with another player with the same number of wins, or as close as possible.

#Classes:#
###tournament.sql###

Contains the sql schema for our database. We create four tables in the database:
- players : a table holding the player names and their serial ids.
- tournaments : a table holding the tournaments names and their serial ids.
- players_in_tournaments : a table holding the relation between each player and his tournaments. Each inserted player_id
will have a tournament_id.
- matches : a table holding the matches results for each match played. It records the id of the winner, the id of the
loser, and the id of the tournament that they played inside, and records the serial number of the played match too.

###tournament.py###

holds the implementation of the needed methods to construct a Swiss-system tournament.

- deleteTournaments(): Deletes all tournaments from database.

- deleteMatches(tournament=None): If a tournament id number is passed, delete that tournament's matches, else,
remove all the match records from the database.

- deletePlayers(): Removes all the player records from the database.

- createTournament(name): Creates a new tournament.

- addPlayerToTournament(player_id, tournament): Adds a player to a specific tournament

- countPlayers(tournament=None): if a tournament id is passed, count the number of players added to this tournament, else
return the all number of players currently registered.

- registerPlayer(name): Adds a player to the tournament database.

- playerStandings(tournament): Returns a list of the players and their win records, sorted by wins.

- reportMatch(winner, loser, tournament): Records the  outcome of a single match between two players.

- getPlayedMatches(tournament): Returns the list of matches played in a specific tournament.

- swissPairings(tournament): Returns a list of pairs of players for the next round of a match for a specific tournament.

###tournament_test.py###

Contains a set of unit tests for the Swiss-system tournament methods implementation.

#How to run:#
- Clone the whole directory to your local machine.
- Open the psql command line interface, and run "\i tournament.sql". This will build the database, connect to it and create database tabes.
- You will get four tables created after that, according to the schema in "tournament.sql"
- You can change the database name from "tournament.sql", from this line CREATE DATABASE [database name];.
- After that, you can run "tournament_test.py" to run the unit tests. Make sure that you are in the project's directory and run "python tournament_test.py" in terminal.
- Everything is running well when the last printed statement to console is "Success!  All tests pass!".

#Modules Used:#
- psycopg2
- bleach
###You can install both modules using pip install [module name] from your terminal.###

