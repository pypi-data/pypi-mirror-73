import json
from os import makedirs
from os.path import isdir, split
from typing import Any, List, Optional

from pandas import DataFrame
from pandas.io.json import _json_normalize


class Data:
    """Class for handling data returned by using `apitalker.api.API.get_data()` method.
    """

    def __init__(self, data: List[Any]) -> None:
        """Initializes instance of the class.

        Args:
            data (List[Any]): data retrieved from Apitalks API data resource.
        
        Attributes:
            as_list (List[Any]): original data retrieved from Api resource
            as_dataframe (pandas.Dataframe): data as pandas' DataFrame object, converted using `pandas._json_normalize()`
        """
        self.as_list: List[Any] = data
        self.as_dataframe: DataFrame = self.to_dataframe()

    def to_dataframe(self) -> DataFrame:
        """Converts `apitalker.data.Data.as_list` attribute value to DataFrame and
        returns.

        Returns:
            DataFrame: converted API data to pandas DataFrame
        """
        return _json_normalize(self.as_list)

    def to_json(self, filepath: str, **kwargs) -> Optional[int]:
        """Saves `apitalker.data.Data.as_dataframe` in .json fileformat to provided filepath.

        Uses `pandas.DataFrame.to_json()` method to generate strings, so it is possible to
        provide additional keyword parameters, which `to_json()` method accepts.

        Args:
            filepath (str): filepath where the .json file will be saved.

        Returns:
            Optional[int]: 

                None: if save is successful

                1: if `Exception` is raised
        """
        keys = list(kwargs.keys())
        head, _ = split(filepath)

        try:
            if not isdir(head):
                makedirs(head, exist_ok=True)

            result = self.as_dataframe.to_json(
                path_or_buf=None,
                orient=kwargs["orient"] if "orient" in keys else None,
                date_format=kwargs["date_format"] if "date_format" in keys else None,
                double_precision=kwargs["double_precision"]
                if "double_precision" in keys
                else 10,
                force_ascii=kwargs["force_ascii"] if "force_ascii" in keys else True,
                date_unit=kwargs["date_unit"] if "date_unit" in keys else "ms",
                default_handler=kwargs["default_handler"]
                if "default_handler" in keys
                else None,
                lines=kwargs["lines"] if "lines" in keys else False,
                compression=kwargs["compression"] if "compression" in keys else "infer",
                index=kwargs["index"] if "index" in keys else True,
                indent=kwargs["indent"] if "indent" in keys else 0,
            )
            # we do not save directly using pandas method, since it does not support encoding parametrization unfortunately :(
            with open(filepath, mode="w", encoding="utf-8") as f:
                json.dump(
                    json.loads(result),
                    f,
                    ensure_ascii=kwargs["force_ascii"]
                    if "force_ascii" in keys
                    else True,
                    indent=kwargs["indent"] if "indent" in keys else 0,
                )

            return None

        except Exception as e:
            print(f"Method 'apitalks.data.Data.to_json()' exception: {str(e)}")
            return 1
