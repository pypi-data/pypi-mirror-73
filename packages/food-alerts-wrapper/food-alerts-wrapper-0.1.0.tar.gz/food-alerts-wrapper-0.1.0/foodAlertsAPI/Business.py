class Business:
    """
    Attributes:

        _commonName (string): name by which the organisation is commonly known 
        _identifier (string, optional): unique identifier for the organisation
        _legalName (string, optional): legal (registered) name of the organisation   
    """

    def __init__(self, dict):
        for k, v in dict.items():
            setattr(self, "_" + k, v)

        # only seems to have attribute:
        #   commonName

    def __getattr__(self, attribute):
        return None

    def commonName(self):
        """
        Returns:
            commonName (string): name by which the organisation is commonly known 
        """
        try:
            value = self._commonName
        except AttributeError:
            value = None

        return value

    def identifier(self):
        """
        Returns:
            identifier (string, optional): unique identifier for the organisation
        """

        try:
            value = self._identifier
        except AttributeError:
            value = None

        return value

    def legalName(self):
        """
        Returns:
            legalName (string, optional): legal (registered) name of the organisation  
        """

        try:
            value = self._legalName
        except AttributeError:
            value = None

        return value
