class Status:
    """
    Attributes:

        _id (string): URL for the status
        _label (string): name of the status of the Alert, normally this will be 'Published' but in rare cases may be changed to 'Withdrawn'
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
            id (string): URL for the status
        """

        try:
            value = self._id
        except AttributeError:
            value = None

        return value

    def label(self):
        """
        Returns:
            label (string, optional): name of the status of the Alert, normally this will be 'Published' but in rare cases may be changed to 'Withdrawn'
        """

        try:
            value = self._label
        except AttributeError:
            value = None

        return value
