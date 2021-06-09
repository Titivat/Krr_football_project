:- module(rules, [rule/1, try_rules/2]).

:- use_module(world).
:- use_module(inference).

% empty rule
try_rules([], []) :- !, fail.

% execute each rule
try_rules([H|T], [Action]) :-
        (Condition -> Action) = H,
        prove(Condition);
        try_rules(T, Action).

% list of rules in form of Condition -> Actions
rule.
