-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create database
CREATE DATABASE tournament;
-- Connect to database
\c tournament;

-- Create tables
-- Create players table
-- player_id : the serial id of players
-- player_name : the name of each player
CREATE TABLE players (
    player_id serial primary key,
    player_name text
);

-- Create tournaments table
-- tournament_id : the serial id of tournaments
-- tournament_name : the name of each tournament
CREATE TABLE tournaments(
    tournament_id serial primary key,
    tournament_name text
);

-- Create matches table
-- match_id : the serial id of matches
-- winner_id : the int id of the winner player
-- loser_id : the int id of the loser player
-- tournament_id : the int id of the tournament that holds this match
-- if a player is deleted, his corresponding match will be deleted too.
-- if a tournament is deleted, the corresponding matches to this tournament will be deleted too.
CREATE TABLE matches(
    match_id serial primary key,
    winner_id int,
    loser_id int,
    tournament_id int,
    foreign key(winner_id) references players(player_id) on delete cascade,
    foreign key(loser_id) references players(player_id) on delete cascade,
    foreign key(tournament_id) references tournaments(tournament_id) on delete cascade
);

-- Create a table to old relations between players and tournaments
-- player_id : the int id of the player that is associated to tournament_id, the int id of the tournament
-- if a player is deleted, his corresponding tournament will be deleted too.
-- if a tournament is deleted, the corresponding tournament in this table will be deleted too.
CREATE TABLE players_in_tournaments(
    player_id int references players(player_id) on delete cascade,
    tournament_id int references tournaments(tournament_id) on delete cascade,
    primary key(player_id, tournament_id)
);