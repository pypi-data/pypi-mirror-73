class Allergen:
    """ Array of allergens drawn from the controlled list of allergens. 
    For an Allergen Alert there will also be at least one allergen present on the problem statement.

    Attributes:

        _label (string): name for the allergen
        _notation (string): a unique identifier for the allergen
        _riskStatement (string): text describing the risk from the allergen
    """

    def __init__(self, dict):
        for k, v in dict.items():
            setattr(self, "_" + k, v)

        # id is written @id in the API
        self._id = dict["@id"]

    def __getattr__(self, attribute):
        return None

    def label(self):
        """
        Returns:
            label (string): the allergen name
        """

        try:
            value = self._label
        except AttributeError:
            value = None

        return value

    def notation(self):
        """
        Returns:
            notation (string, optional): unique identifier for the allergen
        """

        try:
            value = self._notation
        except AttributeError:
            value = None

        return value

    def riskStatement(self):
        """
        Returns:
            riskStatement (string): text describing the risk from the allergen
        """

        try:
            value = self._riskStatement
        except AttributeError:
            value = None

        return value
