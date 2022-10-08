import rolumns
import rolumns.renderers


def test() -> None:
    data = {
        "name": "Robert Pringles",
        "email": "bob@pringles.pop",
    }

    columns = rolumns.Columns()
    columns.add("Name", "name")
    columns.add("Email", "email")

    rows_renderer = rolumns.renderers.RowsRenderer(columns)

    expect_rows = [
        ["Name", "Email"],
        ["Robert Pringles", "bob@pringles.pop"],
    ]

    assert list(rows_renderer.render(data)) == expect_rows

    md_renderer = rolumns.renderers.MarkdownRenderer(columns)

    expect_md = [
        "| Name | Email |",
        "| - | - |",
        "| Robert Pringles | bob@pringles.pop |",
    ]

    assert list(md_renderer.render(data)) == expect_md
