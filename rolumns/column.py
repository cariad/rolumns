from rolumns.source import Source


class Column:
    """
    A column to render.
    """

    def __init__(self, name: str, source: Source) -> None:
        self.name = name
        self.source = source
