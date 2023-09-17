# Simple Derivative Calculator
#### Video Demo:  https://youtu.be/rEkSFY7cLnM
#### Description:
This project aims to take in a mathematical equation as user input and output its derivative.

The project involved three key aspects:
- Parsing the user input to convert it into a representation that our derivative calculator can understand - "DiffLang"
- Implementing the derivative calculator which would take the DiffLang above as input and output the derivative
  using DiffLang too
- Converting the output of the derivative calculator from DiffLang to a generic mathematical equation that the user can
  understand

##### Parsing User Input - DiffLang
We first start by discussing parsing the user input. As such, we must first discuss how DiffLang represents the mathematical equations.

###### DiffLang operators
There are two type of mathematical operators considered in this project - unary and binary. Unary operators take one operand whereas binary
operators take two. Consider unary operators first:

- Neg(a) - Negative of another DiffLang (DL) literal 'a'
- Sin(a) - Sin of a DL literal
- Cos(a) - Cos of a DL literal
- Tan(a) - Tan of a DL literal
- Ln(a) - Ln of a DL literal

Now consider binary operators:

- Add(a, b) - represents addition of two DL literals 'a' and 'b'
- Mul(a, b) - represents multiplication of two DL literals 'a' and 'b'
- Div(a,b) - represents division of two DL literals 'a' and 'b'
- Sub(a, b) - represents subtraction of two DL literals 'a' and 'b'
- Pow(a, Num(n)) - represents exponentiation of a DL literal 'a' to a power. This implementation only allows numerical powers (i.e. such that we can use power rule), see below.

Notice how these literals can be recursively defined in terms of other DL literals. This calls for base cases. We have two base cases:

- Num(n) - A literal number, where n is any number (we restrict to integers in this project)
- Exp(x) - A variable 'x' (we restrict to only using a single variable which must be 'x')

###### parse_user_input()

Now when we take user input, we must parse it into DiffLang. To do this we have parse_user_input(). This function works recursively - as is required to build a recursive data
structure. As such, it needs base cases. These cases are:

- A literal number - just return Num(n) with n as the number
- The variable 'x' - Just return Exp(x)
- The variable with a coefficient - mathematical notation allows Cx where C is some constant, thus we use this as a base case and return Mul(Num(C), Exp(x))
- The variable with a coefficient and exponent - in the case of Cx^E with constants C and E, return Mul(Num(C), Pow(Exp(x), Num(E))), this case is needed as before I hadn't accounted
  for it and ended up parsing Cx^E as (Cx)^E causing errors

  Then we consider the unary operators - i.e. the trigonometric functions, ln and neg. For these, we just write their respective DiffLang operator and recursively call parse_user_input()
  on their argument. Ohterwise, we parse through by counting the number of brackets in the user input and thus deducing the primary operator in the equation, i.e. (+, -, * etc). We then
  find the arguments for this operator and recursively build our DL representation using this function. We also have helper functions such as get_left_exp() and get_right_exp() which again
  count brackets to deduce the operands for an operator. Their implementations are detailed through comments in the code.


##### The Derivative Calculator

The derivative_calc() function takes the DL expression and returns a DL expression representing the derivative of the input. This function essentially pattern matches on the input and uses
basic differentiation rules. We start by the base cases - DL literals:

- Num(n) -> for any n, this is a constant so, it differentiates to Num(0)
- Exp(x) -> this differentiates to Num(1)

We then considered unary operators and will give a brief overview of their derivatives (Note a' means derivative of a DL literal a which is to be computed recursively):
- -a -> -a'
- sin(a) -> a'cos(a)
- cos(a) -> -a'sin(a)
- tan(a) -> a' / ((cos(a))^2)
- ln(a) -> a' / a

For binary operators:
- a + b -> a' + b'
- a - b -> a' - b'
- a * b -> Product Rule, ab' + a'b
- a / b -> Quotient Rule, (ba' - ab') / (b^2)
- a ^ n -> n (a ^ (n-1)), special case 0 then return 0, special case 1 then return a'

With these simple rules, we have built our derivative calculator. However, the derivative calculator may introduce some redundancies in our representation, i.e. multiplying or dividing by
1 or adding/ subtracting 0. As such, we have a simplify_exp() function to eliminate these redundancies.

###### Evaluating at a point

We also let the user evaluate the derivative at a certain point. This can be done recursively too by pattern matching the input. The eval() function takes the derivative in DL as
one argument and the value at which to evaluate (evalVal) as another. We outline part of the process below:

- Num(n) - return n
- Exp(x) - return evalVal
- Neg(a) - return eval(a) * -1
- Add(a, b) - returnb eval(a) + eval(b)

The rest of the process is pretty self-explanatory.

##### Converting to readable format

We now need a function to convert our DL expression to a format that can be understood by the user. To do this we define a function get_readable_deriv(). This calls on helper functions print_exp(), get_deriv() and more importantly uses the library sympy. Although I have written simplify_exp(), this doesn't quite put the derivative into a representation that is most
readable, as such I use sympy's simplify() function to aid with that. We discuss the helper functions.

###### get_deriv()

This simply calculates the derivative of the DL expression and calls simplify_exp() on it.

###### print_exp()

As done multiple times before, we pattern match on our DL expression to generate the mathematical expression. We outline some of the cases below:

- Num(n) - return n as a string
- Exp(x) - return x
- Add(a, b) - return print_exp(a) + print_exp(b) as a string

The rest of the cases are self-explanatory.

##### Thoughts and Improvements

- This derivative calculator utilises sympy's simplify() function which is something I wish to get rid of, I wish to implement a version of this myself in the future.
- The implementation is not perfect, it does not account for abnormal inputs and all possible forms of mathematical notation, i.e. there are still some errors when brackets are
  used abnormally
- I iwsh to test this more thoroughly ni the future
- I could ptentially add more mathematical functions in the future such as the hyperbolic functions
- I could add the exponential function, e^x, and similarly add e and more important constants
- Perhaps extend the program with an integral calculator?