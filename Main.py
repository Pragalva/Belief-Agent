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
expr8 ="¬C"
BeliefBase.expand(expr)
BeliefBase.expand(expr2)
BeliefBase.expand(expr3)
#BeliefBase.expand(expr3)

BeliefBase.show()

#print(BeliefBase.entail(expr3))
#print(BeliefBase.entail(expr5))
#print(BeliefBase.entail(expr7))
#print(BeliefBase.entail(expr6))
#print(BeliefBase.find_remainders(expr5))
#print(max(BeliefBase.find_remainders(expr7)))
#BeliefBase.Maximal_meet_contraction(expr6)
#BeliefBase.Revison_with_Maximal(expr8)
BeliefBase.partial_meet_contraction(expr5)


BeliefBase.show()
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