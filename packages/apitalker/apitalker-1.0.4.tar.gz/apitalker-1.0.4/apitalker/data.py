from typing import Any, List, Union

from pandas import DataFrame  # type: ignore
from pandas.io.json import _json_normalize  # type: ignore


class Data:
    """Class for handling data returned by using `apitalker.api.API.get_data()` method.
    """

    def __init__(self, data: List[Any]) -> None:
        """Initializes instance of the class.

        Args:
            data (List[Any]): data retrieved from Apitalks API data resource.
        
        Attributes:
            as_list (List[Any]): original data retrieved from Api resource
            as_dataframe (pandas.Dataframe): data as pandas DataFrame object, converted using `pandas._json_normalize()`.
                You can then use various methods, which `pandas.DataFrame` class provides, e.g. for saving data
                in various file types.

        Examples:

            >>> from apitalker.api import API
            >>> 
            >>> api = API("yourapikey")
            >>> 
            >>> data, error = api.get_data("/path/to/resource/", **kwargs)
            >>> 
            >>> if error is None:
            >>>     data.as_dataframe.to_json()
            >>>     data.as_dataframe.to_csv()

        """
        self.as_list: List[Any] = data
        self.as_dataframe: Union[DataFrame, bool] = self.to_dataframe(data=self.as_list)

    def to_dataframe(self, data=None, **kwargs) -> Union[DataFrame, bool]:
        """Converts `data` to DataFrame.

        Keyword Args:
            data (Union[None, Any]): data to normalize and convert into `pandas.core.frame.DataFrame`
            kwargs: keyword args to pass to pandas `_json.normalize()` function, which does the normalization and conversion
                to `DataFrame`. See References for link.

        Returns:
            Union[pandas.core.frame.DataFrame, bool]
                * pandas.core.frame.DataFrame: converted API data to pandas `DataFrame`, if normalization of data was successful. \
                If data cannot be normalized, returns empty `DataFrame`.
            
                * False: if normalization raises an `Exception`. Can happen, if data have deeply nested and irregular structure.
        
        References:
            json_normalize: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.json_normalize.html#pandas-json-normalize
        """
        try:
            return _json_normalize(data, **kwargs)
        except Exception as e:
            print(f"Exception in 'apitalker.data.Data.to_dataframe()': {str(e)}")
            return False
