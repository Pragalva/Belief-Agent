from Agent import Agent
from Parser import *
from Evaluator import *
from CNF_converter import *

BeliefBase = Agent()
#{'B → C', 'A → B', 'A'}
expr = "(B → C)"
expr2 = "(A → B)"
expr3 = "A"
expr4 = "B"
expr5 = "C"
expr6 = "D"
expr7 = "(A → C)"
BeliefBase.expand(expr)
BeliefBase.expand(expr2)
BeliefBase.expand(expr3)

BeliefBase.show()

print(BeliefBase.entail(expr3))
print(BeliefBase.entail(expr5))
print(BeliefBase.entail(expr7))
print(BeliefBase.entail(expr6))
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