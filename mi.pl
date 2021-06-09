:- use_module(world).
:- use_module(rules).
:- use_module(inference).

% Execute meta interpreter
mi(Actions) :-
        findall(X, rule(X), Rules),
        try_rules(Rules, Actions).
