from rolumns.groups import ByKey


def test_name() -> None:
    assert ByKey().name() == "__by_key__"
