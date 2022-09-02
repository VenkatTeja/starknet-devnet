"""
Test block number
"""

from test.account import execute_single
from .shared import (
    ARTIFACTS_PATH,
    FAILING_CONTRACT_PATH,
    GENESIS_BLOCK_NUMBER,
    PREDEPLOYED_ACCOUNT_ADDRESS,
    PREDEPLOYED_ACCOUNT_PRIVATE_KEY,
)
from .util import declare, devnet_in_background, deploy, call, invoke

BLOCK_NUMBER_CONTRACT_PATH = f"{ARTIFACTS_PATH}/block_number.cairo/block_number.json"
BLOCK_NUMBER_ABI_PATH = f"{ARTIFACTS_PATH}/block_number.cairo/block_number_abi.json"


def my_get_block_number(address: str):
    """Execute my_get_block_number on block_number.cairo contract deployed at `address`"""
    return call(
        function="my_get_block_number", address=address, abi_path=BLOCK_NUMBER_ABI_PATH
    )


def base_workflow():
    """Used by test cases to perform the test"""
    deploy_info = deploy(BLOCK_NUMBER_CONTRACT_PATH)
    block_number_before = my_get_block_number(deploy_info["address"])
    assert int(block_number_before) == GENESIS_BLOCK_NUMBER + 1

    execute_single(
        address=deploy_info["address"],
        function="write_block_number",
        inputs=[],
        account_address=PREDEPLOYED_ACCOUNT_ADDRESS,
        private_key=PREDEPLOYED_ACCOUNT_PRIVATE_KEY,
    )

    written_block_number = call(
        function="read_block_number",
        inputs=[],
        address=deploy_info["address"],
        abi_path=BLOCK_NUMBER_ABI_PATH,
    )
    assert int(written_block_number) == GENESIS_BLOCK_NUMBER + 2

    block_number_after = my_get_block_number(deploy_info["address"])
    assert int(block_number_after) == GENESIS_BLOCK_NUMBER + 2


@devnet_in_background()
def test_block_number_incremented():
    """Tests how block number is incremented in regular mode"""
    base_workflow()


@devnet_in_background("--lite-mode")
def test_block_number_incremented_in_lite_mode():
    """Tests compatibility with lite mode"""
    base_workflow()


@devnet_in_background()
def test_block_number_incremented_on_declare():
    """Declare tx should increment get_block_number response"""

    deploy_info = deploy(BLOCK_NUMBER_CONTRACT_PATH)
    block_number_before = my_get_block_number(deploy_info["address"])
    assert int(block_number_before) == GENESIS_BLOCK_NUMBER + 1

    # just to declare a new class - nothing fails here
    declare(FAILING_CONTRACT_PATH)

    block_number_after = my_get_block_number(deploy_info["address"])
    assert int(block_number_after) == GENESIS_BLOCK_NUMBER + 2


@devnet_in_background()
def test_block_number_not_incremented_if_deploy_fails():
    """
    Since the deploy fails, no block should be created;
    get_block_number should return an unchanged value
    """

    deploy_info = deploy(BLOCK_NUMBER_CONTRACT_PATH)
    block_number_before = my_get_block_number(deploy_info["address"])
    assert int(block_number_before) == GENESIS_BLOCK_NUMBER + 1

    deploy(FAILING_CONTRACT_PATH)

    block_number_after = my_get_block_number(deploy_info["address"])
    assert int(block_number_after) == GENESIS_BLOCK_NUMBER + 1


@devnet_in_background()
def test_block_number_not_incremented_if_invoke_fails():
    """
    Since the invoke fails, no block should be created;
    get_block_number should return an unchanged value
    """

    deploy_info = deploy(BLOCK_NUMBER_CONTRACT_PATH)
    block_number_before = my_get_block_number(deploy_info["address"])
    assert int(block_number_before) == GENESIS_BLOCK_NUMBER + 1

    execute_single(
        function="fail",
        inputs=[],
        address=deploy_info["address"],
        account_address=PREDEPLOYED_ACCOUNT_ADDRESS,
        private_key=PREDEPLOYED_ACCOUNT_PRIVATE_KEY,
    )

    block_number_after = my_get_block_number(deploy_info["address"])
    assert int(block_number_after) == GENESIS_BLOCK_NUMBER + 1
