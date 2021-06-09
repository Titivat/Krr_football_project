:- module(inference, [op(250,fx,not), op(650,xfy,and), op(651,xfy,or), op/3, not/1, and/2, or/2, prove/1]).

:- op(250,fx,not).
:- op(650,xfy,and).
:- op(651,xfy,or).

not(A) :- prove(not A).
and(A,B) :- prove(A and B).
or(A,B) :- prove(A or B).

prove(true) :- !.
prove(not A) :- !, \+prove(A).
prove(A and B) :- !, prove(A), prove(B).
prove(A or B) :- prove(A), !; !, prove(B).
prove((A,B)) :- !, prove(A), prove(B).
prove(A) :- predicate_property(A,built_in), !, call(A).
prove(A) :- clause(A,B), prove(B).
