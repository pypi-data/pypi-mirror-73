# FSA Food Alerts API Python Wrapper

This is a Python wrapper for the [FSA Food Alerts API](https://data.food.gov.uk/food-alerts/ui/reference), created with the aim of making interactions with the API much simpler so developers can focus on processing and analysing the data it provides.

This Python 3 wrapper is created using the [requests](https://requests.readthedocs.io/en/master/) package. It abstracts the details of HTTP requests away so that the user can just interact with API data. Using the wrapper, developers can access data from the API by simply calling intuitive functions, such as `getAlerts()` and `searchAlerts()`.

These functions also parse the HTTP response, so the user can simply access the response data as Python objects. 

## Example

```python
from foodAlertsAPI import foodAlertsAPI

f = foodAlertsAPI()

yearAgo = (datetime.now() - timedelta(days=365)).isoformat()
alerts = f.getAlerts(yearAgo)

allergenCounts = defaultdict(int)

alert: Alert  # type hinting for code completion
for alert in alerts:
    allergens = alert.allergenLabels()
    for allergen in allergens:
        allergenCounts[allergen] += 1

# get the 10 most frequently occurring allergens
sortedAllergens = [
    (k, v)
    for k, v in sorted(
        allergenCounts.items(), key=lambda item: item[1], reverse=True
    )][:10]

labels = [k for (k, v) in sortedAllergens]
heights = [v for k, v in sortedAllergens]

plt.bar(labels, heights, color="green")
plt.xticks(rotation="vertical")
plt.title("10 Most Common Allergens in the Past Year")
plt.tight_layout()
plt.show()
```

![Allergens column chart](https://github.com/epimorphics/food-alerts-wrapper/raw/master/top_allergens.png)

The example above plots a column chart of the 10 most frequently occurring allergens in alerts over the past year. The entirety of data acquisition and parsing has been accomplished using only `getAlerts()` and `allergenLabels()`, allowing for succinct and readable code. 

## Documentation Summary


The two most important classes in the wrapper are `foodAlertsAPI` and `Alert`. Below is an excerpt of the documentation relevant to these two classes.

### foodAlertsAPI

**Methods:**

`getAlert(ID)`

Get a specific alert based on its notation, e.g. (FSA-AA-01-2018)

_Parameters_

- ID (string) – the alert ID

_Returns_

an Alert object

_Raises_

ValueError – occurs when an invalid value for the notation is provided

`getAlerts(quantifier=None, detailed=False, limit=None, offset=None, sortBy=None, filters={})`

Gets alerts from the FSA Food Alerts API

_Parameters_


- quantifier – the quantifier can be an int n, in which case the function returns the last n alerts. The quantifier can also be a date string in ISO format, in which case the function returns the alerts published since the given date

- detailed (bool, optional) – determines whether the Alert objects returned will contain all properties. When this is set to false, only the summary properties are included. Defaults to False if unspecified

- limit (int, optional) – specifies the maximum number of Alert objects that can be returned

- offset (int, optional) – return the list of items starting with the nth item, together with limit this enables paging through a long set of results

- sortBy (string, optional) – reorder the list of results in ascending order of the given property (or property chain). To sort in descending order use sortBy=-prop. More than one sort can be included in which case they will be applied in order

- filters (dict, optional) – filters based on alert object properties, e.g. {“type”:”AA”}

_Returns_

a list of Alert objects

_Raises_

ValueError – occurs when an invalid value for the quantifier or optional arguments is provided

`searchAlerts(query, detailed=False, limit=None, offset=None, sortBy=None, filters={})`

Search for query in alerts from the FSA Food Alerts API

_Parameters_

- query (string) – the search query

- detailed (bool, optional) – determines whether the Alert objects returned will contain all properties. When this is set to false, only the summary properties are included. Defaults to False if unspecified

- limit (int, optional) – specifies the maximum number of Alert objects that can be returned

- offset (int, optional) – return the list of items starting with the nth item, together with limit this enables paging through a long set of results

- sortBy (string, optional) – reorder the list of results in ascending order of the given property (or property chain). To sort in descending order use sortBy=-prop. More than one sort can be included in which case they will be applied in order

- filters (dict, optional) – filters based on alert object properties, e.g. {“type”:”AA”}

_Returns_

list of Alert objects

_Raises_

ValueError – occurs when an invalid value for the query or optional arguments is provided

### Alert

**Methods:**

`id()`

_Returns_

(string) url to alert in the FSA page, same as the alertURL attribute.

`title()`

_Returns_

(string) alert title

`modified()`

_Returns_

(string) datetime when the alert is last modified in ISO format

`notation()`

_Returns_

(string) unique identifier for alert used in the foodAlertsAPI.foodAlertsAPI getAlert() function

`type()`

_Returns_

(string) one of “AA”, “FAFA”, or “PRIN”

