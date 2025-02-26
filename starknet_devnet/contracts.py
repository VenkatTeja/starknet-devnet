"""
Class for storing and handling contracts
"""

from typing import Dict

from starkware.starknet.services.api.contract_class import ContractClass

from .origin import Origin
from .util import StarknetDevnetException, fixed_length_hex
from .contract_wrapper import ContractWrapper


class DevnetContracts:
    """
    This class is used to store the deployed contracts of the devnet.
    """

    def __init__(self, origin: Origin):
        self.origin = origin
        self.__instances: Dict[int, ContractWrapper] = {}
        self.__classes: Dict[int, ContractClass] = {}

    def store(self, address: int, contract_wrapper: ContractWrapper) -> None:
        """
        Store the contract wrapper.
        """
        self.__instances[address] = contract_wrapper

        class_hash = self.get_class_hash_at(address)
        self.__classes[class_hash] = contract_wrapper.contract_class

    def store_class(self, class_hash: int, contract_class: ContractClass) -> None:
        """Store contract class."""
        self.__classes[class_hash] = contract_class.remove_debug_info()

    def is_deployed(self, address: int) -> bool:
        """
        Check if the contract is deployed.
        """
        return address in self.__instances

    def get_by_address(self, address: int) -> ContractWrapper:
        """
        Get the contract wrapper by address.
        """
        if not self.is_deployed(address):
            message = (
                f"No contract at the provided address ({fixed_length_hex(address)})."
            )
            raise StarknetDevnetException(message=message)

        return self.__instances[address]

    def get_code(self, address: int) -> str:
        """
        Get the contract code by address.
        """
        if not self.is_deployed(address):
            return self.origin.get_code(address)

        return self.__instances[address].code

    def get_full_contract(self, address: int) -> ContractClass:
        """
        Get the contract wrapper by address.
        """
        contract_wrapper = self.get_by_address(address)
        return contract_wrapper.contract_class

    def get_class_by_hash(self, class_hash: int) -> ContractClass:
        """Gets the class from the provided class_hash."""
        if class_hash not in self.__classes:
            return self.origin.get_class_by_hash(class_hash)

        return self.__classes[class_hash]

    def get_class_hash_at(self, address: int) -> int:
        """Gets the class hash at the provided address."""
        if not self.is_deployed(address):
            return self.origin.get_class_hash_at(address)

        contract_states = self.__instances[address].contract.state.state.contract_states
        class_hash_hexed = contract_states[address].state.contract_hash.hex()
        return int(class_hash_hexed, 16)
