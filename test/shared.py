"""Shared values between tests"""

ARTIFACTS_PATH = "test/artifacts/contracts/cairo"
CONTRACT_PATH = f"{ARTIFACTS_PATH}/contract.cairo/contract.json"
ABI_PATH = f"{ARTIFACTS_PATH}/contract.cairo/contract_abi.json"
STORAGE_CONTRACT_PATH = f"{ARTIFACTS_PATH}/storage.cairo/storage.json"
STORAGE_ABI_PATH = f"{ARTIFACTS_PATH}/storage.cairo/storage_abi.json"
EVENTS_CONTRACT_PATH = f"{ARTIFACTS_PATH}/events.cairo/events.json"
EVENTS_ABI_PATH = f"{ARTIFACTS_PATH}/events.cairo/events_abi.json"
FAILING_CONTRACT_PATH = f"{ARTIFACTS_PATH}/always_fail.cairo/always_fail.json"
DEPLOYER_CONTRACT_PATH = f"{ARTIFACTS_PATH}/deployer.cairo/deployer.json"
DEPLOYER_ABI_PATH = f"{ARTIFACTS_PATH}/deployer.cairo/deployer_abi.json"

BALANCE_KEY = (
    "916907772491729262376534102982219947830828984996257231353398618781993312401"
)

SIGNATURE = [
    "1225578735933442828068102633747590437426782890965066746429241472187377583468",
    "3568809569741913715045370357918125425757114920266578211811626257903121825123",
]

EXPECTED_SALTY_DEPLOY_ADDRESS = (
    "0x07a0c836e446fb20e2b8e3354251b862ea45cfd039bb158576f5e8d0983ff2bb"
)
EXPECTED_SALTY_DEPLOY_HASH = (
    "0x23801cc34aa43f4e2bf3e74a838fe45dd1b1ad316a2d3545aaef7efe1f39b21"
)
EXPECTED_SALTY_DEPLOY_HASH_LITE_MODE = (
    "0x2"
)
EXPECTED_CLASS_HASH = "0x757a84aa38bf4ad191a7dfea2e8146fc7f3c4aa6090a8f0bddd7b688f0b24c"

NONEXISTENT_TX_HASH = "0x1"
GENESIS_BLOCK_NUMBER = 0
GENESIS_BLOCK_HASH = "0x0"
INCORRECT_GENESIS_BLOCK_HASH = "0x1"
DEFAULT_GAS_PRICE = int(1e11)
