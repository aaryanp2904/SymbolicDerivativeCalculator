import re
import sympy
import math

# ---- Our "DiffLang" operators:

# -------- Unary Operators
# Num(n) - A literal number where n is an integer
# Exp(x) - A variable
# Neg(a) - Negative of another DiffLang (DL) literal
# Sin(a) - Sin of a DL literal
# Cos(a) - Cos of a DL literal
# Tan(a) - Tan of a DL literal
# Ln(a) - Ln of a DL literal

# --------- Binary Operators
# Add(a, b) - represents addition of two DL literals 'a' and 'b'
# Mul(a, b) - represents multiplication of two DL literals 'a' and 'b'
# Div(a,b) - represents division of two DL literals 'a' and 'b'
# Sub(a, b) - represents subtraction of two DL literals 'a' and 'b'
# Pow(a, Num(n)) - represents exponentiation of a DL literal 'a' to a power. This implementation only allows numerical powers (i.e. such that we can use power rule)

# ----


# Here are the regex patterns to match for each operator
ADD_REGEX = re.compile(r"^Add\((.*)\)$")
SUB_REGEX = re.compile(r"^Sub\((.*)\)$")
MUL_REGEX = re.compile(r"^Mul\((.*)\)$")
DIV_REGEX = re.compile(r"^Div\((.*)\)$")
NEG_REGEX = re.compile(r"^Neg\((.*)\)$")
SIN_REGEX = re.compile(r"^Sin\((.*)\)$")
COS_REGEX = re.compile(r"^Cos\((.*)\)$")
TAN_REGEX = re.compile(r"^Tan\((.*)\)$")
LN_REGEX = re.compile(r"^Ln\((.*)\)$")
POW_REGEX = re.compile(r"^Pow\((.*)\)$")

SYMBOLS = ["+", "^", "-", "*", "/"]


def main():
    try:

        while True:

            # Ask the user for the expression to differentiate and the point to find a derivative.
            expression = input("\nWhat would you like to calculate the derivative of?\n\n   - ").strip()
            evalVal = input(
                "\nEnter a numerical value if you would like to evaluate the derivative at a point.\n\n   - ").strip()

            # Try to parse the user input into our "DiffLang"
            expression = parse_user_input(expression)

            eqn = conv_exp_to_eqn(expression)

            dec = input(
                f"Would you like to calculate the derivative of {eqn}? If a term has the wrong sign, please put negative terms towards the end of a sum. (y/N) \n\n   - ").strip()

            if dec == "y":
                break

            print("\n Ok... re-enter input..\n")

        print(f"\n\n Printing derivative of {eqn}...")

        # Find the derivative of our expression
        deriv = get_deriv(expression)

    # In any case, if any error is thrown, this is due to wrong user input.
    except:
        print("There was an error with your input. Please check your expression syntax.")

    try:
        # Find the derivative of our expression
        deriv = get_deriv(expression)

    except:
        print("Unable to calculate derivative")

    try:

        # Check to see if the point provided is an integer or not
        evalVal = int(evalVal)

        # Print the derivative and its value at the point provided
        print(f"\n\n The simplified derivative is: \n\n {' ' * 20} {get_readable_deriv(expression)}")
        print(f"\n\n The derivative at x = {evalVal} is: \n\n {' ' * 30} {eval(deriv, evalVal)}")

    # If evalVal was indeed not an integer, inform the user
    except ValueError:
        print(f"{evalVal} is not a valid integer.")


def parse_user_input(expr):
    # Remove unnecessary whitespace
    expr = expr.strip()

    # Get rid of spaces in between
    expr = expr.replace(" ", "")

    # ---- Cover the base cases

    # Do we just have a variable...
    if expr == "x":
        return "Exp(x)"

    # Do we just have a variable with a coefficient
    if expr[-1] == "x" and expr[:-1].isnumeric():
        return f"Mul(Num({expr[:-1]}), Exp(x))"

    if re.search('^.*x\^[0-9]*$', expr):
        (coefficient, exponent) = expr.split("x^")
        if exponent.isnumeric():
            return f"Mul(Num({coefficient}), Pow(Exp(x), Num({exponent})))"

    # Do we just have a number
    if expr.isnumeric():
        return f"Num({expr})"

    # Do we have any of the trigonometric funcs
    if re.search('^sin(.*)$', expr):
        return f"Sin({parse_user_input(expr[4:-1])})"

    if re.search('^cos(.*)$', expr):
        return f"Cos({parse_user_input(expr[4:-1])})"

    if re.search('^tan(.*)$', expr):
        return f"Tan({parse_user_input(expr[4:-1])})"

    # Do we have the ln func
    if re.search('^ln(.*)$', expr):
        return f"Ln({parse_user_input(expr[3:-1])})"

    # Do we have a negative number
    if re.search('^-(.*)$', expr):
        return f"Neg({parse_user_input(expr[2:-1])})"

    # ----

    # Counter used to check if we have reached a matching bracket
    brackNum = 0

    # So we don't break the loop before we encounter the first bracket
    start = True

    # Iterate through every character in the expression
    for i in range(len(expr)):
        c = expr[i]

        # We have encountered another layer of brackets
        if c == "(":
            brackNum += 1
            start = False

        # The previous layer of brackets has closed
        elif c == ")":
            brackNum -= 1

        # If all open brackets were closed, the following character must be a symbol
        if brackNum == 0:  # and not start:

            # Find out what the symbol is
            symbol = get_symbol(expr[i + 1:])

            # Get the operands
            left_exp = get_left_exp(expr.split(symbol)[0])
            (right_exp, expr1) = get_right_exp(symbol.join(expr.split(symbol)[1:]))

            expr1 = expr1.strip()

            # Depending on the symbol, we choose our DiffLang operator
            if symbol == "+":
                operation = "Add"
            elif symbol == "-":
                operation = "Sub"
            elif symbol == "*":
                operation = "Mul"
            elif symbol == "/":
                operation = "Div"
            elif symbol == "^":
                operation = "Pow"

            # Form the DiffLang expression, making sure to recurse through the operands too
            if expr1 == "":
                return f"{operation}({parse_user_input(left_exp)}, {parse_user_input(right_exp)})"
            else:
                # Find out what the symbol is
                symbol = get_symbol(expr1)
                # Depending on the symbol, we choose our DiffLang operator
                if symbol == "+":
                    operation1 = "Add"
                elif symbol == "-":
                    val = f"Add({operation}({parse_user_input(left_exp)}, {parse_user_input(right_exp)}), Neg({parse_user_input(expr1[1:])}))"
                    return val
                elif symbol == "*":
                    operation1 = "Mul"
                elif symbol == "/":
                    operation1 = "Div"
                elif symbol == "^":
                    operation1 = "Pow"

                val = f"{operation1}({operation}({parse_user_input(left_exp)}, {parse_user_input(right_exp)}), {parse_user_input(expr1[1:])})"

                return val


def get_left_exp(expr):
    """
    Returns the first operand in an expression (i.e., the operand on the left)
    """

    # Remove unnecessary whitespace
    expr = expr.strip()

    # Counter used to check if we have reached a matching bracket
    brackNum = 0

    # So we don't break the loop before we encounter the first bracket
    start = True

    # Iterate through every character in reverse order in the expression
    for i in range(-1, -len(expr) - 1, -1):
        c = expr[i]

        # We have encountered a new close bracket
        if c == ")":
            brackNum += 1
            start = False

        # We have encountered an open bracket which matches the previous close bracket
        elif c == "(":
            brackNum -= 1

        # All close brackets have been matched hence everything enclosed within these
        # outermost brackets is our expression
        if brackNum == 0 and not start:
            return expr[i + 1:-1]

        if brackNum == 0 and c in SYMBOLS:
            return expr[:i + 1]

    return expr


def get_symbol(expr):
    for x in expr:
        if x in SYMBOLS:
            return str(x)


# def get_right_exp(expr):
#     """
#     Returns the second operand in an expression (i.e., the operand on the right)
#     """
#     # Remove unnecessary whitespace
#     expr = expr.strip()

#     # Counter used to check if we have reached a matching bracket
#     brackNum = 0

#     # So we don't break the loop before we encounter the first bracket
#     start = True

#     # Iterate through every character in the expression
#     for i in range(len(expr)):
#         c = expr[i]

#         # We have encountered another layer of brackets
#         if c == "(":
#             brackNum += 1
#             start = False

#         # The previous layer of brackets has closed
#         elif c == ")":
#             brackNum -= 1

#         # All open brackets have been matched hence everything enclosed within these
#         # outermost brackets is our expression
#         if brackNum == 0 and not start:
#             return expr[1:i]

#         if brackNum == 0 and c in ["+","^","-","*","/"]:
#             return expr[:i]

#     return expr

def get_right_exp(expr):
    """
    Returns tuple where first item is the second operand in an expression (i.e., the next operand on the right) and the second
    item is the rest of the expression
    """
    # Remove unnecessary whitespace
    expr = expr.strip()

    # Counter used to check if we have reached a matching bracket
    brackNum = 0

    # So we don't break the loop before we encounter the first bracket
    start = True

    # Iterate through every character in the expression
    for i in range(len(expr)):
        c = expr[i]

        # We have encountered another layer of brackets
        if c == "(":
            brackNum += 1
            start = False

        # The previous layer of brackets has closed
        elif c == ")":
            brackNum -= 1

        # All open brackets have been matched hence everything enclosed within these
        # outermost brackets is our expression
        if brackNum == 0 and not start:
            return (expr[1:i].strip(), remove_close_brackets(expr[i:]).strip())

        if brackNum == 0 and c in SYMBOLS and c != "^":
            return (expr[:i].strip(), remove_close_brackets(expr[i:]).strip())

    return (expr, "")


def remove_close_brackets(expr):
    for i in range(len(expr)):
        if expr[i] != ")":
            return expr[i:]
    return ""


def derivative_calc(expr):
    """
    Returns the derivative of a DiffLang expression as a DiffLang expression.
    """

    # Cover the base cases
    if re.search('^Num(.*)$', expr):
        return "Num(0)"

    if expr == "Exp(x)":
        return "Num(1)"

    # We simply use the chain rule on these more complex cases which will reduce to
    # base cases later on.
    if re.search('^Neg(.*)$', expr):
        mo = NEG_REGEX.search(expr)
        return f"Neg({derivative_calc(mo.groups()[0])})"

    if re.search('^Sin(.*)$', expr):
        mo = SIN_REGEX.search(expr)
        return f"Mul({derivative_calc(mo.groups()[0])}, Cos({mo.groups()[0]}))"

    if re.search('^Cos(.*)$', expr):
        mo = COS_REGEX.search(expr)
        return f"Neg(Mul({derivative_calc(mo.groups()[0])}, Sin({mo.groups()[0]})))"

    if re.search('^Tan(.*)$', expr):
        mo = TAN_REGEX.search(expr)
        return f"Div({derivative_calc(mo.groups()[0])}, Mul(Cos({mo.groups()[0]}), Cos({mo.groups()[0]}))"

    if re.search('^Ln(.*)$', expr):
        mo = LN_REGEX.search(expr)
        return f"Div({derivative_calc(mo.groups()[0])}, {mo.groups()[0]})"

    # Using the power rule for a polynomial
    if re.search('^Pow(.*)$', expr):
        mo = POW_REGEX.search(expr)
        (exp1, exp2) = get_inner_exps(mo.groups()[0])

        # Special cases - if the exponent is 0 then we just have to differentiate 1 which is just 0.
        if exp2 == "Num(0)":
            return "Num(0)"

        # If the exponent is 1 then we just differentiate the expression that is in the first argument.
        if exp2 == "Num(1)":
            return derivative_calc(exp1)

        # Implementing the power rule
        nminusone = int(exp2[4:-1]) - 1
        return f"Mul({derivative_calc(exp1)}, Mul({exp2}, Pow({exp1}, Num({nminusone}))))"

    # Derivative of a sum is the sum of the derivatives
    if re.search("^Add(.*)$", expr):
        mo = ADD_REGEX.search(expr)
        (exp1, exp2) = get_inner_exps(mo.groups()[0])
        return f"Add({derivative_calc(exp1)}, {derivative_calc(exp2)})"

    # Same as above but for subtraction
    if re.search("^Sub(.*)$", expr):
        mo = SUB_REGEX.search(expr)
        (exp1, exp2) = get_inner_exps(mo.groups()[0])
        return f"Sub({derivative_calc(exp1)}, {derivative_calc(exp2)})"

    # Implementing product rule
    if re.search("^Mul(.*)$", expr):
        mo = MUL_REGEX.search(expr)
        (exp1, exp2) = get_inner_exps(mo.groups()[0])
        return f"Add(Mul({exp1}, {derivative_calc(exp2)}), Mul({exp2}, {derivative_calc(exp1)}))"

    # Implementing chain rule
    if re.search("^Div(.*)$", expr):
        mo = DIV_REGEX.search(expr)
        (exp1, exp2) = get_inner_exps(mo.groups()[0])
        return f"Div(Sub(Mul({exp2}, {derivative_calc(exp1)}), Mul({exp1}, {derivative_calc(exp2)})), Mul({exp2}, {exp2}))"


def get_inner_exps(expr):
    """
    Returns the arguments within a binary DiffLang operator as a tuple.
    This function is necessarily this complicated as the arguments may be more complicated and have their own arguments.
    Thus a simple .split(", ") wouldn't work, nor a regex equation, as the expression may not be split correctly.
    """
    # Remove unnecessary whitespace
    expr = expr.strip()

    # Counter used to check if we have reached a matching bracket
    brackNum = 0

    # So we don't break the loop before we encounter the first bracket
    start = True

    # Iterate through every character in the expression
    for i in range(len(expr)):
        c = expr[i]

        # We have another layer of brackets starting
        if c == "(":
            brackNum += 1
            start = False

        # We have the previous layer of brackets closing
        elif c == ")":
            brackNum -= 1

        # All brackets have had a match
        if brackNum == 0 and not start:
            # Return the two arguments by omitting the ", " in between
            return (expr[:i + 1], expr[i + 3:])


def eval(expr, evalVal):
    """
    Returns the value of a DiffLang expression at a given value of x.
    """

    # Cover the base cases
    if re.search('^Num(.*)$', expr):
        return int(expr[4:-1].strip())

    if expr == "Exp(x)":
        return evalVal

    # These functions require you to evaluate their arguments too
    if re.search('^Neg(.*)$', expr):
        mo = NEG_REGEX.search(expr)
        return eval(mo.groups()[0], evalVal) * (-1)

    if re.search('^Sin(.*)$', expr):
        mo = SIN_REGEX.search(expr)
        return math.sin(eval(mo.groups()[0], evalVal))

    if re.search('^Cos(.*)$', expr):
        mo = COS_REGEX.search(expr)
        return math.cos(eval(mo.groups()[0], evalVal))

    if re.search('^Tan(.*)$', expr):
        mo = TAN_REGEX.search(expr)
        return math.tan(eval(mo.groups()[0], evalVal))

    if re.search('^Ln(.*)$', expr):
        mo = LN_REGEX.search(expr)
        return math.log(eval(mo.groups()[0], evalVal))

    # These expressions require you to evaluate their two arguments separately and
    # combine them suitably.
    if re.search('^Pow(.*)$', expr):
        mo = POW_REGEX.search(expr)
        (exp1, exp2) = get_inner_exps(mo.groups()[0])
        return eval(exp1, evalVal) ** eval(exp2, evalVal)

    if re.search("^Add(.*)$", expr):
        mo = ADD_REGEX.search(expr)
        (exp1, exp2) = get_inner_exps(mo.groups()[0])
        return eval(exp1, evalVal) + eval(exp2, evalVal)

    if re.search("^Sub(.*)$", expr):
        mo = SUB_REGEX.search(expr)
        (exp1, exp2) = get_inner_exps(mo.groups()[0])
        return eval(exp1, evalVal) - eval(exp2, evalVal)

    if re.search("^Mul(.*)$", expr):
        mo = MUL_REGEX.search(expr)
        (exp1, exp2) = get_inner_exps(mo.groups()[0])
        return eval(exp1, evalVal) * eval(exp2, evalVal)

    if re.search("^Div(.*)$", expr):
        mo = DIV_REGEX.search(expr)
        (exp1, exp2) = get_inner_exps(mo.groups()[0])
        return eval(exp1, evalVal) / eval(exp2, evalVal)


def simplify_exp(expr):
    """
    Returns a DiffLang expression which has removed redundancies
    """

    # Cover the bases cases as these cannot be simplified further
    if re.search("^Exp(.*)$", expr) or re.search("^Num(.*)$", expr):
        return expr

    # ---- If we have a unary operator, return it with a simplified argument

    if re.search("^Neg(.*)$", expr):
        mo = NEG_REGEX.search(expr)
        return f"Neg({simplify_exp(mo.groups()[0])})"

    if re.search("^Sin(.*)$", expr):
        mo = SIN_REGEX.search(expr)
        return f"Sin({simplify_exp(mo.groups()[0])})"

    if re.search("^Tan(.*)$", expr):
        mo = TAN_REGEX.search(expr)
        return f"Tan({simplify_exp(mo.groups()[0])})"

    if re.search("^Cos(.*)$", expr):
        mo = COS_REGEX.search(expr)
        return f"Cos({simplify_exp(mo.groups()[0])})"

    if re.search("^Ln(.*)$", expr):
        mo = LN_REGEX.search(expr)
        return f"Ln({simplify_exp(mo.groups()[0])})"

    # ====

    # We define these as variables rather than using directly in the if statement as
    # they may be used more than once
    addition = re.search("^Add(.*)$", expr)
    subtraction = re.search("^Sub(.*)$", expr)

    # If we are adding or subtracting..
    if addition or subtraction:

        # Get the two arguments
        (exp1, exp2) = get_inner_exps(expr[4:-1])

        # ---- Consider the simple cases

        # If we are adding 0 to an expression, just return that expression
        if exp1 == "Num(0)" and addition:
            return simplify_exp(exp2)

        # If we are subtracting from 0, just return a negated version of the expression
        if exp1 == "Num(0)" and subtraction:
            return f"Neg({simplify_exp(exp2)})"

        # If we are adding 0 or subtracting 0 just return that expression
        if exp2 == "Num(0)":
            return simplify_exp(exp1)

        # ----

        # If there are no simple cases, just simplify the arguments
        if addition:
            return f"Add({simplify_exp(exp1)}, {simplify_exp(exp2)})"
        if subtraction:
            return f"Sub({simplify_exp(exp1)}, {simplify_exp(exp2)})"

    # If we are multiplying...
    if re.search("^Mul(.*)$", expr):

        # Get the two arguments
        (exp1, exp2) = get_inner_exps(expr[4:-1])

        # ---- Consider the special cases

        # If we are multiplying by 0, just return 0
        if exp1 == "Num(0)" or exp2 == "Num(0)":
            return "Num(0)"

        # If one of the arguments is 1, just return the other argument.
        if exp1 == "Num(1)":
            return exp2
        if exp2 == "Num(1)":
            return exp1

        # ----

        # If there are no simple cases, just simplify the arguments
        return f"Mul({simplify_exp(exp1)}, {simplify_exp(exp2)})"

    # If we are dividing...
    if re.search("^Div(.*)$", expr):

        # Get the two arguments
        (exp1, exp2) = get_inner_exps(expr[4:-1])

        # If we are dividing by 1, just return the first argument
        if exp2 == "Num(1)":
            return exp1

        # If the second argument is 0, we could have a problem. but this would be raised as an error
        # later in the eval section so we do not worry about that here.

        # If there are no simple cases, just simplify the arguments
        return f"Div({simplify_exp(exp1)}, {simplify_exp(exp2)})"

    if re.search("^Pow(.*)$", expr):
        # Get the two arguments
        (exp1, exp2) = get_inner_exps(expr[4:-1])

        # If we are dividing by 1, just return the first argument
        if exp2 == "Num(1)":
            return exp1

    # Return the expression
    return expr


def print_exp(expr):
    """
    Returns a mathematical expression from a DiffLang expression. This is later made more readable
    by using SymPy.
    """

    # ---- Cover the base cases

    if re.search('^Num(.*)$', expr):
        return expr[4:-1]

    if expr == "Exp(x)":
        return "x"

    # ----

    # ---- For the complex cases, we do a suitable recursive call

    if re.search('^Neg(.*)$', expr):
        mo = NEG_REGEX.search(expr)
        return f"- ({print_exp(mo.groups()[0])})"

    if re.search("^Add(.*)$", expr):
        mo = ADD_REGEX.search(expr)
        (exp1, exp2) = get_inner_exps(mo.groups()[0])
        return f"({print_exp(exp1)}) + ({print_exp(exp2)})"

    if re.search("^Sub(.*)$", expr):
        mo = SUB_REGEX.search(expr)
        (exp1, exp2) = get_inner_exps(mo.groups()[0])
        return f"({print_exp(exp1)}) - ({print_exp(exp2)})"

    if re.search("^Mul(.*)$", expr):
        mo = MUL_REGEX.search(expr)
        (exp1, exp2) = get_inner_exps(mo.groups()[0])
        return f"({print_exp(exp1)}) * ({print_exp(exp2)})"

    if re.search("^Div(.*)$", expr):
        mo = DIV_REGEX.search(expr)
        (exp1, exp2) = get_inner_exps(mo.groups()[0])
        return f"({print_exp(exp1)}) / ({print_exp(exp2)})"

    if re.search('^Sin(.*)$', expr):
        mo = SIN_REGEX.search(expr)
        return f"sin({print_exp(mo.groups()[0])})"

    if re.search('^Cos(.*)$', expr):
        mo = COS_REGEX.search(expr)
        return f"cos({print_exp(mo.groups()[0])})"

    if re.search('^Tan(.*)$', expr):
        mo = TAN_REGEX.search(expr)
        return f"tan({print_exp(mo.groups()[0])})"

    if re.search('^Ln(.*)$', expr):
        mo = LN_REGEX.search(expr)
        return f"log({print_exp(mo.groups()[0])})"

    if re.search('^Pow(.*)$', expr):
        mo = POW_REGEX.search(expr)
        (exp1, exp2) = get_inner_exps(mo.groups()[0])

        # We use ** here so that SymPy can understand, this is later replaced with ^
        return f"({print_exp(exp1)}) ** ({print_exp(exp2)})"

    # ----


def conv_exp_to_eqn(expr):
    """
    Converts our DiffLang expression to an equation, making sure to replace the ** symbol with ^
    for consistency. We can also remove * signs for readability as this return value will not be
    used for anything except for output to the user.
    """
    return str(sympy.sympify(print_exp(expr))).replace("**", "^").replace("*", "")


def get_deriv_at_point(expression, evalVal):
    """
    Returns the value of the derivative at the given point
    """

    try:

        # Try to evaluate the derivative at the given point
        val = eval(simplify_exp(derivative_calc(expression)), evalVal)
        return val

    # If the code failed, it's because there may be a math error (e.g., Division by Zero)
    # rather than an error in the expression syntax as that should've been discovered
    # before this function is even called.
    except:
        return (f"We cannot calculate the derivative at the point {evalVal}.")


def get_deriv(expression):
    """
    Returns the simplified derivative of an expression in DiffLang
    """
    return simplify_exp(derivative_calc(expression))


def get_readable_deriv(expression):
    """
    Returns the simplified derivative of an expression as a mathematical expression, making sure it's readable and consistent
    """
    return str(sympy.simplify(sympy.sympify(print_exp(get_deriv(expression))))).replace("**", "^").replace("*", "")


if __name__ == "__main__":
    main()

# sin(((x) ^ (3)) - ((3) * ((x) ^ (2))))
