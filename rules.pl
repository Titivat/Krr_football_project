:- module(rules, [rule/1, try_rules/2]).

:- use_module(world).
:- use_module(inference).

% empty rule
try_rules([], []) :- !, fail.

% execute each rule
try_rules([H|T], [Action]) :-
        (Condition -> Action) = H,
        prove(Condition);
        try_rules(T, [Action]).

% list of rules in form of Condition -> Action
rule(not has(_,ball) and closest_players_ball(P) and not goalkeeper(P) -> follow(P,ball)).
%rule(has(P,ball) and not goalkeeper(P) and player(P1) and not goalkeeper(P1) and is_same_team(P,P1) -> forward(P1)).
%rule(has(P1,ball) and not goalkeeper(P1) and player(P2) and not goalkeeper(P2) and not is_same_team(P1,P2) -> backward(P2)).
%rule(has(P1,ball) and not goalkeeper(P1) and closest_opponents(P1,[(P2,_)|_]) and not goalkeeper(P2) -> follow(P2,P1)).
%rule(has(P2,ball) and closest_opponents(P2,[(P1,D)|_]) and D =< 10 -> tackle(P1,P2)).
%rule(goalkeeper(P1) and team(T1,L) and is_member(P1,L) and player(P2) and has(P2,ball) and not is_same_team(P1,P2) and is_at(P2,X1,Y1) and shooting_zone(T1,X2,Y2,X3,Y3) and in(X1,Y1,X2,Y2,X3,Y3) -> tackle(P1,P2)).
%rule(goalkeeper(P1) and has(P1,ball) and player(P2) and not goalkeeper(P2) and is_same_team(P1,P2) -> backward(P2)).
%rule(has(P1, ball) and goalkeeper(P1) and closest_allies(P1,[(P2,D)|_]) and D =< 100 -> pass(P1,P2)).

rule(player(P) and back(P) and in_field(P) and not in_midfield_zone(P) -> forward(P)).
rule(player(P) and mid(P) and in_field(P) and not in_oponent_shooting_zone(P) -> forward(P)).
rule(player(P) and front(P) and in_field(P) and not in_oponent_shooting_zone(P) -> forward(P)).
rule(has(P,ball) and in_oponent_shooting_zone(P) -> shoot(P)).
