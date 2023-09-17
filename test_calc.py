from calc import main, parse_user_input, get_left_exp, get_right_exp, derivative_calc, get_inner_exps, eval, simplify_exp, print_exp, get_deriv, get_readable_deriv, get_deriv_at_point, conv_exp_to_eqn

def test_get_left_exp():
    assert get_left_exp("(((x) ^ (3)) + ((32) * (x))) - (((x) ^ (3)) + ((x) ^ (4)))") == "((x) ^ (3)) + ((x) ^ (4))"
    assert get_left_exp("((3) * (x) ^ 2)") == "(3) * (x) ^ 2"
    assert get_left_exp("((((x) + 4) ^ (3)) / ((x) ^ (2))) - ((x) ^ 2)") == "(x) ^ 2"
    assert get_left_exp("(x+4)") == "x+4"

def test_get_right_exp():
    assert get_right_exp("(((x) ^ (3)) + ((32) * (x))) - (((x) ^ (3)) + ((x) ^ (4)))") == ("((x) ^ (3)) + ((32) * (x))", "- (((x) ^ (3)) + ((x) ^ (4)))")
    assert get_right_exp("((3) * (x) ^ 2)") == ("(3) * (x) ^ 2", "")
    assert get_right_exp("((((x) + 4) ^ (3)) / ((x) ^ (2))) - ((x) ^ 2)") == ("(((x) + 4) ^ (3)) / ((x) ^ (2))", "- ((x) ^ 2)")
    assert get_right_exp("x^2 + 4*x") == ("x^2", "+ 4*x")

def test_print_exp():
    assert print_exp("Num(5)") == "5"
    assert print_exp("Neg(Num(5))") == "- (5)"
    assert print_exp("Exp(x)") == "x"
    assert print_exp("Add(Exp(x), Num(4))") == "(x) + (4)"
    assert print_exp("Mul(Num(4), Add(Num(4), Exp(x)))") == "(4) * ((4) + (x))"
    assert print_exp("Div(Num(4), Exp(x))") == "(4) / (x)"

def test_application():
    assert get_readable_deriv(parse_user_input("x^2 + 4x")) == "2x + 4"
    assert get_readable_deriv(parse_user_input("sin(3x^2)")) == "6xcos(3x^2)"
    assert get_readable_deriv(parse_user_input("ln(3x^2)")) == "2/x"
    assert get_readable_deriv(parse_user_input("cos(9x^3)")) == "-27x^2sin(9x^3)"