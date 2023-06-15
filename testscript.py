"""Run an example script to quickly test."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import json

from aioambient import Websocket
from aioambient.errors import WebsocketError

_LOGGER = logging.getLogger()

API_KEY = ["f759604cff504167adc5c5ca98ad5c00cc2b14e2362a4be88e52936fbaba1453",
           "b93528c5ad494a70bf4cf804b1fcf92df2ffddd530084ab7903fac42c235becd"]
APP_KEY = "13ec7b504f8b4ab5b0cd97d8f0f8b570cba24a36dedf4fe5938e9754b471ba59"


def print_data(data: dict[str, Any]) -> None:
    """Print data as it is received.
    Args:
        data: The websocket data received.
    """
    _LOGGER.info(data, '\n')
    
    jdata = json.dumps(data)
    
    print('THIS IS DATA')
    print(jdata)
    print('THIS WAS DATA')
    f = open("datame.txt", "a")
    f.write(jdata)
    f.write('\n')
    f.close()


def print_goodbye() -> None:
    """Print a simple "goodbye" message."""
    _LOGGER.info("Client has disconnected from the websocket")


def print_hello() -> None:
    """Print a simple "hello" message."""
    _LOGGER.info("a")


def print_subscribed(data: dict[str, Any]) -> None:
    """Print subscription data as it is received.
    Args:
        data: The websocket data received.
    """
    _LOGGER.info("a")


async def main() -> None:
    """Run the websocket example."""
    logging.basicConfig(level=logging.INFO)

    websocket = Websocket(APP_KEY, API_KEY)

    websocket.on_connect(print_hello)
    websocket.on_data(print_data)
    websocket.on_disconnect(print_goodbye)
    websocket.on_subscribed(print_subscribed)

    try:
        await websocket.connect()
    except WebsocketError as err:
        _LOGGER.error("a", err)
        return

    while True:
        _LOGGER.info("a")
        await asyncio.sleep(5)


asyncio.run(main())


