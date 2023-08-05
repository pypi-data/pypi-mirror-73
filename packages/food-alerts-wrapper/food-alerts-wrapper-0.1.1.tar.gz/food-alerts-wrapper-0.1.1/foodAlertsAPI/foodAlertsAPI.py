import requests
from foodAlertsAPI.Alert import Alert


class foodAlertsAPI:

    # a negative limit value would return all entries
    def getAlerts(
        self,
        quantifier=None,
        detailed=False,
        limit=None,
        offset=None,
        sortBy=None,
        filters={},
    ):
        """Gets alerts from the FSA Food Alerts API

        Args:
            quantifier: the quantifier can be an int n, in which case the function returns the last n
                        alerts. The quantifier can also be a date string in ISO format, in which case 
                        the function returns the alerts published since the given date
            detailed (bool, optional): determines whether the Alert objects returned will contain all properties. When this
                             is set to false, only the summary properties are included. Defaults to False if unspecified
            limit (int, optional): specifies the maximum number of Alert objects that can be returned
            offset (int, optional): return the list of items starting with the nth item, together with limit this enables paging through a long set of results
            sortBy (string, optional): reorder the list of results in ascending order of the given property (or property chain). 
                                       To sort in descending order use sortBy=-prop. More than one sort can be included in which case they will be applied in order
            filters (dict, optional): filters based on alert object properties, e.g. {"type":"AA"}
                             
        Returns:
            A list of `foodAlertsAPI.Alert` objects

        Raises:
            ValueError: occurs when an invalid value for the quantifier or optional arguments is provided
        """

        params = {}

        if detailed:
            params["_view"] = "full"

        if limit != None:
            params["_limit"] = limit

        if offset != None:
            params["_offset"] = offset

        if sortBy != None:
            params["_sort"] = sortBy

        # combining the two dictionaries, params and filters

        params = {**params, **filters}
        # if quantifier is an int, then use the limit param
        try:
            limit = int(quantifier)
            r = requests.get(
                f"https://data.food.gov.uk/food-alerts/id?_limit={limit}", params=params
            )

        except ValueError:
            # if quantifier is not an int, try if it works as an iso datetime string
            try:
                since = quantifier
                r = requests.get(
                    f"https://data.food.gov.uk/food-alerts/id?since={since}",
                    params=params,
                )
                r.raise_for_status()

            except requests.HTTPError:
                raise ValueError(
                    """Quantifier must be an integer or an ISO datetime string"""
                )

        items = r.json()["items"]
        alerts = [Alert(a) for a in items]

        return alerts

    def searchAlerts(
        self, query, detailed=False, limit=None, offset=None, sortBy=None, filters={}
    ):
        """Search for query in alerts from the FSA Food Alerts API

        Args:
            query (string): the search query
            detailed (bool, optional): determines whether the Alert objects returned will contain all properties. When this
                                       is set to false, only the summary properties are included. Defaults to False if unspecified
            limit (int, optional): specifies the maximum number of Alert objects that can be returned
            offset (int, optional): return the list of items starting with the nth item, together with limit this enables paging through a long set of results
            sortBy (string, optional): reorder the list of results in ascending order of the given property (or property chain). 
                                       To sort in descending order use sortBy=-prop. More than one sort can be included in which case they will be applied in order
            filters (dict, optional): filters based on alert object properties, e.g. {"type":"AA"}        

        Returns:
            A list of `foodAlertsAPI.Alert` objects

        Raises:
            ValueError: occurs when an invalid value for the query or optional arguments is provided
        """

        params = {}

        if detailed:
            params["_view"] = "full"

        if limit != None:
            params["_limit"] = limit

        if offset != None:
            params["_offset"] = offset

        if sortBy != None:
            params["_sort"] = sortBy

        params = {**params, **filters}

        try:
            r = requests.get(
                f"https://data.food.gov.uk/food-alerts/id?search={query}", params=params
            )
            r.raise_for_status()

            items = r.json()["items"]
            alerts = [Alert(a) for a in items]

        except requests.HTTPError:
            raise ValueError("""Query must be a valid search query string""")

        return alerts

    def getAlert(self, ID):
        """Get a specific alert based on its notation, e.g. (FSA-AA-01-2018)

        Args:
            ID (string): the alert ID                 

        Returns:
            A `foodAlertsAPI.Alert` object

        Raises:
            ValueError: occurs when an invalid value for the notation is provided
        """

        try:
            r = requests.get(f"https://data.food.gov.uk/food-alerts/id/{ID}")
            r.raise_for_status()

            alert = Alert(r.json()["items"][0])

        except requests.HTTPError:
            raise ValueError("Argument must be a valid alert ID")

        return alert
