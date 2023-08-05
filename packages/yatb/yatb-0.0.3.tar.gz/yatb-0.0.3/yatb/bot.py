import asyncio
import json
from enum import Enum
from typing import Any, Dict, Iterable, Union

import attr

from . import dtypes, exceptions


class Action(str, Enum):
    """
    Enum of supported Telegram actions (methods)
    """

    get_me = "getMe"
    send_message = "sendMessage"
    send_dice = "sendDice"
    set_webhook = "setWebhook"


@attr.s
class BaseBot:
    """
    Base class for Telegram Bot object.
    Sync and async Bot versions are derived from this class
    """

    token: str = attr.ib()
    client: Any = attr.ib()
    telegram_url: str = attr.ib(default="https://api.telegram.org")

    def __attrs_post_init__(self):
        self.telegram_url = self.telegram_url.rstrip("/")

    def _get_url(self, action: Action):
        return f"{self.telegram_url}/bot{self.token}/{action.value}"

    async def _afinalize_response(self, response: Any):
        response.raise_for_status()

        if asyncio.iscoroutinefunction(response.json):
            data = await response.json()
        else:
            data = response.json()

        if data["ok"] is False:
            raise exceptions.TelegramAPIException(f"Telegram API Exception: {data}")

        return data["result"]

    def _finalize_response(self, response: Any):
        response.raise_for_status()

        data = response.json()
        if data["ok"] is False:
            raise exceptions.TelegramAPIException(f"Telegram API Exception: {data}")

        return data["result"]

    async def _aget(self, url, **params) -> dict:
        response = await self.client.get(url, params=params)
        return await self._afinalize_response(response)

    async def _apost(self, url, **data):
        response = await self.client.post(url, data=data)
        return await self._afinalize_response(response)

    def _get(self, url, **params) -> dict:
        response = self.client.get(url, **params)
        return self._finalize_response(response)

    def _post(self, url, **data):
        response = self.client.post(url, data=data)
        return self._finalize_response(response)


class AsyncBot(BaseBot):
    """
    Asynchronous Telegram Bot
    """

    client: Any = attr.ib()

    async def get_me(self) -> dtypes.User:
        """
        A simple method for testing your bot's auth token. Requires no parameters.
        Returns basic information about the bot in form of a User object.

        https://core.telegram.org/bots/api#getme
        """
        data = await self._aget(self._get_url(Action.get_me))
        return dtypes.User(**data)

    # todo: add support for the remaining options
    async def send_message(
        self, chat_id: Union[str, int], text: str,
    ) -> dtypes.Message:
        """
        Use this method to send text messages.
        On success, the sent Message is returned.

        https://core.telegram.org/bots/api#sendmessage
        """
        data = await self._apost(
            self._get_url(Action.send_message), data={"chat_id": chat_id, "text": text}
        )
        return dtypes.Message(**data)

    async def send_dice(self, chat_id):
        data = await self._apost(
            self._get_url(Action.send_dice), data={"chat_id": chat_id}
        )
        return dtypes.Message(**data)

    async def set_webhook(
        self,
        url: str,
        max_connections: int = None,
        allowed_updates: Iterable[str] = None,
    ):
        """
        Use this method to specify a url and receive
        incoming updates via an outgoing webhook.
        Whenever there is an update for the bot,
        we will send an HTTPS POST request to the
        specified url, containing a JSON-serialized Update.
        """
        data = {"url": url}  # type: Dict[str, Union[str, int]]

        if max_connections is not None:
            data["max_connections"] = max_connections

        if allowed_updates is not None:
            data["allowed_updates"] = json.dumps(allowed_updates)

        response = await self._apost(self._get_url(Action.set_webhook), data=data)

        return response


class Bot(BaseBot):
    """
    Synchronous Telegram Bot
    """

    client: Any = attr.ib()

    def get_me(self) -> dtypes.User:
        """
        A simple method for testing your bot's auth token. Requires no parameters.
        Returns basic information about the bot in form of a User object.

        https://core.telegram.org/bots/api#getme
        """
        data = self._get(self._get_url(Action.get_me))
        return dtypes.User(**data)

    def send_message(self, chat_id: Union[str, int], text: str,) -> dtypes.Message:
        """
        Use this method to send text messages.
        On success, the sent Message is returned.

        https://core.telegram.org/bots/api#sendmessage
        """
        data = self._post(
            self._get_url(Action.send_message), data={"chat_id": chat_id, "text": text}
        )
        return dtypes.Message(**data)

    def send_dice(self, chat_id):
        data = self._post(self._get_url(Action.send_dice), data={"chat_id": chat_id})
        return dtypes.Message(**data)

    def set_webhook(
        self,
        url: str,
        max_connections: int = None,
        allowed_updates: Iterable[str] = None,
    ):
        """
        Use this method to specify a url and receive
        incoming updates via an outgoing webhook.
        Whenever there is an update for the bot,
        we will send an HTTPS POST request to the
        specified url, containing a JSON-serialized Update.
        """
        data = {"url": url}  # type: Dict[str, Union[str, int]]

        if max_connections is not None:
            data["max_connections"] = max_connections

        if allowed_updates is not None:
            data["allowed_updates"] = json.dumps(allowed_updates)

        response = self._post(self._get_url(Action.set_webhook), data=data)

        return response
