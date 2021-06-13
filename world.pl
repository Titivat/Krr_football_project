:- module(world, [player/1, team/2, goalkeeper/1, back/1, mid/1, front/1, is_at/3, field_zone/4, shooting_zone/5, midfield_zone/4, in/6, in_field/1, in_oponent_shooting_zone/1, in_midfield_zone/1, distance/3, has/2, is_member/2, is_same_team/2, closest_objects/2, closest_allies/2, closest_opponents/2, closest_players_ball/1, closest_players_ball/3]).

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

goalkeeper(playerA1).
goalkeeper(playerB1).

back(playerA2).
back(playerA3).
back(playerB2).
back(playerB3).

mid(playerA4).
mid(playerA5).
mid(playerA6).
mid(playerB4).
mid(playerB5).
mid(playerB6).

front(playerA7).
front(playerB7).

team(a, [playerA1, playerA2, playerA3, playerA4, playerA5, playerA6, playerA7]).
team(b, [playerB1, playerB2, playerB3, playerB4, playerB5, playerB6, playerB7]).

% location of object
%is_at(ball, 450, 300).

%is_at(playerA1, 0, 300).
%is_at(playerA2, 200, 200).
%is_at(playerA3, 200, 400).
%is_at(playerA4, 300, 200).
%is_at(playerA5, 300, 400).
%is_at(playerA6, 400, 200).
%is_at(playerA7, 400, 400).

%is_at(playerB1, 900, 300).
%is_at(playerB2, 700, 200).
%is_at(playerB3, 700, 400).
%is_at(playerB4, 600, 200).
%is_at(playerB5, 600, 400).
%is_at(playerB6, 500, 200).
%is_at(playerB7, 500, 400).

field_zone(20, 20, 1480, 770).

% shooting region
shooting_zone(a, 30, 0, 235, 800).
shooting_zone(b, 1260, 0, 1465, 800).

midfield_zone(600, 30, 970, 760).

% inside region
in(X1, Y1, X2, Y2, X3, Y3) :-
        X1 > X2,
        X1 < X3,
        Y1 > Y2,
        Y1 < Y3.

in_field(P) :-
        is_at(P, X1, Y1),
        field_zone(X2, Y2, X3, Y3),
        in(X1, Y1, X2, Y2, X3, Y3).

% inside oponent shooting zone
in_oponent_shooting_zone(P) :-
        is_at(P, X1, Y1),
        team(T1, L),
        is_member(P, L),
        shooting_zone(T2, X2, Y2, X3, Y3),
        T1 \= T2,
        in(X1, Y1, X2, Y2, X3, Y3).

in_midfield_zone(P) :-
        is_at(P, X1, Y1),
        midfield_zone(X2, Y2, X3, Y3),
        in(X1, Y1, X2, Y2, X3, Y3).

% calculate distance between two points
distance(O1, O2, D) :-
        is_at(O1, X1, Y1),
        is_at(O2, X2, Y2),
        D is sqrt((X2-X1)^2 + (Y2-Y1)^2).

is_member(_,[]) :- !, fail.
is_member(X,[X|_]) :- !.
is_member(X,[_|T]) :-
        is_member(X,T), !.

is_same_team(X, Y) :- team(_,Z), player(X), player(Y), is_member(X, Z), is_member(Y, Z), !.

closest_objects(X, SL) :-
        is_at(X,_,_),
        findall((Y,D), (is_at(Y,_,_), X \= Y, distance(X,Y,D)), UL),
        sort(2, @=<, UL, SL).

closest_allies(X, SL) :-
        is_at(X,_,_),
        findall((Y,D), (is_at(Y,_,_), Y \= ball, X \= Y, is_same_team(X,Y), distance(X,Y,D)), UL),
        sort(2, @=<, UL, SL).

closest_opponents(X, SL) :-
        is_at(X,_,_),
        findall((Y,D), (is_at(Y,_,_), Y \= ball, X \= Y, \+is_same_team(X,Y), distance(X,Y,D)), UL),
        sort(2, @=<, UL, SL).

closest_players_ball([], _, _).
closest_players_ball([H|T], P1, P2) :-
        \+is_same_team(P1,H),
        (P2,_) = H, !;
        closest_players_ball(T, P1, P2).
closest_players_ball(P) :-
        closest_objects(ball, [(P,_)|_]);
        closest_objects(ball, [(P1,_)|T]),
        closest_players_ball(T, P1, P).
