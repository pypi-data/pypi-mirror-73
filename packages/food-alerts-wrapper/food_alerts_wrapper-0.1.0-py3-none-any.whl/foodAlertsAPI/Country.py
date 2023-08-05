class Country:
    """
    Attributes:

        _id (string): country URL
        _label (string): name of country for which the alert applies
    """

    def __init__(self, dict):
        for k, v in dict.items():
            setattr(self, "_" + k, v)

        # id is written @id in the API
        self._id = dict["@id"]

    def __getattr__(self, attribute):
        return None

    def id(self):
        """
        Returns:
            id (string): URL for the country
        """

        try:
            value = self._id
        except AttributeError:
            value = None

        return value

    def label(self):
        """
        Returns:
            label (string, optional): name of country
        """

        try:
            value = self._label
        except AttributeError:
            value = None

        return value
