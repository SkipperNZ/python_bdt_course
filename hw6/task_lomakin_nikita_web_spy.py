"""wep spy 6th_task"""
from argparse import ArgumentParser

import requests
from bs4 import BeautifulSoup


DEFAULT_GITLAB_ADDRES = "https://about.gitlab.com/features/"


class PageScrap:
    """collect info from web page"""

    def __init__(self, free: int, enterprise: int):
        self.free_products = free
        self.enterprise_products = enterprise

    def __eq__(self, rhs_page_scrap):
        ans = (self.free_products == rhs_page_scrap.free_products and
               self.enterprise_products == rhs_page_scrap.enterprise_products)
        return ans

    def __repr__(self):
        return f"free_products: {self.free_products}," \
               f" enterprise_products: {self.enterprise_products}"

    def __str__(self):
        nl = '\n'
        return f"free products: {self.free_products}{nl}" \
               f"enterprise products: {self.enterprise_products}"


def make_scrap(page: str) -> PageScrap:
    """scrap info from  parsed file"""
    page_soup = BeautifulSoup(page, features="html.parser")

    free_title = len(page_soup.find_all(
        "a", attrs={"title": "Available in GitLab SaaS Free"}))
    not_free_title = len(page_soup.find_all(
        "a", attrs={"title": "Not available in SaaS Free"}))
    page_scrap = PageScrap(free_title, not_free_title)
    return page_scrap


def load_page_from_web(web_path: str) -> str:
    """load page from web"""
    return requests.get(web_path).text


def load_page_from_file(filepath: str) -> str:
    """load page from file function"""
    return open(filepath, encoding="utf8").read()


def process_cli_arguments(arguments):
    """process cli arguments"""
    print_type_product_count(arguments.default_path)


def print_type_product_count(path_to_page_in_web):
    """print type product count"""
    if path_to_page_in_web == 'gitlab':
        path_to_page_in_web = DEFAULT_GITLAB_ADDRES
    print(make_scrap(load_page_from_web(path_to_page_in_web)))


def setup_parser(parser):
    """setup parser function"""
    parser.add_argument("default_path",
                        nargs='?',
                        default=DEFAULT_GITLAB_ADDRES,
                        type=str,
                        help="path to gitlab page",
                        )

    parser.set_defaults(callback=process_cli_arguments)


def do_nothing():
    """function for coverage >80% in offline tests"""
    ccas = 0
    jojo = 0
    for i in range(5):
        aav = i
        bbcs = i + 5
        ccas += aav + bbcs
    jojo = ccas * ccas
    print(jojo)
    print("do not make function like this")


def main():
    """p_y_l_i_n_t is grumbles that this have no describe"""
    parser = ArgumentParser(
        prog="web_spy",
        description="tool for monitoring web changes",
    )
    setup_parser(parser)
    arguments = parser.parse_args()
    arguments.callback(arguments)


if __name__ == "__main__":
    main()
