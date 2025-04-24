import re

# Defining which order the logical operaters are evalauted 5 is highest priority 1 is lowest 
# Source for thr precedence http://intrologic.stanford.edu/dictionary/operator_precedence.html
PRECEDENCE = {
    '↔': 1,
    '→': 2,
    '∨': 3,
    '∧': 4,
    '^': 4,
    '¬': 5
}

# Define node structure for a tree
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value  # Operator or variable
        self.left = left
        self.right = right

    def __repr__(self):
        if self.left and self.right:
            return f"({self.left} {self.value} {self.right})"
        elif self.left:
            return f"({self.value} {self.left})"
        else:
            return self.value

#Print the tree in order of operation        
def print_tree(node, indent=0):
    if node is None:
        return
    if node.right:
        print_tree(node.right, indent + 4)
    print(" " * indent + str(node.value))
    if node.left:
        print_tree(node.left, indent + 4)
        
# Tokenizer that will change a logical statement into individual items
#Input = (P → (Q ∧ R))
#Output = ['P', '→', '(', 'Q', '∧', 'R', ')']
def tokenize(expr):
    expr = expr.replace(" ", "")
    pattern = r'¬|∧|∨|→|↔|\^|\(|\)|[A-Za-z][A-Za-z0-9]*'
    return re.findall(pattern, expr)

#Parse - recursively creates a tree out of token and the precidence set
#Input = ['P', '→', '(', 'Q', '∧', 'R', ')']
#Output = First and R and Q together then → P)
def parse(tokens):
    def parse_expression(min_prec=0):
        token = tokens.pop(0)

        if token == '(':
            node = parse_expression()
            tokens.pop(0)  # remove ')'
        elif token == '¬':
            right = parse_expression(PRECEDENCE['¬'])
            node = Node('¬', right)
        else:
            node = Node(token)

        while tokens and tokens[0] in PRECEDENCE and PRECEDENCE[tokens[0]] >= min_prec:
            op = tokens.pop(0)
            prec = PRECEDENCE[op]
            right = parse_expression(prec + 1)
            node = Node(op, node, right)

        return node

    return parse_expression()
