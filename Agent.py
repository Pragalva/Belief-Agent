from Evaluator import*
from Parser import*

class Agent:
    def __init__(self):
        self.beliefs = set()

    #Function to add to the belief base
    #Still need to check if it is logical add the belief
    def expand(self, belief):
        if len(find_assignments_that_make_true(belief)) != 0:
            self.beliefs.add(belief)
        else:
            print('The belief you want to add is a contradiction')
    
    #Function to remove from the Belief base
    def contract(self, belief):
        self.beliefs.discard(belief)

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

    #Combine all the expression with a and in the belief set
    def combine_with_and(self):
        expressions = self.beliefs
        if not expressions:
            return ""        
        # Join all expressions with '∧'
        combined = ' ∧ '.join(expressions)
        # Wrap the whole expression in parentheses
        return f'({combined})'
