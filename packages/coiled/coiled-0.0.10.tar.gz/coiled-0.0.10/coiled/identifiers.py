# Unfortunately there's an exact copy of this file in the REST API, since
# they don't share code. This is not ideal, but please keep both up to date.
from typing import Tuple, Optional
import re


def is_slug(name: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9-_]+$", name))


class ParseIdentifierError(ValueError):
    def __init__(self, which_name):
        super().__init__(
            f"Invalid {which_name}: should have format (<account>/)<name>,"
            ' for example "coiled/xgboost" or "python-37". The <name> '
            ' is required ("xgboost" and "python-37" in the previous examples),'
            " and can contain ASCII letters, numbers, hyphens and underscores."
            f' The account prefix (i.e. "coiled/") can be used to specifies a {which_name}'
            " from a different account."
        )


def parse_identifier(identifier: str, property_name: str) -> Tuple[Optional[str], str]:
    """
    Parameters
    ----------
    identifier:
        identifier of the resource, i.e. "coiled/xgboost" or "python-37"
    property_name:
        The name of the parameter that was being validated; will be printed
        with any error messages, i.e. "software_environment".

    Examples
    --------
    >>> parse_identifier("coiled/xgboost", "software_environment")
    ("coiled", "xgboost")
    >>> parse_identifier("xgboost", "software_environment")
    (None, "xgboost")

    Raises
    ------
    ParseIdentifierError
    """
    identifier = identifier.split("/")
    len_full_name = len(identifier)
    if len_full_name == 1:
        account = None
        name = identifier[0]
    elif len_full_name == 2:
        account, name = identifier
    else:
        raise ParseIdentifierError(property_name)

    if not is_slug(name):
        raise ParseIdentifierError(property_name)

    return account, name
