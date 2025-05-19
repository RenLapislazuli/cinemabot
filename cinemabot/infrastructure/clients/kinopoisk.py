from http import HTTPStatus
from typing import Any
from urllib.parse import urljoin

from .base import BaseAiohttpClient


class FilmNotFoundError(Exception):
    pass


class KinopoiskClient(BaseAiohttpClient):
    def __init__(
        self,
        base_url: str,
        api_key: str,
    ) -> None:
        super().__init__(base_url=base_url, header_tokens={"X-API-KEY": api_key})

    async def search_film_with_keyword(self, keyword: str) -> dict[str, Any]:
        async with self.session.get(
            urljoin(self.base_url, "/v1.4/movie/search"),
            params={"page": 1, "limit": 1, "query": keyword},
            headers=self.make_headers(),
        ) as response:
            response_data = await response.json()
            if response.status != HTTPStatus.OK or not response_data["docs"]:
                raise FilmNotFoundError
        return response_data["docs"][0]

    async def get_image_size(self, url: str) -> int:
        async with self.session.get(url) as response:
            return int(response.headers["Content-Length"])
