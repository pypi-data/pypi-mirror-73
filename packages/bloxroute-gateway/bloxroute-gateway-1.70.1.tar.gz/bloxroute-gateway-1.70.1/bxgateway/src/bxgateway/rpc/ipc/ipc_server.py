import os
from typing import Optional, List, TYPE_CHECKING
from bxgateway.feed.feed_manager import FeedManager
from bxgateway.rpc.subscription_rpc_handler import SubscriptionRpcHandler
from bxgateway.rpc.ws.ws_connection import WsConnection
from bxutils import logging
from bxcommon.utils import config

import websockets
from websockets import WebSocketServerProtocol
from websockets.server import WebSocketServer

if TYPE_CHECKING:
    from bxgateway.connections.abstract_gateway_node import AbstractGatewayNode

logger = logging.get_logger(__name__)


class IpcServer:
    def __init__(self, ipc_file: str, feed_manager: FeedManager, node: "AbstractGatewayNode"):
        self.ipc_path = config.get_data_file(ipc_file)
        self.node = node
        self.feed_manager = feed_manager
        self._server: Optional[WebSocketServer] = None
        self._connections: List[WsConnection] = []

    async def start(self) -> None:
        if os.path.exists(self.ipc_path):
            os.remove(self.ipc_path)
        self._server = await websockets.unix_serve(self.handle_connection, self.ipc_path)

    async def stop(self) -> None:
        server = self._server
        if server is not None:
            for connection in self._connections:
                connection.close()

            server.close()
            await server.wait_closed()
        if os.path.exists(self.ipc_path):
            os.remove(self.ipc_path)

    async def handle_connection(self, websocket: WebSocketServerProtocol, path: str) -> None:
        logger.trace("Accepting new IPC connection...")
        connection = WsConnection(
            websocket,
            path,
            SubscriptionRpcHandler(self.node, self.feed_manager)
        )
        self._connections.append(connection)
        await connection.handle()
        self._connections.remove(connection)
