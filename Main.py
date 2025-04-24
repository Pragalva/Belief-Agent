from Agent import Agent
from Parser import *
from Evaluator import *
from CNF_converter import *

BeliefBase = Agent()
expr = "(P ↔ (Q ∨ R))"
expr2 = "¬P ∧ P"
BeliefBase.expand(expr)
BeliefBase.expand("P")

print("Belief Base:", expr)
print(find_assignments_that_make_true(expr))
print("Consistency:", is_consistent(find_assignments_that_make_true(expr)))

'''
belief_agent.expand(expr)
print(belief_agent.beliefs)
#print(find_assignments_that_make_true(expr))

CNF = belief_agent.combine_with_and()
print(CNF)
print(find_assignments_that_make_true(CNF))
print(len(find_assignments_that_make_true(CNF)))

print(to_cnf(parse(tokenize(expr))))
'''