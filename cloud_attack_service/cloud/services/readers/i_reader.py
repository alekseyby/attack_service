from typing import List

from cloud.services.entities import VirtualMachineEntity, FirewallRuleEntity

from abc import ABC, abstractmethod


class IFileReader(ABC):

    @staticmethod
    @abstractmethod
    def file_to_dict(filename: str) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def file_content_to_entities(filename: str) -> (List[VirtualMachineEntity], List[FirewallRuleEntity]):
        pass
