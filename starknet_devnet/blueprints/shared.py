"""
Shared functions between blueprints
"""

from marshmallow import ValidationError

from starknet_devnet.constants import CAIRO_LANG_VERSION
from starknet_devnet.util import StarknetDevnetException

# TODO restore to using Transaction
def validate_transaction(transaction_dict: dict, loader):
    """Ensure `transaction_dict` is a valid Starknet transaction. Returns the parsed Transaction."""
    try:
        dict_copy = transaction_dict.copy()
        del dict_copy["type"]
        transaction = loader.load(dict_copy)
    except (TypeError, ValidationError) as err:
        msg = f"""Invalid tx: {err}
Be sure to use the correct compilation (json) artifact. Devnet-compatible cairo-lang version: {CAIRO_LANG_VERSION}"""
        raise StarknetDevnetException(message=msg, status_code=400) from err

    return transaction
