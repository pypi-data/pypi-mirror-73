from dataclasses import dataclass
from typing import Any, Dict

from bxcommon import constants
from bxcommon.models.blockchain_network_environment import BlockchainNetworkEnvironment
from bxcommon.models.blockchain_network_type import BlockchainNetworkType


@dataclass
class BlockchainNetworkModel:
    # pyre-fixme[8]: Attribute has type `str`; used as `None`.
    protocol: str = None
    # pyre-fixme[8]: Attribute has type `str`; used as `None`.
    network: str = None
    network_num: int = constants.UNASSIGNED_NETWORK_NUMBER
    # pyre-fixme[8]: Attribute has type `BlockchainNetworkType`; used as `None`.
    type: BlockchainNetworkType = None
    # pyre-fixme[8]: Attribute has type `BlockchainNetworkEnvironment`; used as `None`.
    environment: BlockchainNetworkEnvironment = None
    # pyre-fixme[8]: Attribute has type `Dict[str, typing.Any]`; used as `None`.
    default_attributes: Dict[str, Any] = None
    # pyre-fixme[8]: Attribute has type `int`; used as `None`.
    block_interval: int = None
    # pyre-fixme[8]: Attribute has type `int`; used as `None`.
    ignore_block_interval_count: int = None
    # pyre-fixme[8]: Attribute has type `int`; used as `None`.
    block_recovery_timeout_s: int = None
    block_hold_timeout_s: float = constants.DEFAULT_BLOCK_HOLD_TIMEOUT
    # pyre-fixme[8]: Attribute has type `int`; used as `None`.
    final_tx_confirmations_count: int = None
    # pyre-fixme[8]: Attribute has type `int`; used as `None`.
    tx_contents_memory_limit_bytes: int = None
    max_block_size_bytes: int = constants.DEFAULT_MAX_PAYLOAD_LEN_BYTES
    max_tx_size_bytes: int = constants.DEFAULT_MAX_PAYLOAD_LEN_BYTES
    block_confirmations_count: int = constants.BLOCK_CONFIRMATIONS_COUNT
    tx_percent_to_log_by_hash: float = constants.TRANSACTIONS_BY_HASH_PERCENTAGE_TO_LOG_STATS_FOR
    tx_percent_to_log_by_sid: float = constants.TRANSACTIONS_BY_SID_PERCENTAGE_TO_LOG_STATS_FOR
    removed_transactions_history_expiration_s: int = constants.REMOVED_TRANSACTIONS_HISTORY_EXPIRATION_S
    # pyre-fixme[8]: Attribute has type `str`; used as `None`.
    sdn_id: str = None
    tx_sync_interval_s: float = constants.GATEWAY_SYNC_TX_THRESHOLD_S
    tx_sync_sync_content: bool = constants.GATEWAY_SYNC_SYNC_CONTENT
    enable_network_content_logs: bool = False
