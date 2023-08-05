class ProductCategory:
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
