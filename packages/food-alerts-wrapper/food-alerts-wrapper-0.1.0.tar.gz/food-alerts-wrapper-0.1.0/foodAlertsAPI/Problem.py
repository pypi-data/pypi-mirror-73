from foodAlertsAPI.Allergen import Allergen
from foodAlertsAPI.PathogenRisk import PathogenRisk


class Problem:
    """
    Attributes:

        _riskStatement (string): text describing the problem in terms of the risk to consumers
        _allergen (object[]): a list of `foodAlertsAPI.Allergen` objects
        _hazardCategory (object, optional): a `foodAlertsAPI.HazardCategory` object. Classifies the problem as into one of the hazard categories. 
                                   Support for this field is under discussion.
        _pathogenRisk (object, optional): classifies the problem as being due to actual or possible contamination with a pathogen.
        _reason (object, optional): a `foodAlertsAPI.Reason` object
    """

    def __init__(self, dict):
        for k, v in dict.items():
            setattr(self, "_" + k, v)

        # id is written @id in the API
        self._id = dict["@id"]

        if "allergen" in list(dict.keys()):
            allergen = [Allergen(a) for a in dict["allergen"]]
            self._allergen = allergen

        if "pathogenRisk" in list(dict.keys()):
            self._pathogenRisk = PathogenRisk(dict["pathogenRisk"])

    def __getattr__(self, attribute):
        return None

    def riskStatement(self):
        """
        Returns:
            riskStatement (string): text describing the problem in terms of the risk to consumers
        """

        try:
            value = self._riskStatement
        except AttributeError:
            value = None

        return value

    def allergen(self):
        """
        Returns:
            allergen (object[]): a list of `foodAlertsAPI.Allergen` objects
        """

        try:
            value = self._allergen
        except AttributeError:
            value = None

        return value

    def allergenLabels(self):
        """
        Returns:
            allergenLabels (string[], optional): list of allergens in string format
        """

        try:
            allergens = [allergenObject._label for allergenObject in self._allergen]

        except TypeError:
            allergens = None

        return allergens

    def hazardCategory(self):
        """
        Returns:
            hazardCategory (object, optional): a `foodAlertsAPI.HazardCategory` object. Classifies the problem as into one of the hazard categories. 
                                               Support for this field is under discussion.
        """

        try:
            value = self._hazardCategory
        except AttributeError:
            value = None

        return value

    def hazardCategoryLabel(self):
        """
        Returns:
            hazardCategoryLabel (string, optional): hazard category in string format
        """

        try:
            value = self._hazardCategory._label
        except AttributeError:
            value = None

        return value

    def hazardCategoryNotation(self):
        """
        Returns:
            hazardCategoryNotation (string, optional): unique identifier for hazard category in string format
        """

        try:
            value = self._hazardCategory._notation
        except AttributeError:
            value = None

        return value

    def pathogenRisk(self):
        """
        Returns:
            pathogenRisk (object, optional): classifies the problem as being due to actual or possible contamination with a pathogen.
        """

        try:
            value = self._pathogenRisk
        except AttributeError:
            value = None

        return value

    def pathogenRiskLabels(self):
        """
        Returns: 
            pathogenRiskLabels (string[], optional): pathogen risks in string format
        """
        try:
            risks = [riskObject._label for riskObject in self._pathogenRisk]

        except TypeError:
            risks = None

        return risks

    def reason(self):
        """
        Returns:
            reason (object, optional): a `foodAlertsAPI.Reason` object
        """
        try:
            value = self._reason
        except AttributeError:
            value = None

        return value
