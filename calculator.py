import ast
import operator
import sys

# Supported operators mapping from AST node to function
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def _eval(node):
    """Recursively evaluate an AST node representing an expression."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval(node.operand)
    if isinstance(node, ast.BinOp):
        if type(node.op) not in _OPERATORS:
            raise ValueError(f"Unsupported operator: {ast.dump(node.op)}")
        left = _eval(node.left)
        right = _eval(node.right)
        return _OPERATORS[type(node.op)](left, right)
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def evaluate_expression(expr):
    """Safely evaluate a math expression string and return the result."""
    parsed = ast.parse(expr, mode="eval")
    return _eval(parsed.body)

def repl():
    print("Simple Calculator. Enter 'quit' to exit.")
    while True:
        try:
            expr = input('> ')
        except EOFError:
            break
        if expr.strip().lower() in {'quit', 'exit'}:
            break
        if not expr.strip():
            continue
        try:
            result = evaluate_expression(expr)
        except Exception as exc:
            print(f"Error: {exc}")
        else:
            print(result)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            print(evaluate_expression(' '.join(sys.argv[1:])))
        except Exception as exc:
            sys.exit(f"Error: {exc}")
    else:
        repl()
