def str_to_bool(value) -> bool:
    """
    Convert string to boolean.
    """
    return True if value == "True" else False


def str_to_int(value) -> int | None:
    """
    Convert string to integer.
    """
    return int(value) if (value or "").isdigit() else None
