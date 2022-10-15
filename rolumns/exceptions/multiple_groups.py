class MultipleGroups(Exception):
    """
    Raised when attempting to add multiple groups to a column set.
    """

    def __init__(self) -> None:
        msg = "A column set cannot have multiple groups"
        super().__init__(msg)
