class BatchDescription:
    """
    
    Attributes:

        _bestBeforeDescription (string, optional): "best before" date range for the batch
        _bestBeforeDate (string, optional): "best before" date (or dates) for the batch
        _useByDescription (string, optional): "use by" date range for the batch
        _useByDate (string, optional): "use by" date (or dates) for the batch
        _batchCode (string, optional): batch number or code for the batch
        _lotNumber (string, optional): lot number for the batch
        _batchTextDescription (string, optional): other textual description for the batch        
    """

    def __init__(self, dict):
        for k, v in dict.items():
            setattr(self, "_" + k, v)

    def __getattr__(self, attribute):
        return None

    def bestBeforeDescription(self):
        """
        Returns:
            bestBeforeDescription (string, optional): "best before" date range for the batch
        """

        try:
            value = self._bestBeforeDescription
        except AttributeError:
            value = None

        return value

    def bestBeforeDate(self):
        """
        Returns:
            bestBeforeDate (string, optional): "best before" date (or dates) for the batch 
        """

        try:
            value = self._bestBeforeDate
        except AttributeError:
            value = None

        return value

    def useByDescription(self):
        """
        Returns:
            useByDescription (string, optional): "use by" date range for the batch
        """

        try:
            value = self._useByDescription
        except AttributeError:
            value = None

        return value

    def useByDate(self):
        """
        Returns:
            useByDate (string, optional): "use by" date (or dates) for the batch
        """

        try:
            value = self._useByDate
        except AttributeError:
            value = None

        return value

    def batchCode(self):
        """
        Returns:
            batchCode (string, optional): batch number or code for the batch
        """

        try:
            value = self._batchCode
        except AttributeError:
            value = None

        return value

    def lotNumber(self):
        """
        Returns:
            lotNumber (string, optional): lot number for the batch
        """

        try:
            value = self._lotNumber
        except AttributeError:
            value = None

        return value

    def batchTextDescription(self):
        """
        Returns:
            batchTextDescription (string, optional): other textual description for the batch
        """

        try:
            value = self._batchTextDescription
        except AttributeError:
            value = None

        return value
