import rolumns
import rolumns.renderers


def test() -> None:
    data = {
        "name": "Robert Pringles",
        "email": "bob@pringles.lol",
    }

    columns = rolumns.Columns()
    columns.add("Name", "name")
    columns.add("Email", "email")

    rows_renderer = rolumns.renderers.RowsRenderer(columns)

    expect_rows = [
        ["Name", "Email"],
        ["Robert Pringles", "bob@pringles.lol"],
    ]

    assert list(rows_renderer.render(data)) == expect_rows

    md_renderer = rolumns.renderers.MarkdownRenderer(columns)

    expect_md = [
        "| Name | Email |",
        "| - | - |",
        "| Robert Pringles | bob@pringles.lol |",
    ]

    assert list(md_renderer.render(data)) == expect_md
