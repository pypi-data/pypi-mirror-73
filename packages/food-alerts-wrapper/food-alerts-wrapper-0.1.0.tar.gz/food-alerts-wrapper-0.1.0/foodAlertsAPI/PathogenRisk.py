class PathogenRisk:
    """Classifies the problem as being due to actual or possible contamination with a pathogen.
    
    Attributes:

        _label (string): name for the pathogen risk
        _notation (string): unique identifier for the pathogen risk
        _pathogen (string): URL to page of the pathogen involved
        _riskStatement (string): text describing the risk from this pathogen, or possible pathogen
    """

    def __init__(self, dict):
        for k, v in dict.items():
            setattr(self, "_" + k, v)

        # id is written @id in the APi
        self._id = dict["@id"]

        if isinstance(dict["label"], list):
            self._label = dict["label"][0]

        if "riskStatement" in list(dict.keys()):
            if isinstance(dict["riskStatement"], list):
                self._riskStatement = dict["riskStatement"][0]

    def __getattr__(self, attribute):
        return None

    def label(self):
        """
        Returns:
            label (string): name for the pathogen risk
        """

        try:
            value = self._label
        except AttributeError:
            value = None

        return value

    def notation(self):
        """
        Returns:
            notation (string): unique identifier for the pathogen risk
        """

        try:
            value = self._notation
        except AttributeError:
            value = None

        return value

    def pathogen(self):
        """
        Returns:
            pathogen (object): indicates the actual pathogen involved. The PathogenRisk may represent actual or possible contamination with this pathogen
        """

        try:
            value = self._pathogen["@id"]
        except AttributeError:
            value = None

        return value

    def riskStatement(self):
        """
        Returns:
            riskStatement (string): text describing the risk from this pathogen, or possible pathogen
        """

        try:
            value = self._riskStatement
        except AttributeError:
            value = None

        return value
