#!/usr/bin/python

import argparse
from collections import namedtuple
import operator


Number = namedtuple('Number', ['value'])
Operator = namedtuple('Operator', ['value'])
Expression = namedtuple('Expression', ['values'])


class Parser(object):

    def __init__(self, input):
        self._input = input
        self._index = 0


    def parse(self):
        return self._parseExpression()


    def _skip_blanks(self):
        while not self._done() and self._input[self._index] == ' ':
            self._index += 1


    def _peek(self):
        return self._input[self._index]


    def _pop(self):
        value = self._peek()
        self._index += 1
        return value


    def _done(self):
        return self._index >= len(self._input)


    def _raise(self, message):
        raise Exception('%s (at %s)' % (message, self._index))


    def _parseNumber(self):
        value = ''
        while not self._done():
            char = self._peek()
            if char.isdigit():
                value += char
                self._pop()
            else:
                break
        return Number(int(value))


    def _parseOperand(self):
        self._skip_blanks()
        char = self._peek()
        if char == '(':
            self._pop()
            value = self._parseExpression()
            if self._pop() != ')':
                self._raise('Missing closing parenthesis')
            return value
        elif char.isdigit():
            return self._parseNumber()
        else:
            self._raise('Unrecognized operand character "%s"', char)


    def _parseOperator(self):
        char = self._pop()
        if char == '*':
            return Operator(operator.mul)
        elif char == '+':
            return Operator(operator.add)
        self._raise('Unrecognized operator "%s"' % char)


    def _parseExpression(self):
        values = []
        self._skip_blanks()
        values.append(self._parseOperand())
        self._skip_blanks()

        while not self._done():
            if self._peek() == ')':
                break
            values.append(self._parseOperator())
            self._skip_blanks()
            values.append(self._parseOperand())
            self._skip_blanks()

        return Expression(values)


def compute_serial(line):
    def evaluate_operand(operand):
        if isinstance(operand, Number):
            return operand.value
        # The operand is an expression.
        result = 0
        operation = operator.add
        for v in operand.values:
            if isinstance(v, Operator):
                operation = v.value
            else:
                result = operation(result, evaluate_operand(v))
        return result
    return evaluate_operand(Parser(line).parse())


def compute_precedence(line):
    def compute_addition(values):
        result = evaluate_operand(values[0])
        index = 1
        while index < len(values) - 1 and values[index].value == operator.add:
            result += evaluate_operand(values[index + 1])
            index += 2
        return result, index

    def evaluate_operand(operand):
        if isinstance(operand, Number):
            return operand.value
        # The operand is an expression.
        result = 1
        index = 0
        while index < len(operand.values):
            current = operand.values[index]
            if isinstance(current, Operator):
                # This can only be a multiplication.
                index += 1
                continue
            addition, delta = compute_addition(operand.values[index:])
            result *= addition
            index += delta
        return result

    return evaluate_operand(Parser(line).parse())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--next', action='store_true')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    if args.next:
        method = compute_precedence
    else:
        method = compute_serial
    print(sum(method(l) for l in lines))


if __name__ == "__main__":
    main()
