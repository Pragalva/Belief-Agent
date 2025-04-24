from Agent import Agent
from Parser import *
from Evaluator import *

expr = "(P ↔ (Q ∨ R))"
print(find_assignments_that_make_true(expr))

