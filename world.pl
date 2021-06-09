:- module(world, [player/1, team/1, is_member/2, is_same_team/2]).

player(playerA1).
player(playerA2).
player(playerA3).
player(playerA4).
player(playerA5).
player(playerA6).
player(playerA7).

player(playerB1).
player(playerB2).
player(playerB3).
player(playerB4).
player(playerB5).
player(playerB6).
player(playerB7).

team([playerA1, playerA2, playerA3, playerA4, playerA5, playerA6, playerA7]).
team([playerB1, playerB2, playerB3, playerB4, playerB5, playerB6, playerB7]).

is_member(_,[]) :- !, fail.
is_member(X,[X|_]) :- !.
is_member(X,[_|T]) :-
        is_member(X,T), !.

is_same_team(X, Y) :- team(Z), player(X), player(Y), is_member(X, Z), is_member(Y, Z).
