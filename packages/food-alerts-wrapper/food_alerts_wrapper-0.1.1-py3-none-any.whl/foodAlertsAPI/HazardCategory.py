class HazardCategory:
    """Classifies the problem as into one of the hazard categories. 
    This information is useful for analysis and retrieval but does not directly affect the default textual presentation of the alert.
    Support for this field is under discussion.


    Attributes:

        _label (string): name for the hazard category
        _notation (string): unique identifier for the hazard category
    """

    def __init__(self):
        for k, v in dict.items():
            setattr(self, "_" + k, v)

    def __getattr__(self, attribute):
        return None


def label(self):
    """
    Returns:
        label (string): name for the hazard category
    """

    try:
        value = self._label
    except AttributeError:
        value = None

    return value


def notation(self):
    """
    Returns:
        notation (string): unique identifier for the hazard category
    """

    try:
        value = self._notation
    except AttributeError:
        value = None

    return value
