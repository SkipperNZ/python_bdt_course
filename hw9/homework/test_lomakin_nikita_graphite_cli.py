from task_lomakin_nikita_graphite_cli import *



def test_can_setup_parser():
    parser = ArgumentParser(
        prog="graphite_cli",
        description="tool to convert log file",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    setup_parser(parser)


def test_parser_can_make_correct_response(capsys):
    configirate_response(DEFAULT_DATASET_PATH, DEFAULT_HOST, DEFAULT_PORT)
    captured = capsys.readouterr()
    assert DEFAULT_HOST, DEFAULT_PORT in captured.out

