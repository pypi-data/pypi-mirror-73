class Reason:
    """Classifies the reason for the problem as being one of a standard set of reasons. 
    This information is useful for analysis and retrieval but does not directly affect the default textual presentation of the alert. 
    Support for this field is under discussion.
    
    Attributes:

        _label (string): name for the reason
        _notation (string): unique identifier for the reason
    """

    def __init__(self):
        for k, v in dict.items():
            setattr(self, "_" + k, v)

    def __getattr__(self, attribute):
        return None

    def label(self):
        """
        Returns:
            label (string): name for the reason
        """

        try:
            value = self._label
        except AttributeError:
            value = None

        return value

    def notation(self):
        """
        Returns:
            notation (string): unique identifier for the reason
        """

        try:
            value = self._notation
        except AttributeError:
            value = None

        return value

