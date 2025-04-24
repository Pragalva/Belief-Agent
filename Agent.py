from Evaluator import*
from Parser import*

class Agent:
    def __init__(self):
        self.beliefs = set()

    #Function to add to the belief base
    #Still need to check if it is logical add the belief
    def expand(self, belief):
        self.beliefs.add(belief)
    
    #Function to remove from the Belief base
    def contract(self, belief):
        remainders = find_remainders(self.beliefs, belief)
        ...

    #Function to show current belief
    def show(self):
        print("Beliefs:", self.beliefs)

    #Funtion is consistent
    def is_beliefs_consistent(self,assignment):
        beliefs_string = ' ∧ '.join(sorted(self.beliefs))
        parsed_beliefs = parse(beliefs_string)
        return(evaluate_tree(beliefs_string,assignment))
    
    #Make a dictionary with truth values
    def get_assignment(self):
        return {b: True for b in self.beliefs}
