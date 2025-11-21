from typing import Dict, List


REQUIRED_FIELDS = [
    "event_id",
    "account_id",
    "strategy_id",
    "environment",
    "venue",
    "timestamp",
    "symbol",
    "side",
    "order_type",
    "quantity",
    "quantity_type",
    "price_open",
    "price_close",
    "fees",
    "pnl",
    "state",
]

ALLOWED_ENVIRONMENTS = {"live", "demo"}
ALLOWED_SIDES = {"buy", "sell"}
ALLOWED_QUANTITY_TYPES = {"lots", "units"}
ALLOWED_STATES = {"open", "closed"}


class TradeEventValidationError(Exception):
    """Custom exception for invalid TRADE_EVENT objects."""
    pass


def validate_trade_event(event: Dict) -> None:
    """
    Validate a TRADE_EVENT dict according to basic rules.

    - Check required fields are present.
    - Check certain fields have allowed values.
    - Check numeric fields can be interpreted as floats.

    Raises TradeEventValidationError if something is wrong.
    """

    missing: List[str] = [field for field in REQUIRED_FIELDS if field not in event]
    if missing:
        raise TradeEventValidationError(f"Missing required fields: {missing}")

    # environment
    env = str(event.get("environment"))
    if env not in ALLOWED_ENVIRONMENTS:
        raise TradeEventValidationError(f"Invalid environment: {env!r}. Expected one of {ALLOWED_ENVIRONMENTS}")

    # side
    side = str(event.get("side"))
    if side not in ALLOWED_SIDES:
        raise TradeEventValidationError(f"Invalid side: {side!r}. Expected one of {ALLOWED_SIDES}")

    # quantity_type
    qty_type = str(event.get("quantity_type"))
    if qty_type not in ALLOWED_QUANTITY_TYPES:
        raise TradeEventValidationError(
            f"Invalid quantity_type: {qty_type!r}. Expected one of {ALLOWED_QUANTITY_TYPES}"
        )

    # state
    state = str(event.get("state"))
    if state not in ALLOWED_STATES:
        raise TradeEventValidationError(f"Invalid state: {state!r}. Expected one of {ALLOWED_STATES}")

    # numeric fields: quantity, price_open, price_close, fees, pnl
    numeric_fields = ["quantity", "price_open", "price_close", "fees", "pnl"]
    for field in numeric_fields:
        value = event.get(field)
        try:
            float(value)
        except (TypeError, ValueError):
            raise TradeEventValidationError(f"Field {field!r} must be numeric, got: {value!r}")

    # If we reach here, the event passes basic validation.
