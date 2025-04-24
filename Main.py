from Agent import Agent
from Parser import *
from Evaluator import *

BeliefBase = Agent()
expr = "(P ↔ (Q ∨ R))"
expr2 = "¬P ∧ P"
BeliefBase.expand(expr)
BeliefBase.expand("P")

print("Belief Base:", expr)
print(find_assignments_that_make_true(expr))
print("Consistency:", is_consistent(find_assignments_that_make_true(expr)))

