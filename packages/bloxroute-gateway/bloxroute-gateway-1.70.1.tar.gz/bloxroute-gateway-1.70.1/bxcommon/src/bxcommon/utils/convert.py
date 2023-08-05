import binascii
from binascii import Error
from typing import Dict, Optional

from bxcommon.connections.connection_type import ConnectionType
from bxcommon.models.node_type import NodeType

NODE_TO_CONNECTION_TYPE: Dict[NodeType, Dict[NodeType, ConnectionType]] = {
    NodeType.GATEWAY: {
        NodeType.GATEWAY: ConnectionType.GATEWAY,
        NodeType.INTERNAL_GATEWAY: ConnectionType.GATEWAY,
        NodeType.EXTERNAL_GATEWAY: ConnectionType.GATEWAY,
        NodeType.RELAY_TRANSACTION: ConnectionType.RELAY_TRANSACTION,
        NodeType.RELAY_BLOCK: ConnectionType.RELAY_BLOCK,
        NodeType.RELAY: ConnectionType.RELAY_ALL
    },
    NodeType.INTERNAL_GATEWAY: {
        NodeType.GATEWAY: ConnectionType.GATEWAY,
        NodeType.INTERNAL_GATEWAY: ConnectionType.INTERNAL_GATEWAY,
        NodeType.EXTERNAL_GATEWAY: ConnectionType.EXTERNAL_GATEWAY,
        NodeType.RELAY_TRANSACTION: ConnectionType.RELAY_TRANSACTION,
        NodeType.RELAY_BLOCK: ConnectionType.RELAY_BLOCK,
        NodeType.RELAY: ConnectionType.RELAY_ALL
    },
    NodeType.EXTERNAL_GATEWAY: {
        NodeType.GATEWAY: ConnectionType.GATEWAY,
        NodeType.INTERNAL_GATEWAY: ConnectionType.INTERNAL_GATEWAY,
        NodeType.EXTERNAL_GATEWAY: ConnectionType.EXTERNAL_GATEWAY,
        NodeType.RELAY_TRANSACTION: ConnectionType.RELAY_TRANSACTION,
        NodeType.RELAY_BLOCK: ConnectionType.RELAY_BLOCK,
        NodeType.RELAY: ConnectionType.RELAY_ALL
    },
    NodeType.RELAY_BLOCK: {
        NodeType.GATEWAY: ConnectionType.GATEWAY,
        NodeType.INTERNAL_GATEWAY: ConnectionType.INTERNAL_GATEWAY,
        NodeType.EXTERNAL_GATEWAY: ConnectionType.EXTERNAL_GATEWAY,
        NodeType.RELAY_TRANSACTION: ConnectionType.CROSS_RELAY,
        NodeType.RELAY_BLOCK: ConnectionType.RELAY_BLOCK,
        NodeType.RELAY: ConnectionType.RELAY_ALL,
        NodeType.API_SOCKET: ConnectionType.SDN
    },
    NodeType.RELAY_TRANSACTION: {
        NodeType.GATEWAY: ConnectionType.GATEWAY,
        NodeType.INTERNAL_GATEWAY: ConnectionType.INTERNAL_GATEWAY,
        NodeType.EXTERNAL_GATEWAY: ConnectionType.EXTERNAL_GATEWAY,
        NodeType.RELAY_TRANSACTION: ConnectionType.RELAY_TRANSACTION,
        NodeType.RELAY_BLOCK: ConnectionType.CROSS_RELAY,
        NodeType.RELAY: ConnectionType.RELAY_ALL,
        NodeType.API_SOCKET: ConnectionType.SDN
    },
    NodeType.RELAY: {
        NodeType.GATEWAY: ConnectionType.GATEWAY,
        NodeType.INTERNAL_GATEWAY: ConnectionType.INTERNAL_GATEWAY,
        NodeType.EXTERNAL_GATEWAY: ConnectionType.EXTERNAL_GATEWAY,
        NodeType.RELAY: ConnectionType.RELAY_ALL,
        NodeType.API_SOCKET: ConnectionType.SDN
    }
}


def str_to_bool(value):
    return value in ["True", "true", "1"]


def bytes_to_hex(s):
    """
    Encodes bytes to hex
    :param s: bytes
    :return: HEX representation of bytes
    """

    if not isinstance(s, (bytes, bytearray, memoryview)):
        raise TypeError("Value must be an instance of str")
    return binascii.hexlify(s).decode("utf-8")


def hex_to_bytes(s):
    """
    Decodes hex string to bytes
    :param s: hex string
    :return: bytes
    """

    if not isinstance(s, (str, bytes, bytearray, memoryview)):
        raise TypeError("Value must be an instance of str or unicode")
    try:
        return binascii.unhexlify(s)
    except Error as e:
        raise ValueError(f"Invalid hex string provided: {s}.") from e


def peer_node_to_connection_type(node_type: NodeType, peer_node_type: Optional[NodeType]) -> ConnectionType:
    if peer_node_type is None:
        raise ValueError("peer node type can't be None!")
    return NODE_TO_CONNECTION_TYPE[node_type][peer_node_type]
