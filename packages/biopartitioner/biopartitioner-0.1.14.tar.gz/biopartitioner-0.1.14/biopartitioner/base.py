from abc import ABCMeta, abstractmethod
from pathlib import PurePosixPath


class PartitionerBase(metaclass=ABCMeta):
    def __init__(self, dataset: str, partition_num: int, working_dir: str):
        self.dataset = dataset
        self.partition_num = partition_num
        self.working_dir = PurePosixPath(working_dir)
        self.num_of_rows = self._count_num_of_rows()

    @abstractmethod
    def partition(self) -> None:
        pass

    @abstractmethod
    def _count_num_of_rows(self) -> int:
        pass
