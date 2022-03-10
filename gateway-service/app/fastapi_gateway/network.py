import aiohttp
import async_timeout
from typing import Optional, Union
from aiohttp import JsonPayload
from starlette.datastructures import Headers
from .utils.form import CustomFormData
from .utils.response import decode_json
from .utils.request import create_dict_if_not


async def make_request(
    url: str,
    method: str,
    headers: Union[Headers, dict],
    query: Optional[dict] = None,
    data: Union[CustomFormData, JsonPayload] = None,
    timeout: int = 60,
):
    data = create_dict_if_not(data=data)
    query = create_dict_if_not(data=query)

    with async_timeout.timeout(timeout):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.request(
                    method=method, url=url, params=query, data=data) as response:
                response_json = await response.json()
                decoded_json = decode_json(data=response_json)
                return decoded_json, response.status, response.headers
