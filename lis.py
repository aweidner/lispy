import math
import operator as op

# Type definitions
Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list
Exp = (Atom, List)
Env = dict


def tokenize(chars: str) -> list:
    """ Convert a string of characters into a list of tokens """
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(program: str) -> Exp:
    return read_from_tokens(tokenize(program))


def read_from_tokens(tokens: list) -> Exp:
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')

    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        # Pop off closing ')'
        tokens.pop(0)
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)


def atom(token: str) -> Atom:
    "Numbers become numbers; ever other token is a symbol."

    try:
        return int(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        return Symbol(token)


def standard_env() -> Env:
    env = Env()
    env.update(vars(math))
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs': abs,
        'append': op.add,
        'apply': lambda proc, args: proc(*args),
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_,
        'expt': pow,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: List(x),
        'list?': lambda x: isinstance(x, List),
        'map': map,
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'print': print,
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(Symbol)
    })
    return env


global_env = standard_env()


def eval(x: Exp, env=global_env) -> Exp:
    """ Evaluate an expression in an environment """
    if isinstance(x, Symbol):
        return env[x]
    elif isinstance(x, Number):
        return x
    elif x[0] == 'if':
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':
        (_, symbol, exp) = x
        env[symbol] = eval(exp, env)
    else:
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)


def schemestr(exp):
    """ Convert a python object back into a scheme readable string """
    return ('({})'.format(' '.join(map(schemestr, exp)))
            if isinstance(exp, List)
            else str(exp))


def repl(prompt=">"):
    """ A repl """
    while True:
        val = eval(parse(input(prompt)))
        if val is not None:
            print(schemestr(val))


if __name__ == "__main__":
    repl()
