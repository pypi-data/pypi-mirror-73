import asyncio
import json
from errno import ECONNREFUSED
from sys import maxsize
from typing import Callable

import websockets
from websockets.http import Headers

from .log import init_logger


class WebSocketClient():

    def __init__(self, url, options):
        self.number = 0
        self.url = url
        self.autoReconnectInterval = 5 * 1000
        self.options = options
        self._debug = options['debug'] | True

        self.callbacks = {}
        self.logger = init_logger(__name__, testing_mode=False)
        self.connectme()

    async def message(self, msg):
        self.number += 1
        if self.number >= maxsize:
            self.logger.info('Resetting message number')
            self.number = 1
        await self.on_message(msg)

    async def error(self, error):
        if error == ECONNREFUSED:
            await self.reconnect()
        else:
            await self.on_error(error)

    async def on_message(self, message):
        self.logger.info(message)
        message = json.loads(message)
        message_type = 'incoming-message' if message["type"] == 'message' else 'system-message'
        self.logger.debug(message_type, self.number, message)
        await self.callbacks['message'](message)

    async def on_error(self, error):
        self.logger.error("error", error)
        await self.callbacks['error'](error)

    def on_close(self):
        self.callbacks['close']()
        self.reconnect()

    def connectme(self):
        headers = Headers(self.options["headers"])
        self.ws = websockets.connect(self.url, extra_headers=headers)

    async def send(self, data, callback=None):
        data = json.dumps(data)
        async with self.ws as websocket:
            try:
                await websocket.send(data)
            except Exception as e:
                self.logger.error(e)
                self.callbacks['error'](e)

    async def reconnect(self):
        self.logger.warn('Connection failed',
                         f'retry in {self.autoReconnectInterval}ms')
        async with self.ws as websocket:
            try:
                await websocket.close()
            except websockets.exceptions.ConnectionClosedError:
                self.logger.info('Connection Closed unexpectedly')
                self.on_close()
            except websockets.exceptions.ConnectionClosedOK:
                self.logger.info('Connection closed by remote')
                await self.on_close()

        await asyncio.sleep(self.autoReconnectInterval)
        self.connectme()
        self.logger.info("Reconnecting...")
        await self.start()

    def register_callback(self, event, callback: Callable) -> None:
        if event in self.callbacks:
            self.logger.info(f"Replacing callback function for {event} event")
        else:
            self.logger.info(f"Setting callback function for {event} event")
        self.callbacks[event] = callback

    async def start(self):

        async with self.ws as websocket:
            while True:
                try:
                    message = await websocket.recv()

                    await self.message(message)

                except websockets.exceptions.ConnectionClosedError as error:
                    self.logger.info(f'Connection Closed unexpectedly {error}')
                    self.on_close()
                except websockets.exceptions.ConnectionClosedOK as error:
                    self.logger.info(f'Connection closed by remote {error}')
                    await self.on_close()
