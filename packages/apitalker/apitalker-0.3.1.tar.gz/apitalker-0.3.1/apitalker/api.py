# pylint: disable=too-many-arguments

from time import sleep
from typing import Any, Dict, List, Union
from urllib.parse import unquote_plus

import requests as r


class ApiResponse:
    """Class for data response of API resource call.

    Keyword Args:
        response (Union[None, Dict[str, List[Any]]], optional): complete response from api call as dict. Defaults to None.
        data (Union[None, List[Any]], optional): only data from response from api call as list. Defaults to None.
        skip (Union[None, int], optional): value of skipped pages. Defaults to None.
        count (Union[None, int], optional): value of count. Defaults to None.
        limit (Union[None, int], optional): value of limit. Defaults to None.
        info (Union[None, Dict[str, str]], optional): value of info. Defaults to None.
        provider (Union[None, str], optional): value of data provider. Defaults to None.

    """

    def __init__(
        self,
        response=None,
        data=None,
        skip=None,
        count=None,
        limit=None,
        info=None,
        provider=None,
    ) -> None:
        self.response: Union[None, Dict[str, List[Any]]] = response
        self.data: Union[None, List[Any]] = data
        self.skip: Union[None, int] = skip
        self.count: Union[None, int] = count
        self.limit: Union[None, int] = limit
        self.info: Union[None, Dict[str, str]] = info
        self.provider: Union[None, str] = provider


class ApiError:
    """Class for data response error return of API resource call.

        Keyword Args:
            response (Union[None, Dict[str, Dict[str, Any]]], optional): complete response message as dict. Defaults to None.
            error (Union[None, Dict[str, Any]], optional): error part of the respone message as dict. Defaults to None.
            status_code (Union[None, int], optional): status code part of the response message. Defaults to None.
            name (Union[None, str], optional): name of the error message. Defaults to None.
            message (Union[None, str], optional): body of the error message. Defaults to None.

    """

    def __init__(
        self, response=None, error=None, status_code=None, name=None, message=None
    ) -> None:
        self.response: Union[None, Dict[str, Dict[str, Any]]] = response
        self.error: Union[None, Dict[str, Any]] = error
        self.status_code: Union[None, int] = status_code
        self.name: Union[None, str] = name
        self.message: Union[None, str] = message


class API(r.Session):
    """API class for connection and getting data from Apitalks API resources.

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

    def query(
        self, resource: str, order=None, where=None, **kwargs
    ) -> Union[ApiResponse, ApiError, int]:
        """Queries API for data from <resource>. See https://www.api.store/czso.cz/dokumentace#section/Query-parametry

        Args:
            resource (str): API resource path as specified in Apitalks documentation

        Keyword Args:
            order (str): order output of returned data of api call.
                e.g `order='"id ASC, nazev DESC"'`. 

            where (str): specifiy filtering of the returned data of api call.
                e.g. `where='"rok":{"gt":2000}'` or `where='"rok=2000,"barva":"red"'`

            limit (int): add limit to set limit for one page of returned data via api call. 

            skip (int): add skip to set number of skipped data entries via api call.
            
        Returns:
            (Union[ApiResponse, ApiError, int])
                ApiResponse: class instance with attributes of successfull API call
                ApiError: class instance with attributes of unsuccessfull API call
                int: 1, if some other bad stuff happened

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
        _json = _response.json()
        _keys = list(_json.keys())
        print(f"Requested API resource: '{unquote_plus(_response.request.url)}'")  # type: ignore

        if _response.status_code in [200]:
            print("Request successful.")

            return ApiResponse(
                response=_json,
                data=_json["data"] if "data" in _keys else None,
                skip=_json["skip"] if "skip" in _keys else None,
                count=_json["count"] if "count" in _keys else None,
                limit=_json["limit"] if "limit" in _keys else None,
                info=_json["info"] if "info" in _keys else None,
                provider=_json["info"]["provider"] if "info" in _keys else None,
            )

        if _response.status_code in [400, 403, 404, 409, 429]:
            print(
                f"API returned error. HTTP response status: {_response.status_code}. Returned message: {_json}."
            )
            return ApiError(
                response=_json,
                error=_json["error"] if "error" in _keys else None,
                status_code=_json["error"]["statusCode"] if "error" in _keys else None,
                name=_json["error"]["name"] if "error" in _keys else None,
                message=_json["error"]["message"] if "error" in _keys else None,
            )

        if _response.status_code in [502, 503, 504]:
            print(
                f"API returned error. HTTP response status: {_response.status_code}. Returned message: {_json}. Retrying..."
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
            print(f"Retried {retries} times. That is enough.")
            return ApiError(
                response=_json,
                error=_json["error"] if "error" in _keys else None,
                status_code=_json["error"]["statusCode"] if "error" in _keys else None,
                name=_json["error"]["name"] if "error" in _keys else None,
                message=_json["error"]["message"] if "error" in _keys else None,
            )

        return 1
