from task_lomakin_nikita_indenter import Indenter


def test_default_indent(capsys):
    with Indenter() as indent:
        indent.print("hi")
        with indent:
            indent.print("hello")
            with indent:
                indent.print("jojo")
        indent.print("referense")

    captured = capsys.readouterr()
    ansver = captured.out
    assert "hi\n    hello\n        jojo\nreferense\n" == ansver, \
        f"test_default_indent do not work, {ansver} "


def test_str_only_indent(capsys):
    with Indenter(indent_str="--") as indent:
        indent.print("hi")
        with indent:
            indent.print("hello")
            with indent:
                indent.print("jojo")
        indent.print("referense")
    captured = capsys.readouterr()
    ansver = captured.out
    assert "hi\n--hello\n----jojo\nreferense\n" == ansver, \
        f"test_str_only_indent do not work, {ansver} "


def test_str_and_level_indent(capsys):
    with Indenter(indent_str="--", indent_level=1) as indent:
        indent.print("hi")
        with indent:
            indent.print("hello")
            with indent:
                indent.print("jojo")
        indent.print("referense")
    captured = capsys.readouterr()
    ansver = captured.out
    assert "--hi\n----hello\n------jojo\n--referense\n" == ansver, \
        "test_str_and_level_indent do not work"
