from typing import Optional

from pytest import mark

from rolumns import Columns, Source, TranslationState
from rolumns.enums import ColumnAlignment
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


@mark.parametrize(
    "value, expect",
    [
        ("", 0),
        (" ", 1),
        ("hello", 5),
        ("🔥", 2),
    ],
)
def test_length(value: str, expect: int) -> None:
    assert MarkdownRenderer.length(value) == expect


@mark.parametrize(
    "value, expect",
    [
        ("", "      "),
        (" ", "      "),
        ("hello", "hello "),
        ("helloworld", "helloworld"),
        ("🔥", "🔥    "),
    ],
)
def test_pad(value: str, expect: str) -> None:
    assert MarkdownRenderer.pad(value, 6) == expect


def test_render_string() -> None:
    (inp, exp) = load_test_case(0, expect_format="md", expect_variant="pretty")
    cs = Columns()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    t = MarkdownRenderer(cs)

    assert t.render_string(inp) == "\n".join(exp) + "\n"


def test_render_string__emoji() -> None:
    def fire(state: TranslationState) -> Optional[str]:
        return "🔥" if state.value == "orange" else None

    (inp, exp) = load_test_case(1, expect_format="md", expect_variant="emoji")
    cs = Columns()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    cs.add("?", Source("favourite_colour", translator=fire))
    t = MarkdownRenderer(cs)

    assert t.render_string(inp) == "\n".join(exp) + "\n"


def test_render_string__alignment() -> None:
    (inp, exp) = load_test_case(1, expect_format="md", expect_variant="numbers")
    cs = Columns()
    cs.add("Name", "name")
    cs.add("Favourite Colour", "favourite_colour")
    cs.add("Favourite Number", "favourite_number")
    t = MarkdownRenderer(cs)
    t.append("Name")
    t.append("Favourite Colour")
    t.append("Favourite Number", alignment=ColumnAlignment.RIGHT)

    assert t.render_string(inp) == "\n".join(exp) + "\n"
