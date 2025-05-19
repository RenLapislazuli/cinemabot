from http import HTTPStatus
from typing import Any
from urllib.parse import urljoin

from .base import BaseAiohttpClient


class GoogleClient(BaseAiohttpClient):
    def __init__(
        self,
        base_url: str,
        api_key: str,
        search_engine_key: str
    ) -> None:
        super().__init__(base_url=base_url, header_tokens={"key": api_key, "cx": search_engine_key})


    async def search_google(self, query: str) -> Any:
        async with self.session.get(
            urljoin(self.base_url, "/customsearch/v1"),
            params=self.make_headers({"num":5, "q": query}),
        ) as response:
            assert response.status == HTTPStatus.OK
            return await response.json()
