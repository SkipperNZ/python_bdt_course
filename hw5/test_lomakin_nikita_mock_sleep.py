import pytest

from sleepy import *

from unittest.mock import patch



@patch("sleepy.sleep")
def test_sleep_add(mock_sleep):
    correct_ans = 10
    ans = sleep_add(3, 7)
    assert correct_ans == ans , f"sleep_aad work incorect. correct ansver is {correct_ans}, current ansver = {ans}"


@patch("sleepy.time.sleep")
def test_sleep_multiply(mock_time_sleep):
    correct_ans  = 50
    ans = sleep_multiply(5, 10)
    assert correct_ans == ans, f"sleep_aad work incorect. correct ansver is {correct_ans}, current ansver = {ans}"

