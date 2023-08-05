from foodAlertsAPI.Problem import Problem
from foodAlertsAPI.ProductDetails import ProductDetails
from foodAlertsAPI.Status import Status
from foodAlertsAPI.BatchDescription import BatchDescription
from foodAlertsAPI.Country import Country
from foodAlertsAPI.Business import Business
from foodAlertsAPI.RelatedMedia import RelatedMedia
from foodAlertsAPI.PathogenRisk import PathogenRisk
from collections import defaultdict
from typing import List


class Alert:
    """Alert is the base class representing the details of an FSA Food Alert. Optional attributes have value `None`
    if unspecified. This applies to all classes.

    Attributes:
        
        _id (string): url to alert in the FSA page, same as the alertURL attribute
        _title (string):   
        _shortTitle (string): "None" if the API does not provide this value
        _description (string):    
        _created (string): represents date in ISO format
        _modified (string): represents datetime in ISO format
        _notation (string): unique identifier for alert used in the `foodAlertsAPI.foodAlertsAPI` getAlert() function
        _country (object):  a `foodAlertsAPI.Country` object. None if unspecified by the API indicating that the alert may apply to any country in the UK
        _status (string): the alert status, usually "Published", but in rare cases may be "Withdrawn"
        _type (string[]): an array of strings (URLs, one corresponding to the Alert object in the API, 
                         and another to the type of alert corresponding to the Alert object (one of "AA" - allergen, "FAFA" - food action, or "PRIN" - product recall))
        _actionTaken (string, optional): description of the action taken, or in the case of FAFAs actions to be taken by enforcement authority
        _consumerAdvice (string, optional): text giving the advice to consumers
        _SMSText (string, optional): short description to be used in SMS notifications
        _twitterText (string, optional): short description to be used in Twitter notifications
        _alertURL (dict, optional): URL for the alert on the FSA web site
        _shortURL (dict, optional):     
        _relatedMedia (object[], optional): array of `foodAlertsAPI.RelatedMedia` objects
        _problem (object[], optional): array of `foodAlertsAPI.Problem` objects
        _productDetails (object[], optional): array of `foodAlertsAPI.ProductDetails` objects
        _reportingBusiness (object[], optional): a `foodAlertsAPI.Business` object
        _otherBusiness (object[], optional): an array of `foodAlertsAPI.Business` objects
        _previousAlert (string, optional): URL to previous alert. This exists if the Alert is an update to a previous one
    """

    def __init__(self, dict):
        for k, v in dict.items():
            setattr(self, "_" + k, v)

        keys = list(dict.keys())

        # id is written @id in the API
        self._id = dict["@id"]

        # assigning different values to some attributes
        if "problem" in keys:
            self._problem = [Problem(p) for p in dict["problem"]]

        if "productDetails" in keys:
            self._productDetails = [ProductDetails(d) for d in dict["productDetails"]]

        if "status" in keys:
            self._status = Status(dict["status"])

        if "country" in keys:
            self._country = [Country(c) for c in dict["country"]]

        if "reportingBusiness" in keys:
            self._reportingBusiness = Business(dict["reportingBusiness"])

        if "otherBusiness" in keys:
            try:
                self._otherBusiness = [Business(dict["otherBusiness"])]
            except AttributeError:
                self._otherBusiness = [Business(b) for b in dict["otherBusiness"]]

        if "relatedMedia" in keys:
            try:
                self._relatedMedia = [RelatedMedia(dict["relatedMedia"])]
            except AttributeError:
                if isinstance(dict["relatedMedia"][0], str):
                    # if relatedMedia is a list of strings, turn the strings into dictionaries to
                    # instantiate relatedMediaObjects
                    self._relatedMedia = [
                        RelatedMedia({"@id": i}) for i in dict["relatedMedia"]
                    ]

                else:
                    self._relatedMedia = [RelatedMedia(m) for m in dict["relatedMedia"]]

        if "alertURL" in keys:
            if isinstance(dict["alertURL"], str):
                self._alertURL = dict["alertURL"]
            else:
                self._alertURL = dict["alertURL"]["@id"]

        if "shortURL" in keys:
            if isinstance(dict["shortURL"], str):
                self._shortURL = dict["shortURL"]
            else:
                self._shortURL = dict["shortURL"]["@id"]

        if "previousAlert" in keys:
            if isinstance(dict["previousAlert"], str):
                self._previousAlert = dict["previousAlert"]
            else:
                self._previousAlert = dict["previousAlert"]["@id"]

    def __getattr__(self, attribute):
        return None

    def id(self):
        """
        Returns:
            id (string): url to alert in the FSA page, same as the alertURL attribute.
        """
        try:
            value = self._id
        except AttributeError:
            value = None

        return value

    def title(self):
        """
        Returns:
            title (string): alert title
        """

        try:
            value = self._title
        except AttributeError:
            value = None

        return value

    def shortTitle(self):
        """
        Returns:
            shortTitle (string, optional): compact version of title. None if the API does not provide this value
        """

        try:
            value = self._shortTitle
        except AttributeError:
            value = None

        return value

    def description(self):
        """
        Returns:
            description (string, optional): alert description. None if the API does not provide this value
        """

        try:
            value = self._description
        except AttributeError:
            value = None

        return value

    def created(self):
        """
        Returns:
            created (string): represents date in ISO format
        """

        try:
            value = self._created
        except AttributeError:
            value = None

        return value

    def modified(self):
        """
        Returns:
            modified (string): represents datetime in ISO format
        """

        try:
            value = self._modified
        except AttributeError:
            value = None

        return value

    def notation(self):
        """
        Returns:
            notation (string): unique identifier for alert used in the `foodAlertsAPI.foodAlertsAPI` getAlert() function
        """

        try:
            value = self._notation
        except AttributeError:
            value = None

        return value

    def country(self):
        """
        Returns:
            country (object, optional): a `foodAlertsAPI.Country` object. None if unspecified by the API indicating that the alert may apply to any country in the UK
        """

        try:
            value = self._country
        except AttributeError:
            value = None

        return value

    def countryLabel(self):
        """
        Returns:
            country.label (string, optional): the country that the alerts applies to in string format. None if unspecified
        """
        try:
            value = self._country._label
        except AttributeError:
            value = None

        return value

    def status(self):
        """
        Returns:
            status (string): the alert status in string format
        """

        try:
            value = self._status._label
        except AttributeError:
            value = None

        return value

    def type(self):
        """
        Returns:
            type (string): one of "AA", "FAFA", or "PRIN"
        """
        if ("AA" in self._type[0]) or ("AA" in self._type[1]):
            return "AA"

        elif ("FAFA" in self._type[0]) or ("FAFA" in self._type[1]):
            return "FAFA"

        else:
            return "PRIN"

    def actionTaken(self):
        """
        Returns:
            actionTaken (string, optional): description of the action taken, or in the case of FAFAs actions to be taken by enforcement authority
        """

        try:
            value = self._actionTaken
        except AttributeError:
            value = None

        return value

    def consumerAdvice(self):
        """
        Returns:
            consumerAdvice (string, optional): text giving the advice to consumers
        """

        try:
            value = self._consumerAdvice
        except AttributeError:
            value = None

        return value

    def SMStext(self):
        """
        Returns:
            SMSText (string, optional): short description to be used in SMS notifications
        """

        try:
            value = self._SMStext
        except AttributeError:
            value = None

        return value

    def twitterText(self):
        """
        Returns:
            twitterText (string, optional): short description to be used in Twitter notifications
        """

        try:
            value = self._twitterText
        except AttributeError:
            value = None

        return value

    def alertURL(self):
        """
        Returns:
            alertURL (string, optional): URL for the alert on the FSA web site
        """

        try:
            value = self._alertURL
        except AttributeError:
            value = None

        return value

    def shortURL(self):
        """
        Returns:
            shortURL (string, optional): short URL to alert used in SMS and twitter texts
        """

        try:
            value = self._shortURL
        except AttributeError:
            value = None

        return value

    def relatedMedia(self):
        """
        Returns:
            relatedMedia (object[], optional): array of `foodAlertsAPI.RelatedMedia` objects
        """

        try:
            value = self._relatedMedia
        except AttributeError:
            value = None

        return value

    def problem(self):
        """
        Returns:
            problem (object[], optional): array of `foodAlertsAPI.Problem` objects
        """

        try:
            value = self._problem
        except AttributeError:
            value = None

        return value

    def productDetails(self):
        """
        Returns:
            productDetails (object[], optional): array of `foodAlertsAPI.ProductDetails` objects
        """

        try:
            value = self._productDetails
        except AttributeError:
            value = None

        return value

    def reportingBusiness(self):
        """
        Returns:
            reportingBusiness (string, optional): common name for the reporting business
        """

        try:
            value = self._reportingBusiness._commonName
        except AttributeError:
            value = None

        return value

    def otherBusiness(self):
        """
        Returns:
            otherBusiness (object[], optional): an array of `foodAlertsAPI.Business` objects
        """

        try:
            value = self._otherBusiness
        except AttributeError:
            value = None

        return value

    def previousAlert(self):
        """
        Returns:
            previousAlert (object, optional): a `foodAlertsAPI.Alert` object
        """

        try:
            value = self._previousAlert
        except AttributeError:
            value = None

        return value

    def allergenLabels(self):
        """Get the list of allergens in this Alert

        Returns:
            allergens (string[]): list of allergens as strings
        """

        allergens = []

        for p in self._problem:
            if p._allergen != None:
                for allergen in p._allergen:
                    allergens.append(allergen._label)

        return allergens

    def pathogenRiskLabels(self):
        """Get the list of pathogen risks in this Alert

        Returns:
            pathogenRisks (string[]): list of pathogen risks as strings
        """

        pathogenRisks = []

        for p in self._problem:
            if p._pathogenRisk != None:
                for risk in p._pathogenRisk:
                    pathogenRisks.append(risk._label)

        return pathogenRisks
