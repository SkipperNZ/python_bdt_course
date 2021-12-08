import io
import pytest

from asset import *


ASSET_DATA_EXAMPLE_STR = "property   1000    0.1"


def test_build_from_str():
    tested_asset = Asset.build_from_str(ASSET_DATA_EXAMPLE_STR)
    etalon_asset = Asset('property', 1000, 0.1)
    assert etalon_asset == tested_asset, ("can't build asset from_string")


def test_calculate_revenue():
    asset = Asset('property', 1000, 0.1)
    tested_result = asset.calculate_revenue(1)
    etalon_result = 100
    assert etalon_result == int(tested_result), \
        (f"calculate revenue work incorrect result: {tested_result} must be : 100")


def test_load_asset_from_file(tmpdir):
    dataset_fio = tmpdir.join("asset_data_example.dataset")
    dataset_fio.write(ASSET_DATA_EXAMPLE_STR)
    tested_asset = load_asset_from_file(dataset_fio)
    etalon_asset = Asset('property', 1000, 0.1)
    assert etalon_asset == tested_asset, ("cant load_asset_from_file")


def test_repr():
    asset = Asset('property', 1000, 0.1)
    result = "Asset(property, 1000, 0.1)"
    assert asset.__repr__() == result, \
        (f"__repr__ work incorrect, must be 'Asset(property, 1000, 0.1)' insteed: {asset.__repr__()}")


def test_print_asset_revenue(tmpdir, capsys, caplog):
    caplog.set_level("DEBUG")
    dataset_fio = tmpdir.join("asset_data_example.dataset")
    dataset_fio.write(ASSET_DATA_EXAMPLE_STR)
    list_of_periods = [1, 2, 3, 4, 5, 6, 7]
    print_asset_revenue(dataset_fio, list_of_periods)
    captured = capsys.readouterr()
    ansver = captured.out
    assert any(
        "too many periods were provided:" in message for message in caplog.messages)
    assert any(
        "asset Asset(property, 1000.0, 0.1) for period" in message for message in caplog.messages)
    assert "1:    100.000" in ansver, (
        "1st ansver in print_asset_revenue is wrong")
    assert "2:    210.000" in ansver, (
        "2nd ansver in print_asset_revenue is wrong")
    assert "3:    331.000" in ansver, (
        "3rd ansver in print_asset_revenue is wrong")


def test_can_setup_logging():
    setup_logging("task_lomakin_nikita_asset_log.conf.yml")


def test_can_setup_parser():
    parser = ArgumentParser(
        prog="asset",
        description="tool to forecast asset revenue",
    )
    setup_parser(parser)
