"""CLI ti parse and print logfile"""
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType, ArgumentTypeError
from typing import Dict, List
from datetime import datetime
import time

DEFAULT_DATASET_PATH = "wiki_search_app.log"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = "2003"


def setup_parser(parser):
    """setup parser function"""

    parser.add_argument(
        "--process",
        default=DEFAULT_DATASET_PATH,
        required=True,
        help="path to log file default is %(default)s",
    )

    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        required=True,
        help="host default is %(default)s",
    )

    parser.add_argument(
        "--port",
        default=DEFAULT_PORT,
        required=True,
        help="port default is %(default)s",
    )

    parser.set_defaults(callback=process_cli_arguments)


def process_cli_arguments(arguments):
    """process cli arguments"""
    configirate_response(arguments.process, arguments.host, arguments.port)


def configirate_response(process, host, port):
    """callback for print response"""

    logs_aggregator = {}

    with open(process, "r", encoding='utf-8') as fin:
        data = fin.readlines()

    for line in data:
        '''
        добавляем в словарь по запросу распаршеные данныне
        и когда по ключу-запросу будет 3 лога выводим их в ответ и удаляем из словаря
        '''
        query, parsed_data = parse_one_log_line(line)
        logs_aggregator.setdefault(query, []).append(parsed_data)
        if (len(logs_aggregator[query]) == 3):
            ansver_data = make_ansver_data(logs_aggregator[query])
            print_response(ansver_data, host, port)
            del logs_aggregator[query]


def print_response(ansver_data: tuple, host: str, port: int):
    """print response in terminal"""
    print(
        f'echo "wiki_search.article_found {ansver_data[0]} {ansver_data[2]}" | nc -N {host} {port}')
    print(
        f'echo "wiki_search.complexity {ansver_data[1]:.3f} {ansver_data[2]}" | nc -N {host} {port}')


def make_ansver_data(parsed_logs: List) -> tuple:
    """make tupple with info to print response"""
    for log in parsed_logs:
        if log[0] == 'start':
            time_start = log[1]
        elif log[0] == 'finish':
            time_finish = log[1]
        elif log[0] == 'found':
            article_found = log[2]
    delta_time = (time_finish - time_start).total_seconds()
    finish_unixtime = int(time.mktime(time_finish.timetuple()))

    return (article_found, delta_time, finish_unixtime)


def parse_one_log_line(log_line: str) -> Dict:
    """parse one log string from row string"""
    list_log_line = log_line.split()
    parsed_data = []

    #type (start/found/finish)
    parsed_data.append(list_log_line[3])

    # date parse
    date_time_obj = datetime.strptime(list_log_line[0], "%Y%m%d_%H%M%S.%f")
    parsed_data.append(date_time_obj)

    # query parse it's last elements in string
    if(list_log_line[2] == 'INFO'):
        query = "".join(list_log_line[8:])
        parsed_data.append(list_log_line[4])  # count
    else:
        query = "".join(list_log_line[6:])

    return query, parsed_data


def main():
    """p_y_l_i_n_t is grumbles that this have no describe"""

    parser = ArgumentParser(
        prog="graphite_cli",
        description="tool to convert log file",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    setup_parser(parser)
    arguments = parser.parse_args()
    arguments.callback(arguments)


if __name__ == "__main__":
    main()
