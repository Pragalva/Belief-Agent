from Evaluator import*
from Parser import*
from CNF_converter import *
from itertools import chain,combinations

'''
def negate(literal: str) -> str:
    return literal[1:] if literal.startswith('¬') else f"¬{literal}"


def is_complementary(literal_1: str, literal_2: str):
    return negate(literal_1) == literal_2


def resolve(clause_i, clause_j):
    resolvents = []
    for literal_1 in clause_i:
        for literal_2 in clause_j:
            if is_complementary(literal_1.strip(), literal_2.strip()):
                new_clause = list(set(clause_i + clause_j) - {literal_1, literal_2})
                resolvents.append(new_clause)
    return resolvents


def resolution(clauses):
    clauses = [frozenset(clause) for clause in clauses]
    new = set()
    while True:
        pairs = combinations(clauses, 2)
        for (clause_i, clause_j) in pairs:
            for resolvent in resolve(list(clause_i), list(clause_j)):
                resolution_set = frozenset(resolvent)
                if not resolution_set:
                    return True  # contradiction
                new.add(resolution_set)
        if new.issubset(set(clauses)):
            return False
        clauses.extend(list(new))


def entails(base, phi):   
    base_clauses = []
    for f in base:
        f_tree = parse(tokenize(f))
        base_clauses.extend(to_cnf(f_tree))
    neg_phi= negate(phi)
    phi_tree = parse(tokenize(neg_phi))
    phi_negated = to_cnf(phi_tree)
    return resolution(base_clauses + phi_negated)
'''

def powerset(iterable):
    s = list(iterable)
    print(s)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))

def get_all_subsets(input_set):
    """
    Returns all possible subsets of the input set as a list of sets.
        
    Parameters:
    input_set (set): A set of strings.

    Returns:
    List[set]: A list containing all subsets of the input set.
    """
    s = list(input_set)
    subsets = list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))
    return [set(subset) for subset in subsets]
    

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
    #def contract(self, belief):
    #    remainders = find_remainders(self.beliefs, belief)
    #    ...

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
        #print(combined)
        return f'({combined})'
    
    

    #Function to create a tree out of the belief base
    def parse_base(self):
        return parse(self.combine_with_and())
    
    def entail(self, phi):
        not_phi = f"¬({phi})"

        # Make a shallow copy to avoid modifying self
        temp_agent = Agent()
        temp_agent.beliefs = self.beliefs.copy()

        # Tokenize and parse ¬φ, then convert to string and add
        tokens = tokenize(not_phi)
        not_phi_tree = parse(tokens)
        not_phi_str = str(not_phi_tree)  # Store as string in the belief base
        temp_agent.expand(not_phi_str)

        # Parse base from tokenized belief string
        tokens = tokenize(temp_agent.combine_with_and())
        #print(tokens)
        temp_base = parse(tokens)
        #CNF = to_cnf_str(temp_agent.combine_with_and())

        #print(find_assignments_that_make_true(temp_agent.combine_with_and()))
        # Check consistency of the temporary belief base
        if len(find_assignments_that_make_true(temp_agent.combine_with_and())) == 0:
            return True  # ¬φ leads to contradiction ⇒ φ is entailed
        else:
            return False
        
    '''def find_remainders(self, phi):
        remainders = []
        base = self.beliefs
        for subset in powerset(base):
            temp_agent = Agent()
            temp_agent.beliefs = subset
            if not temp_agent.entail(phi):
                if all(not (subset < other and not temp_agent.entail(phi)) for other in powerset(base)):
                    remainders.append(subset)
        #print(remainders)
        return remainders'''

    '''def find_remainders(self, phi):
        remainders = []
        base = self.beliefs

        # Generate all subsets of the belief base
        all_subsets = get_all_subsets(base)

        # Loop through all subsets
        for subset in all_subsets:
            temp_agent = Agent()
            temp_agent.beliefs = subset

            # Check if this subset entails phi
            if not temp_agent.entail(phi):
                print(f"Subset {subset} does not entail phi.")  # Debug print

                # Check if this subset is minimal
                is_minimal = True
                for other_subset in all_subsets:
                    # Proper subset check, but exclude empty set comparison
                    if other_subset < subset and other_subset != set():  
                        other_agent = Agent()
                        other_agent.beliefs = other_subset
                        if not other_agent.entail(phi):
                            is_minimal = False
                            print(f"Subset {subset} is not minimal because of {other_subset}.")  # Debug print
                            #break

                if is_minimal:
                    print(f"Adding {subset} to remainders.")  # Debug print
                    remainders.append(subset)

        return remainders'''
    def find_remainders(self, phi):
        remainders = set()
        base = self.beliefs

        for subset in get_all_subsets(base):
            temp_agent = Agent()
            temp_agent.beliefs = subset

            if not temp_agent.entail(phi):
                remainders.add(frozenset(subset))  # frozenset makes it hashable

        return remainders

    def Maximal_meet_contraction(self,phi):
            remainders = self.find_remainders(phi)
            max_remainder = max(remainders)
            self.beliefs = set(max_remainder)

    def Revison_with_Maximal(self,phi):
            not_phi = f"¬({phi})"
            self.Maximal_meet_contraction(not_phi)
            self.expand(phi)