class RelatedMedia:
    """
    Attributes:

        _id (string): URL for the related media
        _title (string, optional): title for the related media
    """

    def __init__(self, dict):
        for k, v in dict.items():
            setattr(self, "_" + k, v)

        # id is written @id in the API
        try:
            self._id = dict["@id"]
        except KeyError:
            pass

    def __getattr__(self, attribute):
        return None

    def id(self):
        """
        Returns:
            id (string): URL for the related media
        """

        try:
            value = self._id
        except AttributeError:
            value = None

        return value

    def title(self):
        """
        Returns:
            title (string, optional): title for the related media
        """

        try:
            value = self._title
        except AttributeError:
            value = None

        return value
