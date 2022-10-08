class MultipleRepeaters(Exception):
    """
    Raised when attempting to add multiple repeaters to a column set.
    """

    def __init__(self) -> None:
        msg = "A column set cannot have multiple repeaters as direct children"
        super().__init__(msg)
