from Parser import *
import itertools

def evaluate_tree(node, assignment):
    # If the node is a variable (leaf node)
    if node.left is None and node.right is None:
        if node.value in assignment:
            return assignment[node.value]  # Return the truth value from the assignment
        return node.value  # Return the symbolic variable if not assigned

    # Negation (¬)
    elif node.value == '¬':
        operand = evaluate_tree(node.left, assignment)
        if operand == True:
            return False
        elif operand == False:
            return True
        return f"¬{operand}"  # Return the negation symbolically if operand is not assigned

    # Conjunction (AND) (∧ or ^)
    elif node.value in ('∧', '^'):
        left = evaluate_tree(node.left, assignment)
        right = evaluate_tree(node.right, assignment)

        if left == False or right == False:
            return False
        elif left == True and right == True:
            return True
        elif left == True:
            return right
        elif right == True:
            return left
        return f"({left} ∧ {right})"  # Return the expression symbolically if undetermined

    # Disjunction (OR) (∨)
    elif node.value == '∨':
        left = evaluate_tree(node.left, assignment)
        right = evaluate_tree(node.right, assignment)

        if left == True or right == True:
            return True
        elif left == False and right == False:
            return False
        elif left == False:
            return right
        elif right == False:
            return left
        return f"({left} ∨ {right})"

    # Implication (→)
    elif node.value == '→':
        left = evaluate_tree(node.left, assignment)
        right = evaluate_tree(node.right, assignment)

        if left == False or right == True:
            return True
        elif left == True and right == False:
            return False
        elif left == True:
            return right
        elif right == False:
            return f"¬{left}"  # True → False is False: means ¬left
        return f"({left} → {right})"

    # Biconditional (↔)
    elif node.value == '↔':
        left = evaluate_tree(node.left, assignment)
        right = evaluate_tree(node.right, assignment)

        if isinstance(left, bool) and isinstance(right, bool):
            return left == right  # Biconditional is true if both sides are equal

        return f"({left} ↔ {right})"

    # Fallback for any unhandled case
    return node.value

def find_assignments_that_make_true(expr):
    # Tokenize and parse the expression
    tokens = tokenize(expr)
    root = parse(tokens)

    # Extract variables from the expression
    variables = set(re.findall(r'[A-Za-z]+', expr))  # Only variables are alphabetic strings

    # Generate all possible assignments for the variables
    all_assignments = list(itertools.product([True, False], repeat=len(variables)))

    valid_assignments = []
    for assignment_tuple in all_assignments:
        assignment = dict(zip(variables, assignment_tuple))  # Create assignment dictionary
        result = evaluate_tree(root, assignment)
        
        if result == True:
            valid_assignments.append(assignment)
    
    return valid_assignments

def is_consistent(valid_assignments):
    """Check if there is any assignment that makes the expression true."""
    return len(valid_assignments) > 0

def longest_remainders_by_length(remainders):
    """Return all remainder sets with the maximum number of beliefs."""
    if not remainders:
        return []

    max_len = max(len(r) for r in remainders)
    return [r for r in remainders if len(r) == max_len]

def remainders_with_shortest_avg_clause_length(remainders):
    """Return remainders with the shortest average clause length."""
    if not remainders:
        return []

    def avg_clause_length(r):
        return sum(len(clause) for clause in r) / len(r) if r else float('inf')

    min_avg = min(avg_clause_length(r) for r in remainders)
    return [r for r in remainders if avg_clause_length(r) == min_avg]

def partial_meet (remainders):
    """Give back the intersection of the remainders."""
    if len(remainders) == 0:
        return set()
    
    intersection = remainders[0]
    for remainder in remainders[1:]:
        intersection = intersection.intersection(remainder)
    return intersection
