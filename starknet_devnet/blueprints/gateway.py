"""
Gateway routes
"""
import json

from flask import Blueprint, request, jsonify
from starkware.starknet.definitions.transaction_type import TransactionType
from starkware.starknet.services.api.gateway.transaction import (
    Deploy,
    Declare,
    InvokeFunction,
)
from starkware.starkware_utils.error_handling import StarkErrorCode

from starknet_devnet.devnet_config import DumpOn
from starknet_devnet.util import StarknetDevnetException, fixed_length_hex
from starknet_devnet.state import state
from .shared import validate_transaction

gateway = Blueprint("gateway", __name__, url_prefix="/gateway")


@gateway.route("/is_alive", methods=["GET"])
def is_alive():
    """Health check endpoint."""
    return "Alive!!!"


@gateway.route("/add_transaction", methods=["POST"])
async def add_transaction():
    """Endpoint for accepting (state-changing) transactions."""

    raw_transaction = json.loads(request.data)
    tx_type = raw_transaction["type"]

    response_dict = {
        "code": StarkErrorCode.TRANSACTION_RECEIVED.name,
    }

    if tx_type == TransactionType.DECLARE.name:
        contract_class_hash, transaction_hash = await state.starknet_wrapper.declare(
            validate_transaction(raw_transaction, Declare)
        )
        response_dict["class_hash"] = hex(contract_class_hash)

    elif tx_type == TransactionType.DEPLOY.name:
        contract_address, transaction_hash = await state.starknet_wrapper.deploy(
            validate_transaction(raw_transaction, Deploy)
        )
        response_dict["address"] = fixed_length_hex(contract_address)

    elif tx_type == TransactionType.INVOKE_FUNCTION.name:
        (contract_address, transaction_hash) = await state.starknet_wrapper.invoke(
            validate_transaction(raw_transaction, InvokeFunction)
        )
        response_dict["address"] = fixed_length_hex(contract_address)

    else:
        raise StarknetDevnetException(
            message=f"Invalid tx_type: {tx_type.name}.", status_code=400
        )

    response_dict["transaction_hash"] = hex(transaction_hash)

    # after tx
    if state.dumper.dump_on == DumpOn.TRANSACTION:
        state.dumper.dump()

    return jsonify(response_dict)
