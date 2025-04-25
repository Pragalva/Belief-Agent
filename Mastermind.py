# Mastermind game
# 4 places, 3 colors (red, green, blue)

import random
from Agent import *
from itertools import permutations
from collections import defaultdict

def generate_combinations(num_true):
    # Define the base combination: Two True values and Two False values
    base_combination = [True] * num_true + [False] * (4 - num_true)
    
    # Use permutations to generate all possible unique combinations of this base combination
    # Since permutations can repeat, we use set() to avoid duplicates
    unique_combinations = set(permutations(base_combination))

    return list(unique_combinations)

def generate_code():
    """Generate a random code of 4 colors from a set of 3 colors."""
    colors = ['R', 'G', 'B']
    return [random.choice(colors) for _ in range(4)]

def evaluate_guess(guess, code):
    """Evaluate the guess against the code."""    
    correct_positions = sum(guess[i] == code[i] for i in range(4)) #green hint
    correct_colors = sum(min(guess.count(c), code.count(c)) for c in set(guess)) - correct_positions #yellow hint
    return correct_positions, correct_colors

def add_to_belief_base(guess, correct_positions, correct_colors, BeliefBase):
    """Add the evaluation of the guess to the belief base."""
    #gained info by green guesses
    combination_g = generate_combinations(correct_positions)

    belief_g = "("
    for combi in combination_g:
        # Create a belief string based on the guess and the evaluation
        belief_g += "("
        for i in range(4):
            if combi[i]:
                belief_g += f"{guess[i]}{i+1} ∧ "
            else:
                belief_g += f"¬{guess[i]}{i+1} ∧ "
        belief_g = belief_g[:-3]  # Remove the last " ∧ "
        belief_g += ") ∨ "
    belief_g = belief_g[:-3]  # Remove the last " ∨ "
    belief_g += ")"
    BeliefBase.expand(belief_g)
    print("Green belief added:", belief_g)   

    #gained info by yellow guesses

    from collections import defaultdict

    combination_y = generate_combinations(correct_colors)

    # Step 1: Collect positions per color
    color_positions = defaultdict(list)
    for i, color in enumerate(guess):
        color_positions[color].append(i + 1)  # Positions are 1-indexed

    # Step 2: Create base clauses
    unique_clauses = []
    for color, positions in color_positions.items():
        # Other positions this color could be in
        other_positions = [f"{color}{j}" for j in range(1, 5) if j not in positions]
        negated_guesses = [f"¬{color}{j}" for j in positions]

        # If there are other places it could go, include them
        if other_positions:
            inner_clause = f"({' ∨ '.join(other_positions)}) ∧ {' ∧ '.join(negated_guesses)}"
        else:
            inner_clause = ' ∧ '.join(negated_guesses)

        unique_clauses.append(inner_clause)

    # Step 3: Combine clauses per combination
    belief_y = "("
    for combi in combination_y:
        belief_y += "("
        for include, clause in zip(combi, unique_clauses):
            if include:
                belief_y += f"({clause}) ∧ "
            else:
                belief_y += f"¬({clause}) ∧ "
        belief_y = belief_y[:-3] + ") ∨ "  # Remove last ' ∧ ', close group
    belief_y = belief_y[:-3] + ")"  # Remove last ' ∨ ', close group

    BeliefBase.expand(belief_y)
    print("Yellow belief added:", belief_y)
            

def next_guess(BeliefBase):
    """Generate the next guess based on the current beliefs."""
    CNF = BeliefBase.combine_with_and()
    possible_solutions = find_assignments_that_make_true(CNF)
    if len(possible_solutions) > 0:
        guess_values = [key for key,value in possible_solutions[0].items() if value == True]
        sorted_entries = sorted(guess_values, key=lambda x: int(x[1:])) #sort them by the second letter
    else:
        print("Mistake in clues... No possible solutions")
        return generate_code()
    
    new_guess = []
    for key in sorted_entries:
        new_guess.append(key[0])
    
    return new_guess

def game():
    ### INITIALIZE GAME ###
    print("Welcome to Mastermind!")
    code = generate_code()
    print("Randomly generated code: \t", code )  # For testing purposes

    ### AGENT INITIALIZATION ###
    BeliefBase = Agent()
    #initialize the belief base

    #there must be a color in each position
    BeliefBase.expand("(R1 ∨ G1 ∨ B1)")
    BeliefBase.expand("(R2 ∨ G2 ∨ B2)")
    BeliefBase.expand("(R3 ∨ G3 ∨ B3)")
    BeliefBase.expand("(R4 ∨ G4 ∨ B4)")

    # there can just be one color in each position
    BeliefBase.expand("(¬R1 ∨ ¬G1)")
    BeliefBase.expand("(¬G1 ∨ ¬B1)")
    BeliefBase.expand("(¬R1 ∨ ¬B1)")

    BeliefBase.expand("(¬R2 ∨ ¬G2)")
    BeliefBase.expand("(¬G2 ∨ ¬B2)")
    BeliefBase.expand("(¬R2 ∨ ¬B2)")

    BeliefBase.expand("(¬R3 ∨ ¬G3)")
    BeliefBase.expand("(¬G3 ∨ ¬B3)")
    BeliefBase.expand("(¬R3 ∨ ¬B3)")

    BeliefBase.expand("(¬R4 ∨ ¬G4)")
    BeliefBase.expand("(¬G4 ∨ ¬B4)")
    BeliefBase.expand("(¬R4 ∨ ¬B4)")

    next_guess(BeliefBase)


    #random initial guess
    guess = generate_code()
    print("1: \nInitial guess: \t \t \t", guess)
    correct_positions, correct_colors = evaluate_guess(guess, code)
    print("\t \t \t \t Green:", correct_positions, "Yellow:", correct_colors)
    add_to_belief_base(guess, correct_positions, correct_colors, BeliefBase)

    ### GAME LOOP ###
    i = 2
    while (not correct_positions == 4)and(i < 10):
        print(f"\n{i}:")
        i += 1
        #show the current beliefs
        BeliefBase.show()

        #make a guess
        guess = next_guess(BeliefBase)
        print("Guess: \t \t \t \t", guess)

        #evaluate the guess
        correct_positions, correct_colors = evaluate_guess(guess, code)
        print("Green:", correct_positions, "Yellow:", correct_colors)

        #add the guess to the belief base
        add_to_belief_base(guess, correct_positions, correct_colors, BeliefBase)

game()