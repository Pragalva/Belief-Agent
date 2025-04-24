from Parser import *

def eliminate_implications(node):
    if node is None:
        return None

    #Removing implications
    if node.value == '→':
        left = eliminate_implications(node.left)
        right = eliminate_implications(node.right)
        return Node('∨', Node('¬', eliminate_implications(left)), eliminate_implications(right))
    
    #Removing biimplications
    elif node.value == '↔':
        A = eliminate_implications(node.left)
        B = eliminate_implications(node.right)
        left = Node('∨', Node('¬', A), B)
        right = Node('∨', Node('¬', B), A)
        return Node('∧', left, right)

    elif node.value == '¬':
        return Node('¬', eliminate_implications(node.left))

    node.left = eliminate_implications(node.left)
    node.right = eliminate_implications(node.right)
    return node

def push_negations(node):
    if node is None:
        return None

    #Applying Demorgan's Law
    if node.value == '¬':
        inner = node.left
        if inner.value == '¬':
            return push_negations(inner.left)  # ¬¬A => A
        elif inner.value == '∧':
            return Node('∨', push_negations(Node('¬', inner.left)), push_negations(Node('¬', inner.right)))
        elif inner.value == '∨':
            return Node('∧', push_negations(Node('¬', inner.left)), push_negations(Node('¬', inner.right)))
        else:
            return Node('¬', push_negations(inner))

    node.left = push_negations(node.left)
    node.right = push_negations(node.right)
    return node

def distribute_or_over_and(node):
    #Distribute ∨ over ∧ to satisfy CNF.
    if node is None:
        return None

    node.left = distribute_or_over_and(node.left)
    node.right = distribute_or_over_and(node.right)

    if node.value == '∨':
        if node.left.value == '∧':
            A = node.left.left
            B = node.left.right
            C = node.right
            return Node('∧',
                        distribute_or_over_and(Node('∨', A, C)),
                        distribute_or_over_and(Node('∨', B, C)))
        elif node.right.value == '∧':
            A = node.right.left
            B = node.right.right
            C = node.left
            return Node('∧',
                        distribute_or_over_and(Node('∨', C, A)),
                        distribute_or_over_and(Node('∨', C, B)))
    return node

def to_cnf(node):
    """Convert a parsed expression tree to CNF."""
    node = eliminate_implications(node)
    node = push_negations(node)
    node = distribute_or_over_and(node)
    return node
