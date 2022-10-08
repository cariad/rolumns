from rolumns import Columns
from rolumns.renderers import MarkdownRenderer
from tests.data import load_test_case


def test_append() -> None:
    (inp, exp) = load_test_case(0, expect_format="md")
    cs = Columns()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    t = MarkdownRenderer(cs)
    t.append("Name")
    t.append("Favourite Colour")
    assert list(t.render(inp)) == exp
