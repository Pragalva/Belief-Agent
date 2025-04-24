# Mastermind game
# 4 places, 3 colors (red, green, blue)

import random
from Agent import *
from itertools import permutations

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
    combination = generate_combinations(correct_positions)

    belief = "("
    for combi in combination:
        # Create a belief string based on the guess and the evaluation
        belief += "("
        for i in range(4):
            if combi[i]:
                belief += f"{guess[i]}{i+1} ∧ "
            else:
                belief += f"¬{guess[i]}{i+1} ∧ "
        belief = belief[:-3]  # Remove the last " ∧ "
        belief += ") ∨ "
    belief = belief[:-3]  # Remove the last " ∨ "
    belief += ")"
    BeliefBase.expand(belief)
    print("Belief added:", belief)   

    """Gained info by yellow guesses""" 
    
            

def next_guess(BeliefBase):
    """Generate the next guess based on the current beliefs."""
    CNF = BeliefBase.combine_with_and()
    possible_solutions = find_assignments_that_make_true(CNF)
    guess_values = [key for key,value in possible_solutions[0].items() if value == True]
    sorted_entries = sorted(guess_values, key=lambda x: int(x[1:])) #sort them by the second letter
    
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