import base64
from typing import Union, List, Optional, Dict

from bxcommon.utils.object_hash import Sha256Hash
from bxcommon.utils.stats.network_content_event_type import NetworkContent
from bxutils.logging import LogLevel
from bxutils.logging.log_record_type import LogRecordType
from bxutils import logging


class _NetworkStatisticsService:
    def __init__(self):
        self.name = "NetworkContent"
        self.log_level = LogLevel.STATS
        self.logger = logging.get_logger(LogRecordType.NetworkContent)

    def transactions_log_event(
            self, network_num: int, tx_hash: Sha256Hash, tx_content: Union[bytearray, memoryview],
            more_info: Optional[Dict] = None) -> None:
        self.logger.log(
            self.log_level,
            {
                "data": {
                    "network_num": network_num,
                    "tx_hash": tx_hash.binary.hex(),
                    "tx_content": base64.b64encode(tx_content),  # pyre-ignore
                    "more_info": more_info
                },
                "type": NetworkContent.TRANSACTION_CONTENT
            }
        )

    def block_content_log_event(
            self, network_num: int, block_hash: Sha256Hash, block_content: memoryview, more_info: Optional[Dict] = None
    ) -> None:
        self.logger.log(
            self.log_level,
            {
                "data": {
                    "network_num": network_num,
                    "block_hash": block_hash.binary.hex(),
                    "block_content": base64.b64encode(block_content),  # pyre-ignore
                    "more_info": more_info
                },
                "type": NetworkContent.BLOCK_CONTENT
            }
        )

    def block_transactions_log_event(
            self, network_num: int, block_hash: Sha256Hash, block_transactions: List[Sha256Hash]
    ) -> None:
        self.logger.log(
            self.log_level,
            {
                "data": {
                    "network_num": network_num,
                    "block_hash": block_hash.binary.hex(),
                    "block_transactions": block_transactions
                },
                "type": NetworkContent.BLOCK_TRANSACTIONS
            }
        )


connection_stats = _NetworkStatisticsService()
