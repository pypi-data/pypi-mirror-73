from collections import defaultdict
from datetime import datetime
from typing import Dict, Type, Any, TYPE_CHECKING

from bxcommon import constants
from bxcommon.utils import memory_utils
from bxcommon.utils.sizer import Sizer
from bxcommon.utils.stats.class_mem_stats import ClassMemStats
from bxcommon.utils.stats.statistics_service import StatsIntervalData, ThreadedStatisticsService
from bxutils import logging
from bxutils.logging.log_record_type import LogRecordType

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    # pylint: disable=ungrouped-imports,cyclic-import
    from bxcommon.connections.abstract_node import AbstractNode


class MemoryStatsIntervalData(StatsIntervalData):
    class_mem_stats: Dict[str, ClassMemStats]

    def __init__(self, *args, **kwargs):
        super(MemoryStatsIntervalData, self).__init__(*args, **kwargs)
        self.class_mem_stats = defaultdict(ClassMemStats)


# pyre-fixme[24]: Type parameter `AbstractNode` violates constraints on `T` in
#  generic type `ThreadedStatisticsService`.
# pyre-fixme[24]: Type parameter `MemoryStatsIntervalData` violates constraints on
#  `N` in generic type `ThreadedStatisticsService`.
class MemoryStatsService(ThreadedStatisticsService[MemoryStatsIntervalData, "AbstractNode"]):
    def __init__(self, interval: int = 0):
        self.sizer_obj = Sizer()
        super(MemoryStatsService, self).__init__(
            "MemoryStats",
            interval=interval,
            look_back=5,
            reset=False,
            stat_logger=logging.get_logger(LogRecordType.Memory, __name__),
        )

    def get_interval_data_class(self) -> Type[MemoryStatsIntervalData]:
        return MemoryStatsIntervalData

    def set_node(self, node: "AbstractNode") -> None:
        super(MemoryStatsService, self).set_node(node)
        self.interval = node.opts.memory_stats_interval
        self.sizer_obj = Sizer(node)

    def add_mem_stats(
        self,
        class_name,
        network_num,
        obj,
        obj_name,
        obj_mem_info,
        object_type=None,
        size_type=None,
        object_item_count=None,
    ):
        # If the object being analyzed doesn't have a length property
        if object_item_count is None:
            object_item_count = len(obj) if hasattr(obj, "__len__") else 0

        if (
            obj_mem_info.size < constants.MEM_STATS_OBJECT_SIZE_THRESHOLD
            and object_item_count < constants.MEM_STATS_OBJECT_COUNT_THRESHOLD
        ):
            return

        mem_stats = self.interval_data.class_mem_stats[class_name]
        mem_stats.timestamp = datetime.utcnow()

        mem_stats.networks[network_num].analyzed_objects[
            obj_name
        ].object_item_count = object_item_count
        mem_stats.networks[network_num].analyzed_objects[obj_name].object_size = obj_mem_info.size
        mem_stats.networks[network_num].analyzed_objects[
            obj_name
        ].object_flat_size = obj_mem_info.flat_size
        mem_stats.networks[network_num].analyzed_objects[
            obj_name
        ].is_actual_size = obj_mem_info.is_actual_size
        mem_stats.networks[network_num].analyzed_objects[obj_name].object_type = object_type
        mem_stats.networks[network_num].analyzed_objects[obj_name].size_type = size_type

    def get_info(self) -> Dict[str, Any]:
        # total_mem_usage is the peak mem usage fo the process (kilobytes on Linux, bytes on OS X)
        assert self.node is not None
        assert self.interval_data is not None
        payload = {
            # pyre-fixme[16]: Optional type has no attribute `opts`.
            "node_id": self.node.opts.node_id,
            "node_type": self.node.opts.node_type,
            "node_network_num": self.node.opts.blockchain_network_num,
            "node_address": f"{self.node.opts.external_ip}:{self.node.opts.external_port}",
            "total_mem_usage": memory_utils.get_app_memory_usage(),
            # pyre-ignore having some difficulty with subclassing generics
            "classes": self.interval_data.class_mem_stats,
        }

        return payload

    def flush_info(self) -> int:
        assert self.node is not None
        # pyre-fixme[16]: Optional type has no attribute `dump_memory_usage`.
        self.node.dump_memory_usage()
        return super(MemoryStatsService, self).flush_info()

    def increment_mem_stats(
        self,
        class_name,
        network_num,
        obj,
        obj_name,
        obj_mem_info,
        object_type=None,
        size_type=None,
        object_item_count=None,
    ):
        mem_stats = self.interval_data.class_mem_stats[class_name]

        # If the object being analyzed doesn't have a length property
        if object_item_count is None:
            object_item_count = len(obj) if hasattr(obj, "__len__") else 1

        mem_stats.networks[network_num].analyzed_objects[
            obj_name
        ].object_item_count += object_item_count
        mem_stats.networks[network_num].analyzed_objects[obj_name].object_size += obj_mem_info.size
        mem_stats.networks[network_num].analyzed_objects[
            obj_name
        ].object_flat_size += obj_mem_info.flat_size
        mem_stats.networks[network_num].analyzed_objects[
            obj_name
        ].is_actual_size = obj_mem_info.is_actual_size
        mem_stats.networks[network_num].analyzed_objects[obj_name].object_type = object_type
        mem_stats.networks[network_num].analyzed_objects[obj_name].size_type = size_type

    def reset_class_mem_stats(self, class_name):
        mem_stats = ClassMemStats()
        mem_stats.timestamp = datetime.utcnow()
        self.interval_data.class_mem_stats[class_name] = mem_stats


memory_statistics = MemoryStatsService(constants.MEMORY_STATS_INTERVAL_S)
