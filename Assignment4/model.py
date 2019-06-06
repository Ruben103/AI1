#!/usr/bin/python
import sys
import random

# Global variables for the KB set, the INFER set and the set of identifiers
kb = []
infer = []
identifiers = []

class Expression:
    """
    A class for expressions. Expressions can either be unary or binary. The value of the operator can be one of
    the following: CONSTANT, IDENTIFIER, NEG, AND, OR, IMPLIES or EQUIV. Expressions always have an operator.
    CONSTANT and IDENTIFIER expressions also have a value for atom. Expressions with the NEG operator store the
    expression which is negated in operand1. Binary expressions (AND, OR, IMPLIES and EQUIV) store  the left and right
    side of the expression in operand1 and operand2, respectively.
    """

    def __init__(self, operator=None, atom=None, operand1=None, operand2=None):
        self.operator = operator
        self.atom = atom
        self.operand1 = operand1
        self.operand2 = operand2

def match(str, sentence):
    """
    Checks whether the expected sequence of characters is actually in the sentence.
    If true, it returns the sentence with the expected sequence removed. If false, it throws an error.
    :param str: The character(s) to be matched
    :param sentence: The sentence to match str with
    :return: The input sentence with the matched character(s) removed
    """
    assert str == sentence[:len(str)], "Parsing failed. Expected " + str

    if (len(sentence[len(str):]) == 0):
        # This only happens when the sentence ends with a ')', which would make the function return an empty string
        return " "

    return sentence[len(str):]


def make_constant_expression(value):
    """
    Creates a constant expression (True or False)
    :param value: The truth value of the constant expression
    :return: An expression of type CONSTANT
    """
    return Expression(operator="CONSTANT", atom=value)

def make_identifier(id):
    """
    If the input identifier is 'true' or 'false', this function creates a constant expression.
    Otherwise, it creates a new identifier with name id (if it does not already exist)
    :param id: The input identifier
    :return: Either an expression of type CONSTANT with value True or False,
    or an expression of type IDENTIFIER with the value in id
    """
    if id == 'false':
        return make_constant_expression(False)
    if id == 'true':
        return make_constant_expression(True)

    if id not in identifiers:
        identifiers.append(id)

    return Expression(operator="IDENTIFIER", atom=id)

def make_negation(expression):
    """
    Makes a negation from the input expression
    :param expression: The expression to be negated
    :return: The negated expression
    """
    return Expression(operator="NEG", operand1=expression)

def make_binary_expression(operator, expression1, expression2):
    """
    Makes a binary expressions from two expressions and an operator
    :param operator: The operator of the binary expression. This can be AND, OR, IMPLIES or EQUIV
    :param expression1: The expression on the left side of the operator
    :param expression2: The expression on the right side of the operator
    :return: A binary expression containing the input expressions and operator
    """
    return Expression(operator=operator, operand1=expression1, operand2=expression2)

def print_expression(expression, end=True):
    """
    Recursively prints an expression
    :param expression: The expression to be printed
    :param end: Whether a new line should be inserted after the last print statement
    """
    if expression.operator == "CONSTANT":
        if end:
            print(expression.atom)
        else:
            print(expression.atom, end='')
        return

    if expression.operator == "IDENTIFIER":
        if end:
            print(expression.atom)
        else:
            print(expression.atom, end='')
        return

    if expression.operator == "NEG":
        print("!", end='')
        print_expression(expression.operand1, end)
        return

    print("(", end='')

    print_expression(expression.operand1, end=False)

    if (expression.operator == "AND"):
        print(" * ", end='')

    if (expression.operator == "OR"):
        print(" + ", end='')

    if (expression.operator == "IMPLIES"):
        print(" => ", end='')

    if (expression.operator == "EQUIV"):
        print(" <=> ", end='')

    print_expression(expression.operand2, end=False)

    if end:
        print(")")
    else:
        print(")", end='')

def print_expression_sets():
    """
    Prints an expression set
    """
    print("===============")

    print("KB:")
    for sen in kb:
        print_expression(sen)

    print()

    print("INFER:")
    for sen in infer:
        print_expression(sen)

    print("===============\n")

##
# Start of recursive parsing functions
# These functions recursively build a single expression. It checks whether the next part of the sentence is
# either an equivalence, implication, disjunction, conjunction, term (a negation or term within brackets)
# or atom (True, False or an identifier), in this order. If the program encounters a term within brackets, it
# recursively calls parse_equivalence on the term
##

def parse_atom(sentence):
    idx = 0
    id = ''

    assert sentence[idx].isalpha(), "Parse error, expected false, true, identifier or (expression)"

    while idx < len(sentence) and sentence[idx].isalpha():
        id += sentence[idx]
        idx += 1

    if idx != len(sentence):
        sentence = sentence[idx:]

    return make_identifier(id), sentence

def parse_term(sentence):
    if sentence[0] == "!":
        e = Expression()
        sentence = match("!", sentence)
        e, sentence = parse_term(sentence)
        return make_negation(e), sentence

    if sentence[0] == "(":
        e = Expression()
        sentence = match("(", sentence)
        e, sentence = parse_equivalence(sentence)
        sentence = match(")", sentence)
        return e, sentence

    return parse_atom(sentence)

def parse_conjunction(sentence):
    e0 = Expression()
    e0, sentence = parse_term(sentence)

    if (sentence[0] == '*'):
        e1 = Expression()
        sentence = match("*", sentence)
        e1, sentence = parse_term(sentence)

        return make_binary_expression("AND", e0, e1), sentence

    return e0, sentence

def parse_disjunction(sentence):
    e0 = Expression()
    e0, sentence = parse_conjunction(sentence)

    if (sentence[0] == '+'):
        e1 = Expression()
        sentence = match("+", sentence)
        e1, sentence = parse_conjunction(sentence)

        return make_binary_expression("OR", e0, e1), sentence

    return e0, sentence

def parse_implication(sentence):
    e0 = Expression()
    e0, sentence = parse_disjunction(sentence)

    if (sentence[0] == '='):
        e1 = Expression()
        sentence = match("=>", sentence)
        e1, sentence = parse_disjunction(sentence)

        return make_binary_expression("IMPLIES", e0, e1), sentence

    return e0, sentence

def parse_equivalence(sentence):
    e0 = Expression()
    e0, sentence = parse_implication(sentence)

    if (sentence[0] == '<'):
        e1 = Expression()
        sentence = match("<=>", sentence)
        e1, sentence = parse_implication(sentence)

        return make_binary_expression("EQUIV", e0, e1), sentence

    return e0, sentence

##
# End of set of recursive parsing functions
##

def parse_sentence(sentence):
    """
    This function recursively parses a sentence
    :param sentence: A sentence to be parsed
    :return: A parsed expression
    """
    e = Expression()
    e, sentence = parse_equivalence(sentence)

    return e

def parse_sentence_set(set, parsed_set):
    """
    Parses each sentence in the set and adds it to either kb or infer
    :param set: A set of sentences to be parsed
    :param parsed_set: The (initially) empty set of parsed sentences. This is either kb or infer (both are global)
    """
    for sentence in set:
        sentence = sentence.replace(" ", "").lower()
        parsed_set.append(parse_sentence(sentence))

def parse_input():
    """
    Reads a model from the input file, parses the KB and INFER sentence sets and stores it in kb and infer
    """
    assert len(sys.argv) > 1, "No arguments given. Please provide a model in an input file as described in the pdf"

    input_file = sys.argv[1]

    f = open(input_file, "r")
    infile = f.read()
    data = eval(infile)

    print("Complete input: ", data)
    assert 'KB' in data.keys(), "Parsing failed, expected input to contain element 'KB'"
    assert 'INFER' in data.keys(), "Parsing failed, expected input to contain element 'INFER'"

    parse_sentence_set(data['KB'], kb)
    parse_sentence_set(data['INFER'], infer)

    print("Identifiers: ", identifiers)

def evaluate_expression(e, model):
    """
    Determines the truth value of a single expression
    :param e: The expression to be evaluated
    :param model: The model containing the evaluations of the identifiers
    :return: The truth value of the expression
    """
    if e.operator == "CONSTANT":
        return e.atom

    if e.operator == "IDENTIFIER":
        return model[e.atom]

    if e.operator == "EQUIV":
        return evaluate_expression(e.operand1, model) == evaluate_expression(e.operand2, model)

    if e.operator == "IMPLIES":
        return (not evaluate_expression(e.operand1, model)) or evaluate_expression(e.operand2, model)

    if e.operator == "AND":
        return evaluate_expression(e.operand1, model) and evaluate_expression(e.operand2, model)

    if e.operator == "OR":
        return evaluate_expression(e.operand1, model) or evaluate_expression(e.operand2, model)

    if e.operator == "NEG":
        return not evaluate_expression(e.operand1, model)

    raise ValueError("Fatal error: we should never get here")

def evaluate_expression_set(expression_set, model):
    """
    Determines the truth value of an expression set
    :param expression_set: The expression set to be evaluated
    :param model: The model containing the evaluations of the identifiers
    :return: True if all expressions in the set evaluate to true, otherwise False
    """
    for expression in expression_set:
        if not evaluate_expression(expression, model):
            return False

    return True

def evaluate_random_model():
    """
    Assigns random truth values to the identifiers, evaluates the KB and INFER sets using this model
    and prints whether KB entails INFER
    """
    model = {}

    for id in identifiers:
        model[id] = random.choice([True, False])

    print("Randomly chosen model: ", model)

    kb_eval = evaluate_expression_set(kb, model)
    infer_eval = evaluate_expression_set(infer, model)

    print("     KB evaluates to: ", kb_eval)
    print("     INFER evaluates to: ", infer_eval, "\n")

    if kb_eval and not infer_eval:
        print("KB does not entail INFER\n")
    else:
        print("KB entails INFER\KeyError: 'p'n")

##
# It should not be necessary to change any code above this line!
##

def check_all_models():
    # This function should return True if KB entails INFER, otherwise it should return False
    # Check all possible configurations of the Truth table. 
    booleans = [True, False]
    iterators = [0,1]
    model = {}


    for i in iterators:
        model[identifiers[0]] = booleans[i]
        for j in iterators:
            model[identifiers[1]] = booleans[j]
            for h in iterators:
                model[identifiers[2]] = booleans[h]

                for i in model:
                    print(model[i])
                
                kb_eval = evaluate_expression_set(kb, model)
                infer_eval = evaluate_expression_set(infer, model)

                print("     KB evaluates to: ", kb_eval)
                print("     INFER evaluates to: ", infer_eval, "\n")

                if kb_eval and not infer_eval:
                    print("KB does not entail INFER\n")
                else:
                    print("KB entails INFER\KeyError: 'p'n")
    return True


def main():
    parse_input()
    print_expression_sets()
    #evaluate_random_model()
    check_all_models()

if __name__ == "__main__":
    main()