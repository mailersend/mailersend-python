import inspect
import logging
from typing import Any, Dict, Optional, Union, TypeVar, Type, ClassVar
from ..models.base import BaseModel, ModelList, APIResponse
from ..logging import get_logger

T = TypeVar("T", bound=BaseModel)


class BaseResource:
    """Base class for all API resources."""

    BASE_API_URL: ClassVar[str] = ""
    MODEL_CLASS: ClassVar[Type[BaseModel]] = BaseModel

    def __init__(self, client, logger: Optional[logging.Logger] = None):
        """
        Initialize a resource with the API client.

        Args:
            client: The MailerSendClient instance
        """
        self.client = client
        self.logger = logger or get_logger()

    def _create_response(self, response: Any, data: Any = None) -> APIResponse:
        """
        Create unified APIResponse object from HTTP response.

        Args:
            response: The HTTP response object
            data: Optional custom data to include (if None, uses response.json())

        Returns:
            APIResponse object with data, headers, and metadata
        """
        if data is None:
            try:
                data = response.json() if response.content else {}
            except Exception:
                # If JSON parsing fails, use empty dict
                data = {}

        return APIResponse(
            data=data,
            headers=dict(response.headers),
            status_code=response.status_code,
            request_id=response.headers.get("x-request-id"),
            rate_limit_remaining=self._parse_int_header(
                response, "x-apiquota-remaining"
            ),
        )

    def _request(self, method, path, params=None, body=None, data=None) -> Any:
        kwargs = {"method": method, "path": path}
        if params is not None:
            kwargs["params"] = params
        if body is not None:
            kwargs["body"] = body
        result = self.client.request(**kwargs)

        if inspect.isawaitable(result):
            async def resolve():
                response = await result
                if data is not None:
                    return self._create_response(response, data(response))
                return self._create_response(response)
            return resolve()

        if data is not None:
            return self._create_response(result, data(result))
        return self._create_response(result)

    def _parse_int_header(self, response: Any, header: str) -> Optional[int]:
        """
        Safely parse integer header value.

        Args:
            response: The HTTP response object
            header: Header name to parse

        Returns:
            Integer value or None if parsing fails
        """
        value = response.headers.get(header)
        if value:
            try:
                return int(value)
            except ValueError:
                pass
        return None

    def _process_response(
        self, response_data: Dict[str, Any], model_class: Optional[Type[T]] = None
    ) -> Union[T, ModelList[T], Dict[str, Any]]:
        """
        Process the API response data into model instances.

        Args:
            response_data: The raw API response data
            model_class: The model class to use for conversion

        Returns:
            Processed model instance(s) or raw data
        """
        cls = model_class or self.MODEL_CLASS

        if not cls:
            return response_data

        # Handle pagination results
        if isinstance(response_data, dict) and "data" in response_data:
            items = [cls(**item) for item in response_data["data"]]
            return ModelList(
                items=items,
                meta=response_data.get("meta", {}),
                links=response_data.get("links", {}),
            )

        # Handle single item
        if isinstance(response_data, dict):
            return cls(**response_data)

        # Handle list of items
        if isinstance(response_data, list):
            return [cls(**item) for item in response_data]

        return response_data


    pass
