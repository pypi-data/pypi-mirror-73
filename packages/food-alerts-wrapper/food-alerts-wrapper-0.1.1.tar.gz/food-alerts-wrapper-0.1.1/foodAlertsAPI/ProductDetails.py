from foodAlertsAPI.BatchDescription import BatchDescription
from foodAlertsAPI.Allergen import Allergen


class ProductDetails:
    """
    Attributes:

        _productName (string): name of the affected product
        _productCode (string, optional): identifying code for the affected product
        _packSizeDescription (string, optional): description of the package size affected - may be weight, volume or other description
        _allergen (string[], optional): list of urls to the allergens present in the product
        _batchDescription (object[]): an array of `foodAlertsAPI.BatchDescription` objects
        _productCategory (object, optional): a `foodAlertsAPI.ProductCategory` object. Identifies the category of the affected product. 
                                  This information is used to support search and analysis and does not need to be separately included in the alert presentation.
        
    """

    def __init__(self, dict):
        for k, v in dict.items():
            setattr(self, "_" + k, v)

        # id is written @id in the API
        self._id = dict["@id"]

        if "batchDescription" in list(dict.keys()):
            batchDescriptions = [BatchDescription(b) for b in dict["batchDescription"]]
            self._batchDescription = batchDescriptions

    def __getattr__(self, attribute):
        return None

    def productName(self):
        """
        Returns:
            productName (string): name of the affected product
        """

        try:
            value = self._productName
        except AttributeError:
            value = None

        return value

    def productCode(self):
        """
        Returns:
            productCode (string, optional): identifying code for the affected product
        """

        try:
            value = self._productCode
        except AttributeError:
            value = None

        return value

    def packSizeDescription(self):
        """
        Returns:
            packSizeDescription (string, optional): description of the package size affected - may be weight, volume or other description
        """

        try:
            value = self._packSizeDescription
        except AttributeError:
            value = None

        return value

    def allergen(self):
        """
        Returns:
            allergen (string[]): list of urls to the allergens present in the product
        """

        try:
            value = self._allergen
        except AttributeError:
            value = None

        return value

    def batchDescription(self):
        """
        Returns:
            batchDescription (object[]): an array of `foodAlertsAPI.BatchDescription` objects
        """

        try:
            value = self._batchDescription
        except AttributeError:
            value = None

        return value

    def productCategory(self):
        """
        Returns:
            productCategory (object, optional): a `foodAlertsAPI.ProductCategory` object. Identifies the category of the affected product. 
                                                This information is used to support search and analysis and does not need to be separately included in the alert presentation.
        """

        try:
            value = self._productCategory
        except AttributeError:
            value = None

        return value
