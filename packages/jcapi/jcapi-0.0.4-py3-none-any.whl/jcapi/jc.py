"""Asynchronous Python client for JC."""
from __future__ import absolute_import
import asyncio
import json
import socket
from typing import Any, Dict, Mapping, Optional, Tuple, Union

import aiohttp
import async_timeout
import backoff

from .exceptions import JCConnectionError, JCError, JCConnectionTimeoutError, JCEmptyResponseError
from .models import Device,update_from_dict


token = "410108959-1593433502-758739600-d8b2018311-c1436335e1"



class JcApi:
    """Main class for handling connections with Jiachang."""

    _device: Optional[Device] = None

    def __init__(
            self,
            host: str,
            base_path: str,
            token: str,
            password: str = None,
            request_timeout: float = 8.0,
            session: aiohttp.client.ClientSession = None,
            username: str = None,
            user_agent: str = None,

    ) -> None:
        """Initialize connection with JC."""
        self._session = session
        self._close_session = False
        self.base_path = base_path
        self.host = host
        self.password = password
        self.socketaddr = None
        self.request_timeout = request_timeout
        self.username = username
        self.user_agent = user_agent
        self.token = token

    @backoff.on_exception(backoff.expo, JCConnectionError, max_tries=3, logger=None)
    async def _request(
            self,
            uri: str = "",
            id:Optional[int] = None,
            data: Optional[Any] = None,
            params: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """Handle a request to a WLED device."""

        url = "http://182.61.44.102:8281/App/b" + uri + "?hictoken=" + self.token

        auth = None

        if self._session is None:
            # self._session = aiohttp.ClientSession()
            self._close_session = True

        # If updating the state, always request for a state response
        # if method == "POST" and uri == "state" and json_data is not None:
        #     json_data["v"] = True

        try:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(self.request_timeout):
                    response = await session.request(
                        url=url,
                        method="POST",
                        data=data,
                        params=params,
                    )
        except asyncio.TimeoutError as exception:
            raise JCConnectionTimeoutError(
                "Timeout occurred while connecting to JC device."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise JCConnectionError(
                "Error occurred while communicating with JC device."
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if (response.status // 100) in [4, 5]:
            contents = await response.read()
            response.close()

            if content_type == "text/html; charset=UTF-8":
                raise JCConnectionError(response.status, json.loads(contents.decode("utf8")))
            raise JCConnectionError(response.status, {"message": contents.decode("utf8")})

        if "text/html; charset=UTF-8" in content_type:
            data = await response.json(content_type='text/html')
            return data

        return await response.text()

    @backoff.on_exception(
        backoff.expo, JCEmptyResponseError, max_tries=3, logger=None
    )
    async def update(self, full_update: bool = False) -> Device:
        """Get all information about the device in a single call."""
        if self._device is None or full_update:
            data_param = {"rs": "getDevListJson"}
            data = await self._request(uri="/home/status.php", data=data_param)
            if not data:
                raise JCEmptyResponseError(
                    "WLED device returned an empty API response on full update"
                )
            self._device = update_from_dict(data)
            return self._device

    async def get_devices(self):
        """Change master state of a switch device."""
        data = {"rs": "getDevListJson"}
        await self._request(uri="/home/status.php", data=data)

    async def turn_on(self,id):
        """Change master state of a switch device."""
        data = {
            "rs": "execAttr",
            "rsargs[]": id,
            "rsargs[m]": "1"
        }
        await self._request(uri="/devattr/devattr.php", data=data)

    async def turn_off(self,id):
        """Change master state of a switch device."""
        data = {
            "rs": "execAttr",
            "rsargs[]": id,
            "rsargs[m]": "0"
        }
        await self._request(uri="/devattr/devattr.php", data=data)

    async def close(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self):
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()

