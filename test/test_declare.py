"""
Tests of contract class declaration and deploy syscall.
"""

import pytest

from .account import execute, execute_single
from .shared import (
    ABI_PATH,
    CONTRACT_PATH,
    DEPLOYER_ABI_PATH,
    DEPLOYER_CONTRACT_PATH,
    EXPECTED_CLASS_HASH,
)
from .util import (
    assert_contract_class,
    assert_equal,
    assert_hex_equal,
    assert_tx_status,
    call,
    declare,
    deploy,
    devnet_in_background,
    get_class_by_hash,
    get_class_hash_at,
    get_transaction_receipt,
    invoke,
)


def assert_deployed_through_syscall(tx_hash, initial_balance: str):
    """Asserts that a contract has been deployed using the deploy syscall"""
    assert_tx_status(tx_hash, "ACCEPTED_ON_L2")

    # Get deployment address from emitted event
    tx_receipt = get_transaction_receipt(tx_hash=tx_hash)
    events = tx_receipt["events"]
    assert_equal(len(events), 1, explanation=events)
    event = events[0]
    assert_equal(len(event["data"]), 1, explanation=events)
    contract_address = event["data"][0]

    # Test deployed contract
    fetched_class_hash = get_class_hash_at(contract_address=contract_address)
    assert_hex_equal(fetched_class_hash, EXPECTED_CLASS_HASH)

    balance = call(function="get_balance", address=contract_address, abi_path=ABI_PATH)
    assert_equal(balance, initial_balance)


PREDEPLOYED_ACCOUNT_ADDRESS = (
    "0x347be35996a21f6bf0623e75dbce52baba918ad5ae8d83b6f416045ab22961a"
)
PREDEPLOYED_ACCOUNT_PRIVATE_KEY = 0xBDD640FB06671AD11C80317FA3B1799D


@pytest.mark.declare
@devnet_in_background("--accounts", "1", "--seed", "42")
def test_declare_and_deploy():
    """
    Test declaring a class and deploying it through an account.
    """

    # Declare the class to be deployed
    declare_info = declare(contract=CONTRACT_PATH)
    class_hash = declare_info["class_hash"]
    assert_hex_equal(class_hash, EXPECTED_CLASS_HASH)

    contract_class = get_class_by_hash(class_hash=class_hash)
    assert_contract_class(contract_class, CONTRACT_PATH)

    # Deploy the deployer - also deploys a contract of the declared class using the deploy syscall
    initial_balance_in_constructor = "5"
    deployer_deploy_info = deploy(
        contract=DEPLOYER_CONTRACT_PATH,
        inputs=[declare_info["class_hash"], initial_balance_in_constructor],
    )
    deployer_address = deployer_deploy_info["address"]

    assert_deployed_through_syscall(
        deployer_deploy_info["tx_hash"], initial_balance_in_constructor
    )

    # Deploy a contract of the declared class through the deployer
    initial_balance = "10"
    invoke_tx_hash = execute_single(
        function="deploy_contract",
        inputs=[initial_balance],
        address=deployer_address,
        account_address=PREDEPLOYED_ACCOUNT_ADDRESS,
        private_key=PREDEPLOYED_ACCOUNT_PRIVATE_KEY,
    )
    assert_deployed_through_syscall(invoke_tx_hash, str(initial_balance))

    # Deploy a contract of the declared class through the deployer - using an account
    initial_balance_through_account = 15
    invoke_through_account_tx_hash = execute(
        calls=[
            (
                int(deployer_address, 16),
                "deploy_contract",
                [initial_balance_through_account],
            )
        ],
        account_address=PREDEPLOYED_ACCOUNT_ADDRESS,
        private_key=PREDEPLOYED_ACCOUNT_PRIVATE_KEY,
    )
    assert_deployed_through_syscall(
        tx_hash=invoke_through_account_tx_hash,
        initial_balance=str(initial_balance_through_account),
    )
