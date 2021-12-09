from task_lomakin_nikita_repeater import *


def test_verbose(capsys):
    @verbose
    def foo():
        print("1")
    foo()
    captured = capsys.readouterr()
    ansver = captured.out
    assert "before function call\n1\nafter function call\n" == ansver, \
        "verbose do not work"


def test_repeater(capsys):
    @repeater(5)
    def foo():
        print("1")

    foo()
    captured = capsys.readouterr()
    ansver = captured.out
    assert "1\n1\n1\n1\n1\n" == ansver, "repeater do not work"


def test_verbose_context(capsys):
    @verbose_context()
    def foo():
        print("1")

    foo()
    captured = capsys.readouterr()
    ansver = captured.out
    assert "class: before function call\n1\nclass: after function call\n" == ansver, \
        "verbose_context do not work"
