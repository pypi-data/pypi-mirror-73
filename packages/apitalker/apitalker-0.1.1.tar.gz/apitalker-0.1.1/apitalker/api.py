from time import sleep
from typing import Any, Union
from urllib.parse import unquote_plus

import requests as r


class API(r.Session):
    """API class for connection and getting data from Apitalks API resources.

    Args:
        r (r.Session): inheriting requests.Session class methods
    """

    base_url = "https://api.apitalks.store"
    max_limit = 30
    default_skip = 0

    def __init__(self, api_key: str) -> None:
        """Initializes the class.

        Args:
            api_key (str): api key. You need to register to Apitalks (free) to get it
        """
        super().__init__()
        self.api_auth_name = "x-api-key"
        self.api_key = api_key

    def query(self, resource: str, order=None, where=None, **kwargs) -> Union[Any, int]:
        """Queries API for data from <resource>.

        Args:
            resource (str): API resource path as specified in Apitalks documentation

        Kwargs:
            order (str): order output of returned data of api call. Argument has to adhere to formatting standard
                as specified in Apitalks documentation.
                e.g `order='"id ASC, nazev DESC"'`. See https://www.api.store/czso.cz/dokumentace#section/Query-parametry

            where (str): specifiy filtering of the returned data of api call. Argument has to adhere to formatting standard
                as specified in Apitalks documentation.
                e.g. `where='"rok":{"gt":2000}'` or `where='"rok=2000,"barva":"red"'

            limit (int): add limit to set limit for one page of returned data via api call. 
                See: https://www.api.store/czso.cz/dokumentace#section/Query-parametry

            skip (int): add skip to set number of skipped pages via api call. Value should be same, as for argument <limit>.
                See https://www.api.store/czso.cz/dokumentace#section/Query-parametry
            
        Returns:
            (int): 0: success; 1: failure
        """
        keys_ = list(kwargs.keys())
        retries = kwargs["retries"] if "retries" in keys_ else 0

        # create always added filters for api request params
        limit_ = str(kwargs["limit"]) if "limit" in keys_ else self.max_limit
        skip_ = str(kwargs["skip"]) if "skip" in keys_ else self.default_skip
        filter_ = "".join([r'{"limit":', f"{limit_}", ",", r'"skip":', f"{skip_}", "}"])

        # check and add other filters for api request params
        if order is not None:
            order_param_ = "".join([",", r'"order":', "[", f"{order}", "]", "}"])
            filter_ = filter_.replace(filter_[-1], order_param_)

        if where is not None:
            where_param_ = "".join([",", r'"where":', "{", f"{where}", "}", "}"])
            filter_ = filter_.replace(filter_[-1], where_param_)

        # send api request
        _response = self.get(
            f"{self.base_url}{resource}",
            headers={self.api_auth_name: self.api_key},
            params={"filter": filter_},
        )
        print(f"Requested API resource: '{unquote_plus(_response.request.url)}'")  # type: ignore

        if _response.status_code in [200]:
            print("Request successfull. Returning 0.")
            return _response.json()

        if _response.status_code in [400, 403, 404, 409, 429]:
            print(f"API returned error status: {_response.status_code}. Returning 1.")
            return 1

        if _response.status_code in [502, 503, 504]:
            print(
                f"API returned error status: {_response.status_code}. Retrying for {retries + 1} time..."
            )
            if retries <= 10:
                sleep(retries * 2)
                retries += 1
                return self.query(
                    resource,
                    retries=retries,
                    order=order,
                    where=where,
                    limit=limit_,
                    skip=skip_,
                    **kwargs,
                )

            print(f"Retried {retries} times. Returning 1.")
            return 1

        return 1
