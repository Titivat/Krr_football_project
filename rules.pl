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
rule(has(P,ball) and in_oponent_shooting_zone(P) -> shoot(P)).
rule(has(P,ball) and not goalkeeper(P) -> forward(P)).
rule(has(P2,ball) and player(P) and in_field(P) and back(P) and not in_midfield_zone(P) and is_same_team(P,P2) -> forward(P)).
rule(has(P2,ball) and player(P) and in_field(P) and mid(P) and not in_oponent_shooting_zone(P) and is_same_team(P,P2) -> forward(P)).
rule(has(P2,ball) and player(P) and in_field(P) and front(P) and not in_oponent_shooting_zone(P) and is_same_team(P,P2) -> forward(P)).
rule(has(P2,ball) and closest_opponents(P2,[(P1,D)|_]) and D > 20 -> follow(P1,P2)).
rule(has(P1,ball) and goalkeeper(P1) and is_at(P1,X1,Y1) and shooting_zone(_,X2,Y2,X3,Y3) and in(X1,Y1,X2,Y2,X3,Y3) and closest_allies(P1,[(P2,D)|_]) and D =< 100 -> pass(P1,P2)).
rule(has(P2,ball) and goalkeeper(P2) and player(P) and in_field(P) and back(P) and is_same_team(P,P2) -> backward(P)).
rule(not has(_,ball) and goalkeeper(P) and is_at(ball,X1,Y1) and shooting_zone(_,X2,Y2,X3,Y3) and in(X1,Y1,X2,Y2,X3,Y3) -> follow(P,ball)).
