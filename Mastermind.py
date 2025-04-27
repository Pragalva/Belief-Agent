# Mastermind game
# 4 places, 3 colors (red, green, blue)

import random
from Agent import *
from itertools import permutations
from collections import defaultdict

NUM_POS = 4
COLORS = ['R', 'G', 'B', 'Y']  # Red, Green, Blue, Yellow

def generate_combinations(num_true, NUM_POS=4):
    # Define the base combination: Two True values and Two False values
    base_combination = [True] * num_true + [False] * (NUM_POS - num_true)
    
    # Use permutations to generate all possible unique combinations of this base combination
    # Since permutations can repeat, we use set() to avoid duplicates
    unique_combinations = set(permutations(base_combination))

    return list(unique_combinations)

def generate_code():
    """Generate a random code."""
    return [random.choice(COLORS) for _ in range(NUM_POS)]

def evaluate_guess(guess, code):
    """Evaluate the guess against the code."""    
    correct_positions = sum(guess[i] == code[i] for i in range(NUM_POS)) #green hint
    correct_colors = sum(min(guess.count(c), code.count(c)) for c in set(guess)) - correct_positions #yellow hint
    return correct_positions, correct_colors


def build_xor_belief(clauses):
    """
    Build a logical formula where exactly one of the given clauses is true (XOR).
    """
    if len(clauses) == 1:
        return clauses[0]  # Only one option

    # Step 1: OR all clauses
    or_part = "(" + " ∨ ".join(clauses) + ")"

    # Step 2: NOT(AND) for every pair
    not_and_parts = []
    for i in range(len(clauses)):
        for j in range(i + 1, len(clauses)):
            not_and_parts.append(f"¬({clauses[i]} ∧ {clauses[j]})")

    and_not_and_part = "(" + " ∧ ".join(not_and_parts) + ")"

    # Step 3: Full XOR
    return f"({or_part} ∧ {and_not_and_part})"


def build_green_belief(guess, correct_positions, num_pos):
    """
    Build and expand the belief for Green hints (correct color, correct position).
    """
    combination_g = generate_combinations(correct_positions)

    belief_g_clauses = []
    for combi in combination_g:
        parts = []
        for i in range(num_pos):
            part = f"{guess[i]}{i+1}" if combi[i] else f"¬{guess[i]}{i+1}"
            parts.append(part)
        belief_g_clauses.append("(" + " ∧ ".join(parts) + ")")

    belief_g = build_xor_belief(belief_g_clauses)

    print("Green belief added:", belief_g)
    return belief_g


def build_yellow_belief(guess, correct_colors, num_pos):
    """
    Build and expand the belief for Yellow hints (correct color, wrong position).
    """
    combination_y = generate_combinations(correct_colors)

    color_positions = defaultdict(list)
    for i, color in enumerate(guess):
        color_positions[color].append(i + 1)

    unique_clauses = []
    for color, positions in color_positions.items():
        other_positions = [f"{color}{j}" for j in range(1, num_pos + 1) if j not in positions]
        negated_guesses = [f"¬{color}{j}" for j in positions]

        if other_positions:
            inner_clause = f"({' ∨ '.join(other_positions)}) ∧ {' ∧ '.join(negated_guesses)}"
        else:
            inner_clause = ' ∧ '.join(negated_guesses)
        
        unique_clauses.append(f"({inner_clause})")

    seen_clauses = set()
    belief_y_clauses = []
    for combi in combination_y:
        parts = []
        for include, clause in zip(combi, unique_clauses):
            part = clause if include else f"¬{clause}"
            parts.append(part)
        clause_str = " ∧ ".join(parts)
        if clause_str not in seen_clauses:
            seen_clauses.add(clause_str)
            belief_y_clauses.append(f"({clause_str})")

    belief_y = build_xor_belief(belief_y_clauses)

    print("Yellow belief added:", belief_y)
    return belief_y
    

def add_to_belief_base(guess, correct_positions, correct_colors, BeliefBase):
    """Add the guess and its evaluation to the belief base."""
    # Build beliefs for green and yellow hints
    belief_g = build_green_belief(guess, correct_positions, NUM_POS)
    belief_y = build_yellow_belief(guess, correct_colors, NUM_POS)
    
    BeliefBase.expand(belief_g)
    BeliefBase.expand(belief_y)


def next_guess(BeliefBase):
    """Generate the next guess based on the current beliefs."""
    CNF = BeliefBase.combine_with_and()
    possible_solutions = find_assignments_that_make_true(CNF)
    print("Possible solutions:", len(possible_solutions))
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
    for pos in range(1, NUM_POS + 1):
        clause = "(" + " ∨ ".join(f"{color}{pos}" for color in COLORS) + ")"
        BeliefBase.expand(clause)

    # there can just be one color in each position
    for pos in range(1, NUM_POS + 1):
        for i in range(len(COLORS)):
            for j in range(i + 1, len(COLORS)):
                clause = f"(¬{COLORS[i]}{pos} ∨ ¬{COLORS[j]}{pos})"
                BeliefBase.expand(clause)

    next_guess(BeliefBase)

    #random initial guess
    guess = generate_code()
    print("1: \nInitial guess: \t \t \t", guess)
    correct_positions, correct_colors = evaluate_guess(guess, code)
    print("\t \t \t \t Green:", correct_positions, "Yellow:", correct_colors)
    add_to_belief_base(guess, correct_positions, correct_colors, BeliefBase)

    ### GAME LOOP ###
    i = 2
    while (not correct_positions == NUM_POS)and(i < 10):
        print(f"\n{i}:")
        i += 1
        #show the current beliefs
        #BeliefBase.show()

        #make a guess
        guess = next_guess(BeliefBase)
        print("Guess: \t \t \t \t", guess)

        #evaluate the guess
        correct_positions, correct_colors = evaluate_guess(guess, code)
        print("Green:", correct_positions, "Yellow:", correct_colors)

        #add the guess to the belief base
        add_to_belief_base(guess, correct_positions, correct_colors, BeliefBase)

game()