from ..lis import tokenize, parse, eval


def test_tokenize():
    assert tokenize("(begin (define r 10) (* pi (* r r))") == [
            "(", "begin", "(", "define", "r", "10", ")", "(", "*", "pi",
            "(", "*", "r", "r", ")", ")"]


def test_parse():
    assert parse("(begin (define r 10) (* pi (* r r)))") == [
        "begin", ["define", "r", 10], ["*", "pi", ["*", "r", "r"]]
    ]


def test_eval():
    assert eval(parse("(begin (define r 10) (* pi (* r r)))")) > 314
    assert eval(parse("(begin (define r 10) (* pi (* r r)))")) < 315
