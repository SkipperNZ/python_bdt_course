n = -1
def get_curse() -> float:
    nonlocal n
    n = n + 1
    return (76.32 + 0.1 * n)

mock_get_usd_course.side_effect = get_curse