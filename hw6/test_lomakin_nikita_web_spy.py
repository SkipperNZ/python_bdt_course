import pytest
from unittest.mock import patch

from task_lomakin_nikita_web_spy import *


URL_GITLAB_FEATURES = "https://about.gitlab.com/features/"
GITLAB_FEATURES_EXPECTED_FILEPATH = "gitlab_features_expected.html"
GITLAB_FEATURES_FILEPATH = "gitlab_features.html"


@pytest.mark.slow
def test_can_open_and_read_webpage_from_file():
    expectes_scrap = "<bound method PageScrap.__repr__ of free_products: 351, enterprise_products: 218>"
    page_scrap = make_scrap(load_page_from_file(GITLAB_FEATURES_FILEPATH))
    assert str(
        page_scrap.__repr__) == expectes_scrap, f" {page_scrap.__repr__} instead  {expectes_scrap}"


@pytest.mark.slow
def test_equal_and_str_method():
    expectes_scrap = PageScrap(351, 218)
    page_scrap = make_scrap(load_page_from_file(GITLAB_FEATURES_FILEPATH))
    assert expectes_scrap == page_scrap, "eq metod doesnt work"
    assert expectes_scrap.__str__() == "free products: 351\nenterprise products: 218", \
        f"str method work, wrong. result: {expectes_scrap.__str__()}"


@pytest.mark.slow
def test_can_setup_parser():
    parser = ArgumentParser(
        prog="web_spy",
        description="tool for monitoring web changes",
    )
    setup_parser(parser)


@pytest.mark.slow
def test_some_trash_test():
    ans = do_nothing()
    assert "https://about.gitlab.com/features/" == DEFAULT_GITLAB_ADDRES


@pytest.mark.slow
@patch('task_lomakin_nikita_web_spy.load_page_from_web')
def test_print_type_product_count(mock_load_page_from_web, capsys):
    mock_load_page_from_web.return_value = load_page_from_file(
        GITLAB_FEATURES_FILEPATH)
    # breakpoint()
    print_type_product_count("some_strange_path")
    captured = capsys.readouterr()

    assert captured.out == "free products: 351\nenterprise products: 218\n", f"Wrong! your print: {captured.out}"


@pytest.mark.integration_test
def test_web_download_and_compare_with_reference():
    reference_scrap = make_scrap(
        load_page_from_file(GITLAB_FEATURES_EXPECTED_FILEPATH))
    tested_scrap = make_scrap(load_page_from_web(URL_GITLAB_FEATURES))

    assert reference_scrap == tested_scrap, f"expected free product count is {reference_scrap.free_products}, " \
                                            f"while you calculated {tested_scrap.free_products}; " \
                                            f"expected enterprise product count is {reference_scrap.enterprise_products}, " \
                                            f"while you calculated {tested_scrap.enterprise_products}"
